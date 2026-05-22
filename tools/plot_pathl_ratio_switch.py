#!/usr/bin/env python3
"""Plot RatioPath vs RatioRot precision by PathLength as standalone SVG."""

from __future__ import annotations

import argparse
import csv
import html
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


WIDTH = 1200
HEIGHT = 760
LEFT = 86
RIGHT = 34
TOP = 62
BOTTOM = 94
XY_WIDTH = 1200
XY_HEIGHT = 860
XY_LEFT = 92
XY_RIGHT = 164
XY_TOP = 72
XY_BOTTOM = 92
BIN_WIDTH_MM = 1.0
ROLLING_WINDOW_GROUPS = 75
RATIO_UNUSED_SENTINEL = 999.0
RATIO_ZERO_TOL = 1e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="pathl_v17.csv", help="Input pathl CSV")
    parser.add_argument("--out-dir", default="reports", help="Output directory")
    parser.add_argument("--suffix", default="v17", help="Output filename suffix")
    parser.add_argument(
        "--reference-mm",
        type=float,
        default=10.0,
        help="Reference PathLength line to draw in the plot",
    )
    return parser.parse_args()


def as_float(value: str | None) -> float:
    try:
        result = float(value or "")
    except ValueError:
        return math.nan
    return result if math.isfinite(result) else math.nan


def used_ratio_value(value: str | None) -> float:
    ratio = as_float(value)
    if math.isfinite(ratio) and abs(ratio - RATIO_UNUSED_SENTINEL) <= RATIO_ZERO_TOL:
        return math.nan
    return ratio


def pick_column(header: list[str], *names: str) -> str:
    lookup = {name.lower(): name for name in header}
    for name in names:
        found = lookup.get(name.lower())
        if found:
            return found
    raise ValueError(f"Missing required column; tried: {', '.join(names)}")


