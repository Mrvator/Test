#!/usr/bin/env python3
"""Plot PathDist/RotDist relationships from pathl CSV logs as standalone SVGs."""

from __future__ import annotations

import argparse
import csv
import html
import math
from pathlib import Path
from statistics import median


WIDTH = 1200
HEIGHT = 820
MARGIN_LEFT = 82
MARGIN_RIGHT = 34
MARGIN_TOP = 58
MARGIN_BOTTOM = 72
PANEL_GAP = 72
POINT_LIMIT = 7000
BIN_COUNT = 60
RATIO_ZERO_TOL = 1e-12
RATIO_UNUSED_SENTINEL = 999.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="pathl_v17.csv", help="Input pathl CSV")
    parser.add_argument("--out-dir", default="reports", help="Output directory")
    parser.add_argument("--suffix", default="v17", help="Output filename suffix")
    return parser.parse_args()


def pick_column(header: list[str], *names: str) -> str:
    lookup = {name.lower(): name for name in header}
    for name in names:
        found = lookup.get(name.lower())
        if found:
            return found
    raise ValueError(f"Missing required column; tried: {', '.join(names)}")


def as_float(value: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return math.nan
    return result if math.isfinite(result) else math.nan


def read_rows(path: Path) -> list[dict[str, float]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header")
        path_length = pick_column(reader.fieldnames, "PathLength", "PathLenth")
        rot_length = pick_column(reader.fieldnames, "RotLength")
        path_dist = pick_column(reader.fieldnames, "PathDist")
        rot_dist = pick_column(reader.fieldnames, "RotDist", "Rotdist")
        ratio_path = pick_column(reader.fieldnames, "RatioPath", "PathRatio")
        ratio_rot = pick_column(reader.fieldnames, "RatioRot", "RotRatio")

        rows: list[dict[str, float]] = []
        for row in reader:
            values = {
                "PathLength": as_float(row.get(path_length, "")),
                "RotLength": as_float(row.get(rot_length, "")),
                "PathDist": as_float(row.get(path_dist, "")),
                "RotDist": as_float(row.get(rot_dist, "")),
                "RatioPath": as_float(row.get(ratio_path, "")),
                "RatioRot": as_float(row.get(ratio_rot, "")),
            }
            if all(math.isfinite(value) for value in values.values()):
                rows.append(values)
    if not rows:
        raise ValueError(f"{path} has no usable numeric rows")
    return rows


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


def nice_ticks(lo: float, hi: float, count: int = 6) -> list[float]:
    if lo == hi:
        return [lo]
    span = hi - lo
    raw_step = span / max(count - 1, 1)
    power = 10 ** math.floor(math.log10(raw_step))
    step = min((1, 2, 5, 10), key=lambda value: abs(value * power - raw_step)) * power
    start = math.floor(lo / step) * step
    ticks = []
    current = start
    while current <= hi + step * 0.5:
        if current >= lo - step * 0.5:
            ticks.append(current)
        current += step
    return ticks


def fmt_tick(value: float) -> str:
    if abs(value) >= 100:
        return f"{value:.0f}"
    if abs(value) >= 10:
        return f"{value:.1f}".rstrip("0").rstrip(".")
    return f"{value:.2f}".rstrip("0").rstrip(".")


def sampled_points(rows: list[dict[str, float]], x_key: str, y_key: str) -> list[tuple[float, float]]:
    step = max(1, len(rows) // POINT_LIMIT)
    return [(row[x_key], row[y_key]) for row in rows[::step]]


def binned_series(rows: list[dict[str, float]], x_key: str, y_key: str) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    x_values = [row[x_key] for row in rows]
    x_min = min(x_values)
    x_max = max(x_values)
    if x_min == x_max:
        return [], []
    bins: list[list[float]] = [[] for _ in range(BIN_COUNT)]
    for row in rows:
        index = min(BIN_COUNT - 1, int((row[x_key] - x_min) / (x_max - x_min) * BIN_COUNT))
        bins[index].append(row[y_key])

    medians: list[tuple[float, float]] = []
    p95s: list[tuple[float, float]] = []
    for index, values in enumerate(bins):
        if not values:
            continue
        center = x_min + (index + 0.5) * (x_max - x_min) / BIN_COUNT
        medians.append((center, median(values)))
        p95s.append((center, percentile(values, 0.95)))
    return medians, p95s


def polyline(points: list[tuple[float, float]], x_scale, y_scale, color: str, width: float, dash: str = "") -> str:
    if len(points) < 2:
        return ""
    coords = " ".join(f"{x_scale(x):.2f},{y_scale(y):.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{dash_attr}/>'


def draw_panel(
    rows: list[dict[str, float]],
    x_key: str,
    y_key: str,
    title: str,
    y_label: str,
    top: float,
    height: float,
    color: str,
    show_x_labels: bool,
) -> list[str]:
    left = MARGIN_LEFT
    right = WIDTH - MARGIN_RIGHT
    bottom = top + height
    x_values = [row[x_key] for row in rows]
    y_values = [row[y_key] for row in rows]
    x_min, x_max = min(x_values), max(x_values)
    y_min = 0
    y_max = max(y_values)
    y_max *= 1.05
    if y_max <= y_min:
        y_max = 1

    def x_scale(value: float) -> float:
        return left + (value - x_min) / (x_max - x_min) * (right - left)

    def y_scale(value: float) -> float:
        clipped = min(max(value, y_min), y_max)
        return bottom - (clipped - y_min) / (y_max - y_min) * height

    parts = [
        f'<text x="{left}" y="{top - 18}" class="panel-title">{html.escape(title)}</text>',
        f'<rect x="{left}" y="{top}" width="{right - left}" height="{height}" class="plot-bg"/>',
    ]

    for tick in nice_ticks(y_min, y_max):
        y = y_scale(tick)
        parts.append(f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" class="grid"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" class="tick">{fmt_tick(tick)}</text>')

    for tick in nice_ticks(x_min, x_max):
        x = x_scale(tick)
        parts.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{bottom}" class="grid"/>')
        if show_x_labels:
            parts.append(f'<text x="{x:.2f}" y="{bottom + 26}" text-anchor="middle" class="tick">{fmt_tick(tick)}</text>')

    parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>')
    parts.append(
        f'<text x="{left - 56}" y="{top + height / 2}" transform="rotate(-90 {left - 56} {top + height / 2})" '
        f'text-anchor="middle" class="axis-label">{html.escape(y_label)}</text>'
    )

    for x, y in sampled_points(rows, x_key, y_key):
        parts.append(f'<circle cx="{x_scale(x):.2f}" cy="{y_scale(y):.2f}" r="1.35" fill="{color}" opacity="0.18"/>')

    medians, p95s = binned_series(rows, x_key, y_key)
    parts.append(polyline(p95s, x_scale, y_scale, color, 2.0, "6 5"))
    parts.append(polyline(medians, x_scale, y_scale, color, 3.0))
    return parts


def make_svg(rows: list[dict[str, float]], x_key: str, x_label: str, title: str) -> str:
    panel_height = (HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - PANEL_GAP) / 2
    first_top = MARGIN_TOP
    second_top = MARGIN_TOP + panel_height + PANEL_GAP
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="820" viewBox="0 0 1200 820">',
        "<style>",
        "svg{background:#f8fafc;color:#1f2937;font-family:Segoe UI,Arial,sans-serif}",
        ".title{font-size:24px;font-weight:700;fill:#111827}",
        ".subtitle,.legend{font-size:13px;fill:#4b5563}",
        ".panel-title{font-size:16px;font-weight:650;fill:#111827}",
        ".plot-bg{fill:#ffffff;stroke:#d1d5db;stroke-width:1}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#374151;stroke-width:1.4}",
        ".tick{font-size:12px;fill:#4b5563}",
        ".axis-label{font-size:13px;font-weight:600;fill:#374151}",
        "</style>",
        f'<text x="{MARGIN_LEFT}" y="32" class="title">{html.escape(title)}</text>',
        f'<text x="{WIDTH - MARGIN_RIGHT}" y="32" text-anchor="end" class="subtitle">n={len(rows)}; points are sampled, line=median, dashed=p95</text>',
    ]
    parts.extend(draw_panel(rows, x_key, "PathDist", "PathDist", "PathDist [mm]", first_top, panel_height, "#2563eb", False))
    parts.extend(draw_panel(rows, x_key, "RotDist", "RotDist", "RotDist [deg]", second_top, panel_height, "#dc2626", True))
    x_center = (MARGIN_LEFT + WIDTH - MARGIN_RIGHT) / 2
    parts.append(f'<text x="{x_center}" y="{HEIGHT - 24}" text-anchor="middle" class="axis-label">{html.escape(x_label)}</text>')
    parts.append('<text x="930" y="776" class="legend" fill="#2563eb">modra: PathDist</text>')
    parts.append('<text x="1040" y="776" class="legend" fill="#dc2626">cervena: RotDist</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def has_unused_ratio_sentinel(rows: list[dict[str, float]]) -> bool:
    return any(
        abs(row[ratio_key] - RATIO_UNUSED_SENTINEL) <= RATIO_ZERO_TOL
        for row in rows
        for ratio_key in ("RatioPath", "RatioRot")
    )


def is_used_ratio(value: float, allow_zero: bool) -> bool:
    lower_bound_ok = value >= -RATIO_ZERO_TOL if allow_zero else value > RATIO_ZERO_TOL
    return (
        math.isfinite(value)
        and lower_bound_ok
        and value <= 1.0
        and abs(value - RATIO_UNUSED_SENTINEL) > RATIO_ZERO_TOL
    )


def rows_with_ratio(rows: list[dict[str, float]], ratio_key: str, allow_zero: bool) -> list[dict[str, float]]:
    return [row for row in rows if is_used_ratio(row[ratio_key], allow_zero)]


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_rows(csv_path)
    allow_zero_ratio = has_unused_ratio_sentinel(rows)
    path_ratio_rows = rows_with_ratio(rows, "RatioPath", allow_zero_ratio)
    rot_ratio_rows = rows_with_ratio(rows, "RatioRot", allow_zero_ratio)

    if not path_ratio_rows:
        raise ValueError("No rows with used RatioPath")
    if not rot_ratio_rows:
        raise ValueError("No rows with used RatioRot")

    outputs = {
        out_dir / f"pathratio_pathdist_rotdist_vs_pathlength_{args.suffix}.svg": make_svg(
            path_ratio_rows,
            "PathLength",
            "PathLength [mm]",
            f"PathDist and RotDist by PathLength - used RatioPath ({csv_path.name})",
        ),
        out_dir / f"pathratio_pathdist_rotdist_vs_rotlength_{args.suffix}.svg": make_svg(
            path_ratio_rows,
            "RotLength",
            "RotLength [deg]",
            f"PathDist and RotDist by RotLength - used RatioPath ({csv_path.name})",
        ),
        out_dir / f"rotratio_pathdist_rotdist_vs_pathlength_{args.suffix}.svg": make_svg(
            rot_ratio_rows,
            "PathLength",
            "PathLength [mm]",
            f"PathDist and RotDist by PathLength - used RatioRot ({csv_path.name})",
        ),
        out_dir / f"rotratio_pathdist_rotdist_vs_rotlength_{args.suffix}.svg": make_svg(
            rot_ratio_rows,
            "RotLength",
            "RotLength [deg]",
            f"PathDist and RotDist by RotLength - used RatioRot ({csv_path.name})",
        ),
    }
    for path, svg in outputs.items():
        path.write_text(svg, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