def percentile(values: list[float], q: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    index = (len(ordered) - 1) * q
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[int(index)]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def read_group_precision(path: Path) -> list[dict[str, float | str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header")
        test_col = pick_column(reader.fieldnames, "testId")
        conf_col = pick_column(reader.fieldnames, "confId")
        branch_col = pick_column(reader.fieldnames, "branch S/L", "branch")
        path_col = pick_column(reader.fieldnames, "PathLength", "PathLenth")
        rot_col = pick_column(reader.fieldnames, "RotLength")
        ratio_path_col = pick_column(reader.fieldnames, "RatioPath", "PathRatio")
        ratio_rot_col = pick_column(reader.fieldnames, "RatioRot", "RotRatio")

        groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
        for row in reader:
            key = (row[test_col], row[conf_col], row[branch_col])
            groups[key].append(row)

    records: list[dict[str, float | str]] = []
    for (test_id, conf_id, branch), rows in sorted(groups.items(), key=lambda item: tuple(item[0])):
        if len(rows) < 2 or len(rows) % 2:
            continue

        path_length = as_float(rows[0].get(path_col))
        rot_length = as_float(rows[0].get(rot_col))
        if not math.isfinite(path_length) or not math.isfinite(rot_length):
            continue

        path_errors: list[float] = []
        rot_errors: list[float] = []
        for index in range(0, len(rows), 2):
            expected = (index // 2 + 1) / 100.0
            path_ratio = used_ratio_value(rows[index].get(ratio_path_col))
            rot_ratio = used_ratio_value(rows[index + 1].get(ratio_rot_col))
            if math.isfinite(path_ratio):
                path_errors.append(abs(path_ratio - expected))
            if math.isfinite(rot_ratio):
                rot_errors.append(abs(rot_ratio - expected))

        if not path_errors or not rot_errors:
            continue

        records.append(
            {
                "testId": test_id,
                "confId": conf_id,
                "branch": branch,
                "PathLength": path_length,
                "RotLength": rot_length,
                "PathErrorMean": mean(path_errors),
                "PathErrorMedian": median(path_errors),
                "PathErrorP95": percentile(path_errors, 0.95),
                "RotErrorMean": mean(rot_errors),
                "RotErrorMedian": median(rot_errors),
                "RotErrorP95": percentile(rot_errors, 0.95),
            }
        )

    if not records:
        raise ValueError(f"{path} has no complete PathL ratio groups")
    return records


def binned_rows(records: list[dict[str, float | str]]) -> list[dict[str, float | int]]:
    min_x = math.floor(min(float(row["PathLength"]) for row in records))
    max_x = math.ceil(max(float(row["PathLength"]) for row in records))
    rows: list[dict[str, float | int]] = []

    edge = float(min_x)
    while edge < max_x:
        next_edge = edge + BIN_WIDTH_MM
        values = [row for row in records if edge <= float(row["PathLength"]) < next_edge]
        if values:
            path_means = [float(row["PathErrorMean"]) for row in values]
            rot_means = [float(row["RotErrorMean"]) for row in values]
            rows.append(
                {
                    "PathLengthFrom": edge,
                    "PathLengthTo": next_edge,
                    "PathLengthCenter": (edge + next_edge) / 2,
                    "Groups": len(values),
                    "RatioPathMeanErrorMedian": median(path_means),
                    "RatioPathMeanErrorP95": percentile(path_means, 0.95),
                    "RatioRotMeanErrorMedian": median(rot_means),
                    "RatioRotMeanErrorP95": percentile(rot_means, 0.95),
                    "PathMinusRot": median(path_means) - median(rot_means),
                }
            )
        edge = next_edge
    return rows


def rolling_series(records: list[dict[str, float | str]]) -> list[tuple[float, float, float]]:
    ordered = sorted(records, key=lambda row: float(row["PathLength"]))
    window = min(ROLLING_WINDOW_GROUPS, len(ordered))
    if window < 3:
        return []
    series: list[tuple[float, float, float]] = []
    for start in range(0, len(ordered) - window + 1):
        chunk = ordered[start : start + window]
        x = median(float(row["PathLength"]) for row in chunk)
        path_error = median(float(row["PathErrorMean"]) for row in chunk)
        rot_error = median(float(row["RotErrorMean"]) for row in chunk)
        series.append((x, path_error, rot_error))
    return series


def find_crossing(series: list[tuple[float, float, float]]) -> float | None:
    if len(series) < 2:
        return None
    prev_x, prev_path, prev_rot = series[0]
    prev_delta = prev_path - prev_rot
    for x, path_error, rot_error in series[1:]:
        delta = path_error - rot_error
        if delta == 0:
            return x
        if (prev_delta < 0 and delta > 0) or (prev_delta > 0 and delta < 0):
            span = x - prev_x
            return prev_x + (0 - prev_delta) * span / (delta - prev_delta)
        prev_x = x
        prev_delta = delta
    return None


def nice_ticks(lo: float, hi: float, count: int = 7) -> list[float]:
    if lo == hi:
        return [lo]
    span = hi - lo
    raw_step = span / max(count - 1, 1)
    power = 10 ** math.floor(math.log10(raw_step))
    step = min((1, 2, 5, 10), key=lambda value: abs(value * power - raw_step)) * power
    start = math.floor(lo / step) * step
    ticks: list[float] = []
    current = start
    while current <= hi + step * 0.5:
        if lo <= current <= hi:
            ticks.append(current)
        current += step
    return ticks


def fmt_num(value: float) -> str:
    if not math.isfinite(value):
        return "n/a"
    if abs(value) >= 100:
        return f"{value:.0f}"
    if abs(value) >= 10:
        return f"{value:.1f}".rstrip("0").rstrip(".")
    if abs(value) >= 1:
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{value:.4f}".rstrip("0").rstrip(".")


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def mix_color(left: str, right: str, t: float) -> str:
    left_rgb = hex_to_rgb(left)
    right_rgb = hex_to_rgb(right)
    return rgb_to_hex(
        tuple(round(left_rgb[index] + (right_rgb[index] - left_rgb[index]) * t) for index in range(3))
    )


def error_color(value: float, max_value: float) -> str:
    if not math.isfinite(value) or max_value <= 0:
        return "#9ca3af"
    t = min(max(value / max_value, 0.0), 1.0)
    stops = [
        (0.0, "#0f766e"),
        (0.35, "#84cc16"),
        (0.62, "#f59e0b"),
        (0.82, "#dc2626"),
        (1.0, "#7c3aed"),
    ]
    for index in range(len(stops) - 1):
        left_t, left_color = stops[index]
        right_t, right_color = stops[index + 1]
        if left_t <= t <= right_t:
            local_t = (t - left_t) / (right_t - left_t)
            return mix_color(left_color, right_color, local_t)
    return stops[-1][1]


def padded_range(values: list[float], pad_ratio: float = 0.04) -> tuple[float, float]:
    lo = min(values)
    hi = max(values)
    if lo == hi:
        pad = max(abs(lo) * pad_ratio, 1.0)
    else:
        pad = (hi - lo) * pad_ratio
    return lo - pad, hi + pad


def make_xy_error_svg(
    csv_name: str,
    records: list[dict[str, float | str]],
    ratio_label: str,
    mean_key: str,
    p95_key: str,
    color_max: float,
    radius_max: float,
) -> str:
    plot_width = XY_WIDTH - XY_LEFT - XY_RIGHT
    plot_height = XY_HEIGHT - XY_TOP - XY_BOTTOM
    x_min, x_max = padded_range([float(row["PathLength"]) for row in records])
    y_min, y_max = padded_range([float(row["RotLength"]) for row in records])
    ordered = sorted(records, key=lambda row: float(row[mean_key]))

    def x_scale(value: float) -> float:
        return XY_LEFT + (value - x_min) / (x_max - x_min) * plot_width

    def y_scale(value: float) -> float:
        return XY_TOP + plot_height - (value - y_min) / (y_max - y_min) * plot_height

    def radius(value: float) -> float:
        if not math.isfinite(value) or radius_max <= 0:
            return 2.0
        t = min(max(value / radius_max, 0.0), 1.0)
        return 2.2 + math.sqrt(t) * 5.8

    mean_values = [float(row[mean_key]) for row in records]
    p95_values = [float(row[p95_key]) for row in records]
    stats = (
        median(mean_values),
        percentile(mean_values, 0.95),
        max(mean_values),
        median(p95_values),
        percentile(p95_values, 0.95),
    )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{XY_WIDTH}" height="{XY_HEIGHT}" viewBox="0 0 {XY_WIDTH} {XY_HEIGHT}">',
        "<style>",
        "svg{background:#f8fafc;color:#111827;font-family:Segoe UI,Arial,sans-serif}",
        ".title{font-size:24px;font-weight:700;fill:#111827}",
        ".subtitle,.legend,.note{font-size:13px;fill:#4b5563}",
        ".plot-bg{fill:#ffffff;stroke:#d1d5db;stroke-width:1}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#374151;stroke-width:1.4}",
        ".tick{font-size:12px;fill:#4b5563}",
        ".axis-label{font-size:14px;font-weight:650;fill:#374151}",
        ".stat{font-size:12px;fill:#374151}",
        "</style>",
        f'<text x="{XY_LEFT}" y="34" class="title">{html.escape(ratio_label)} precision by PathLength and RotLength</text>',
        f'<text x="{XY_WIDTH - XY_RIGHT}" y="34" text-anchor="end" class="subtitle">{html.escape(csv_name)}; '
        f'n={len(records)} groups; color=mean abs error, radius=p95</text>',
        f'<rect x="{XY_LEFT}" y="{XY_TOP}" width="{plot_width}" height="{plot_height}" class="plot-bg"/>',
    ]

    for tick in nice_ticks(y_min, y_max):
        y = y_scale(tick)
        parts.append(f'<line x1="{XY_LEFT}" y1="{y:.2f}" x2="{XY_LEFT + plot_width}" y2="{y:.2f}" class="grid"/>')
        parts.append(f'<text x="{XY_LEFT - 12}" y="{y + 4:.2f}" text-anchor="end" class="tick">{fmt_num(tick)}</text>')

    for tick in nice_ticks(x_min, x_max):
        x = x_scale(tick)
        parts.append(f'<line x1="{x:.2f}" y1="{XY_TOP}" x2="{x:.2f}" y2="{XY_TOP + plot_height}" class="grid"/>')
        parts.append(f'<text x="{x:.2f}" y="{XY_TOP + plot_height + 26}" text-anchor="middle" class="tick">{fmt_num(tick)}</text>')

    for row in ordered:
        path_length = float(row["PathLength"])
        rot_length = float(row["RotLength"])
        mean_error = float(row[mean_key])
        p95_error = float(row[p95_key])
        tooltip = (
            f"{ratio_label}&#10;"
            f"testId={html.escape(str(row['testId']))}, confId={html.escape(str(row['confId']))}, branch={html.escape(str(row['branch']))}&#10;"
            f"PathLength={path_length:.4f} mm, RotLength={rot_length:.4f} deg&#10;"
            f"mean abs error={mean_error:.6f}, p95={p95_error:.6f}"
        )
        parts.append(
            f'<circle cx="{x_scale(path_length):.2f}" cy="{y_scale(rot_length):.2f}" '
            f'r="{radius(p95_error):.2f}" fill="{error_color(mean_error, color_max)}" '
            f'opacity="0.72" stroke="#111827" stroke-width="0.25"><title>{tooltip}</title></circle>'
        )

    parts.extend(
        [
            f'<line x1="{XY_LEFT}" y1="{XY_TOP + plot_height}" x2="{XY_LEFT + plot_width}" y2="{XY_TOP + plot_height}" class="axis"/>',
            f'<line x1="{XY_LEFT}" y1="{XY_TOP}" x2="{XY_LEFT}" y2="{XY_TOP + plot_height}" class="axis"/>',
            f'<text x="{XY_LEFT + plot_width / 2}" y="{XY_HEIGHT - 28}" text-anchor="middle" class="axis-label">PathLength [mm]</text>',
            f'<text x="28" y="{XY_TOP + plot_height / 2}" transform="rotate(-90 28 {XY_TOP + plot_height / 2})" '
            f'text-anchor="middle" class="axis-label">RotLength [deg]</text>',
        ]
    )

    legend_x = XY_WIDTH - XY_RIGHT + 34
    legend_y = XY_TOP + 8
    gradient_steps = 12
    for index in range(gradient_steps):
        t0 = index / gradient_steps
        value = color_max * (1 - t0)
        parts.append(
            f'<rect x="{legend_x}" y="{legend_y + index * 18}" width="24" height="18" '
            f'fill="{error_color(value, color_max)}"/>'
        )
    parts.extend(
        [
            f'<text x="{legend_x + 36}" y="{legend_y + 5}" class="legend">clipped p98</text>',
            f'<text x="{legend_x + 36}" y="{legend_y + 19}" class="legend">{fmt_num(color_max * 100)} pp</text>',
            f'<text x="{legend_x + 36}" y="{legend_y + gradient_steps * 18 - 2}" class="legend">0 pp</text>',
            f'<circle cx="{legend_x + 12}" cy="{legend_y + gradient_steps * 18 + 38}" r="2.6" fill="#64748b" opacity="0.65"/>',
            f'<circle cx="{legend_x + 12}" cy="{legend_y + gradient_steps * 18 + 78}" r="8.0" fill="#64748b" opacity="0.65"/>',
            f'<text x="{legend_x + 36}" y="{legend_y + gradient_steps * 18 + 42}" class="legend">lower p95</text>',
            f'<text x="{legend_x + 36}" y="{legend_y + gradient_steps * 18 + 82}" class="legend">higher p95</text>',
            f'<text x="{XY_LEFT}" y="{XY_HEIGHT - 60}" class="note">Mean stats: median {stats[0]:.6f}, p95 {stats[1]:.6f}, max {stats[2]:.6f}; p95-error median {stats[3]:.6f}, p95 {stats[4]:.6f}.</text>',
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts)


def polyline(
    points: list[tuple[float, float]],
    x_scale,
    y_scale,
    color: str,
    width: float,
    dash: str = "",
) -> str:
    if len(points) < 2:
        return ""
    coords = " ".join(f"{x_scale(x):.2f},{y_scale(y):.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" stroke-linecap="round"{dash_attr}/>'
    )


def make_svg(
    csv_name: str,
    records: list[dict[str, float | str]],
    bins: list[dict[str, float | int]],
    series: list[tuple[float, float, float]],
    crossing: float | None,
    reference_mm: float,
) -> str:
    plot_width = WIDTH - LEFT - RIGHT
    plot_height = HEIGHT - TOP - BOTTOM
    x_min = math.floor(min(float(row["PathLength"]) for row in records))
    x_max = math.ceil(max(float(row["PathLength"]) for row in records))
    y_max = max(
        max(path_error for _, path_error, _ in series),
        max(rot_error for _, _, rot_error in series),
        max(float(row["RatioPathMeanErrorP95"]) for row in bins),
        max(float(row["RatioRotMeanErrorP95"]) for row in bins),
    )
    y_max = max(0.01, y_max * 1.15)

    def x_scale(value: float) -> float:
        return LEFT + (value - x_min) / (x_max - x_min) * plot_width

    def y_scale(value: float) -> float:
        return TOP + plot_height - value / y_max * plot_height

    path_points = [(x, path_error) for x, path_error, _ in series]
    rot_points = [(x, rot_error) for x, _, rot_error in series]
    path_p95 = [
        (float(row["PathLengthCenter"]), float(row["RatioPathMeanErrorP95"]))
        for row in bins
    ]
    rot_p95 = [
        (float(row["PathLengthCenter"]), float(row["RatioRotMeanErrorP95"]))
        for row in bins
    ]
    winner = "RatioRot je nizsi v celem merenem rozsahu" if crossing is None else f"prusecik {crossing:.2f} mm"

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
        "<style>",
        "svg{background:#f8fafc;color:#111827;font-family:Segoe UI,Arial,sans-serif}",
        ".title{font-size:24px;font-weight:700;fill:#111827}",
        ".subtitle,.legend,.note{font-size:13px;fill:#4b5563}",
        ".plot-bg{fill:#ffffff;stroke:#d1d5db;stroke-width:1}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#374151;stroke-width:1.4}",
        ".tick{font-size:12px;fill:#4b5563}",
        ".axis-label{font-size:14px;font-weight:650;fill:#374151}",
        ".ref{stroke:#6b7280;stroke-width:1.5;stroke-dasharray:6 6}",
        "</style>",
        f'<text x="{LEFT}" y="32" class="title">RatioPath vs RatioRot precision by PathLength</text>',
        f'<text x="{WIDTH - RIGHT}" y="32" text-anchor="end" class="subtitle">{html.escape(csv_name)}; '
        f'n={len(records)} groups; line=rolling median of group mean abs error</text>',
        f'<rect x="{LEFT}" y="{TOP}" width="{plot_width}" height="{plot_height}" class="plot-bg"/>',
    ]

    for tick in nice_ticks(0, y_max):
        y = y_scale(tick)
        parts.append(f'<line x1="{LEFT}" y1="{y:.2f}" x2="{WIDTH - RIGHT}" y2="{y:.2f}" class="grid"/>')
        parts.append(f'<text x="{LEFT - 12}" y="{y + 4:.2f}" text-anchor="end" class="tick">{fmt_num(tick * 100)}</text>')

    for tick in nice_ticks(x_min, x_max):
        x = x_scale(tick)
        parts.append(f'<line x1="{x:.2f}" y1="{TOP}" x2="{x:.2f}" y2="{TOP + plot_height}" class="grid"/>')
        parts.append(f'<text x="{x:.2f}" y="{TOP + plot_height + 26}" text-anchor="middle" class="tick">{fmt_num(tick)}</text>')

    if x_min <= reference_mm <= x_max:
        x = x_scale(reference_mm)
        parts.append(f'<line x1="{x:.2f}" y1="{TOP}" x2="{x:.2f}" y2="{TOP + plot_height}" class="ref"/>')
        parts.append(f'<text x="{x + 8:.2f}" y="{TOP + 20}" class="note">reference {fmt_num(reference_mm)} mm</text>')

    if crossing is not None and x_min <= crossing <= x_max:
        x = x_scale(crossing)
        parts.append(f'<line x1="{x:.2f}" y1="{TOP}" x2="{x:.2f}" y2="{TOP + plot_height}" stroke="#111827" stroke-width="1.8"/>')
        parts.append(f'<text x="{x + 8:.2f}" y="{TOP + 42}" class="note">crossing {crossing:.2f} mm</text>')

    parts.append(polyline(path_p95, x_scale, y_scale, "#2563eb", 1.6, "5 6"))
    parts.append(polyline(rot_p95, x_scale, y_scale, "#dc2626", 1.6, "5 6"))
    parts.append(polyline(path_points, x_scale, y_scale, "#2563eb", 3.2))
    parts.append(polyline(rot_points, x_scale, y_scale, "#dc2626", 3.2))

    parts.extend(
        [
            f'<line x1="{LEFT}" y1="{TOP + plot_height}" x2="{WIDTH - RIGHT}" y2="{TOP + plot_height}" class="axis"/>',
            f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{TOP + plot_height}" class="axis"/>',
            f'<text x="{LEFT + plot_width / 2}" y="{HEIGHT - 28}" text-anchor="middle" class="axis-label">PathLength [mm]</text>',
            f'<text x="28" y="{TOP + plot_height / 2}" transform="rotate(-90 28 {TOP + plot_height / 2})" '
            f'text-anchor="middle" class="axis-label">abs(Ratio - expected) [percentage points]</text>',
            '<line x1="830" y1="94" x2="878" y2="94" stroke="#2563eb" stroke-width="3.2" stroke-linecap="round"/>',
            '<text x="888" y="99" class="legend">RatioPath</text>',
            '<line x1="830" y1="118" x2="878" y2="118" stroke="#dc2626" stroke-width="3.2" stroke-linecap="round"/>',
            '<text x="888" y="123" class="legend">RatioRot</text>',
            '<line x1="830" y1="142" x2="878" y2="142" stroke="#374151" stroke-width="1.6" stroke-dasharray="5 6"/>',
            '<text x="888" y="147" class="legend">binned p95</text>',
            f'<text x="{LEFT}" y="{HEIGHT - 56}" class="note">{html.escape(winner)}; nizsi cara znamena presnejsi ratio.</text>',
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts)


def write_bins(path: Path, bins: list[dict[str, float | int]]) -> None:
    fieldnames = [
        "PathLengthFrom",
        "PathLengthTo",
        "Groups",
        "RatioPathMeanErrorMedian",
        "RatioPathMeanErrorP95",
        "RatioRotMeanErrorMedian",
        "RatioRotMeanErrorP95",
        "PathMinusRot",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for row in bins:
            writer.writerow({name: row[name] for name in fieldnames})


def write_summary(
    path: Path,
    csv_name: str,
    records: list[dict[str, float | str]],
    bins: list[dict[str, float | int]],
    crossing: float | None,
    svg_path: Path,
    path_xy_svg_path: Path,
    rot_xy_svg_path: Path,
    bin_path: Path,
) -> None:
    path_min = min(float(row["PathLength"]) for row in records)
    path_max = max(float(row["PathLength"]) for row in records)
    rot_min = min(float(row["RotLength"]) for row in records)
    rot_max = max(float(row["RotLength"]) for row in records)
    path_mean_errors = [float(row["PathErrorMean"]) for row in records]
    rot_mean_errors = [float(row["RotErrorMean"]) for row in records]
    lines = [
        f"# PathL Ratio Switch Analysis ({csv_name})",
        "",
        f"- Groups: {len(records)}",
        f"- PathLength range: {path_min:.4f}..{path_max:.4f} mm",
        f"- RotLength range: {rot_min:.4f}..{rot_max:.4f} deg",
        f"- Crossing: {f'{crossing:.4f} mm' if crossing is not None else 'none in measured range'}",
        f"- 1D graph: `{svg_path.as_posix()}`",
        f"- XY RatioPath precision graph: `{path_xy_svg_path.as_posix()}`",
        f"- XY RatioRot precision graph: `{rot_xy_svg_path.as_posix()}`",
        f"- Binned data: `{bin_path.as_posix()}`",
        "",
        "| metric | median mean abs error | p95 mean abs error | max mean abs error |",
        "| --- | ---: | ---: | ---: |",
        f"| RatioPath | {median(path_mean_errors):.6f} | {percentile(path_mean_errors, 0.95):.6f} | {max(path_mean_errors):.6f} |",
        f"| RatioRot | {median(rot_mean_errors):.6f} | {percentile(rot_mean_errors, 0.95):.6f} | {max(rot_mean_errors):.6f} |",
        "",
        "| PathLength [mm] | groups | RatioPath median mean error | RatioRot median mean error | Path - Rot |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in bins:
        lines.append(
            f"| {float(row['PathLengthFrom']):.1f}-{float(row['PathLengthTo']):.1f} | "
            f"{int(row['Groups'])} | "
            f"{float(row['RatioPathMeanErrorMedian']):.6f} | "
            f"{float(row['RatioRotMeanErrorMedian']):.6f} | "
            f"{float(row['PathMinusRot']):+.6f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    records = read_group_precision(csv_path)
    bins = binned_rows(records)
    series = rolling_series(records)
    crossing = find_crossing(series)

    svg_path = out_dir / f"pathl_ratio_switch_vs_pathlength_{args.suffix}.svg"
    path_xy_svg_path = out_dir / f"pathl_ratio_switch_xy_ratiopath_{args.suffix}.svg"
    rot_xy_svg_path = out_dir / f"pathl_ratio_switch_xy_ratiorot_{args.suffix}.svg"
    bin_path = out_dir / f"pathl_ratio_switch_bins_{args.suffix}.csv"
    summary_path = out_dir / f"pathl_ratio_switch_{args.suffix}.md"
    combined_mean_errors = [float(row["PathErrorMean"]) for row in records] + [
        float(row["RotErrorMean"]) for row in records
    ]
    combined_p95_errors = [float(row["PathErrorP95"]) for row in records] + [
        float(row["RotErrorP95"]) for row in records
    ]
    color_max = max(0.001, percentile(combined_mean_errors, 0.98))
    radius_max = max(0.001, percentile(combined_p95_errors, 0.98))

    svg_path.write_text(
        make_svg(csv_path.name, records, bins, series, crossing, args.reference_mm),
        encoding="utf-8",
    )
    path_xy_svg_path.write_text(
        make_xy_error_svg(
            csv_path.name,
            records,
            "RatioPath",
            "PathErrorMean",
            "PathErrorP95",
            color_max,
            radius_max,
        ),
        encoding="utf-8",
    )
    rot_xy_svg_path.write_text(
        make_xy_error_svg(
            csv_path.name,
            records,
            "RatioRot",
            "RotErrorMean",
            "RotErrorP95",
            color_max,
            radius_max,
        ),
        encoding="utf-8",
    )
    write_bins(bin_path, bins)
    write_summary(
        summary_path,
        csv_path.name,
        records,
        bins,
        crossing,
        svg_path,
        path_xy_svg_path,
        rot_xy_svg_path,
        bin_path,
    )

    print(svg_path)
    print(path_xy_svg_path)
    print(rot_xy_svg_path)
    print(bin_path)
    print(summary_path)
    print(f"crossing={crossing if crossing is not None else 'none'}")


if __name__ == "__main__":
    main()
