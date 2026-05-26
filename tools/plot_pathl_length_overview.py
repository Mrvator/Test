#!/usr/bin/env python3
"""Plot raw PathL PathLength/RotLength overview as standalone SVGs."""

from __future__ import annotations

import argparse
import csv
import html
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


MAP_WIDTH = 1220
MAP_HEIGHT = 820
HIST_WIDTH = 1220
HIST_HEIGHT = 820
LEFT = 86
RIGHT = 210
TOP = 66
BOTTOM = 84
BIN_COUNT = 34
EXPECTED_ROWS_PER_GROUP = 200
PATH_WARN_MM = 1.0
ROT_WARN_DEG = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="pathl_v20.csv", help="Input PathL CSV")
    parser.add_argument("--out-dir", default="reports", help="Output directory")
    parser.add_argument("--suffix", default="v20", help="Output filename suffix")
    return parser.parse_args()


def as_float(value: str | None) -> float:
    try:
        result = float(value or "")
    except ValueError:
        return math.nan
    return result if math.isfinite(result) else math.nan


def as_bool(value: str | None) -> bool:
    return str(value or "").strip().upper() == "TRUE"


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


def padded_range(values: list[float], pad_ratio: float = 0.04) -> tuple[float, float]:
    lo = min(values)
    hi = max(values)
    pad = max((hi - lo) * pad_ratio, 1.0) if hi != lo else max(abs(lo) * pad_ratio, 1.0)
    return lo - pad, hi + pad


def raw_median(rows: list[dict[str, str]], column: str) -> float:
    values = [as_float(row.get(column)) for row in rows]
    finite = [value for value in values if math.isfinite(value)]
    return median(finite) if finite else math.nan


def group_status(rows: list[dict[str, str]], branch_col: str, found_col: str, cfx_col: str, path_dist_col: str, rot_dist_col: str) -> str:
    row_count = len(rows)
    found_mismatch = any(row.get(found_col, "") != row.get(branch_col, "") for row in rows)
    cfx_bad = any(not as_bool(row.get(cfx_col)) for row in rows)
    max_path_dist = max((as_float(row.get(path_dist_col)) for row in rows), default=math.nan)
    max_rot_dist = max((as_float(row.get(rot_dist_col)) for row in rows), default=math.nan)
    if found_mismatch or cfx_bad or row_count != EXPECTED_ROWS_PER_GROUP:
        return "branch/incomplete"
    if max_path_dist > PATH_WARN_MM or max_rot_dist > ROT_WARN_DEG:
        return "distance warning"
    return "ok"


def read_groups(path: Path) -> list[dict[str, float | str | int]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header")
        header = reader.fieldnames
        test_col = pick_column(header, "testId")
        conf_col = pick_column(header, "confId")
        branch_col = pick_column(header, "branch S/L", "branch")
        path_col = pick_column(header, "PathLength", "PathLenth")
        rot_col = pick_column(header, "RotLength")
        path_dist_col = pick_column(header, "PathDist")
        rot_dist_col = pick_column(header, "RotDist", "Rotdist")
        found_col = pick_column(header, "FoundBranch")
        cfx_col = pick_column(header, "CfxOK")

        grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
        for row in reader:
            grouped[(row[test_col], row[conf_col], row[branch_col])].append(row)

    records: list[dict[str, float | str | int]] = []
    for (test_id, conf_id, branch), rows in grouped.items():
        path_length = raw_median(rows, path_col)
        rot_length = raw_median(rows, rot_col)
        if not math.isfinite(path_length) or not math.isfinite(rot_length):
            continue
        max_path_dist = max((as_float(row.get(path_dist_col)) for row in rows), default=math.nan)
        max_rot_dist = max((as_float(row.get(rot_dist_col)) for row in rows), default=math.nan)
        mismatch_count = sum(row.get(found_col, "") != row.get(branch_col, "") for row in rows)
        records.append(
            {
                "testId": test_id,
                "confId": conf_id,
                "branch": branch,
                "PathLength": path_length,
                "RotLength": rot_length,
                "rows": len(rows),
                "FoundBranchMismatchRows": mismatch_count,
                "MaxPathDist": max_path_dist,
                "MaxRotDist": max_rot_dist,
                "status": group_status(rows, branch_col, found_col, cfx_col, path_dist_col, rot_dist_col),
            }
        )

    if not records:
        raise ValueError(f"{path} has no complete PathL groups")
    return records


STATUS_STYLE = {
    "ok": ("#0f766e", "OK"),
    "distance warning": ("#f59e0b", "distance > limit"),
    "branch/incomplete": ("#dc2626", "branch mismatch / incomplete"),
}


def make_map_svg(csv_name: str, records: list[dict[str, float | str | int]]) -> str:
    plot_width = MAP_WIDTH - LEFT - RIGHT
    plot_height = MAP_HEIGHT - TOP - BOTTOM
    x_min, x_max = padded_range([float(row["PathLength"]) for row in records])
    y_min, y_max = padded_range([float(row["RotLength"]) for row in records])

    def x_scale(value: float) -> float:
        return LEFT + (value - x_min) / (x_max - x_min) * plot_width

    def y_scale(value: float) -> float:
        return TOP + plot_height - (value - y_min) / (y_max - y_min) * plot_height

    status_counts = Counter(str(row["status"]) for row in records)
    ordered = sorted(records, key=lambda row: ("ok", "distance warning", "branch/incomplete").index(str(row["status"])))
    worst = sorted(
        records,
        key=lambda row: (
            str(row["status"]) == "ok",
            -float(row["MaxPathDist"]) if math.isfinite(float(row["MaxPathDist"])) else 0.0,
            -float(row["MaxRotDist"]) if math.isfinite(float(row["MaxRotDist"])) else 0.0,
        ),
    )[:10]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{MAP_WIDTH}" height="{MAP_HEIGHT}" viewBox="0 0 {MAP_WIDTH} {MAP_HEIGHT}">',
        "<style>",
        "svg{background:#f8fafc;color:#111827;font-family:Segoe UI,Arial,sans-serif}",
        ".title{font-size:24px;font-weight:700;fill:#111827}",
        ".subtitle,.legend,.note{font-size:13px;fill:#4b5563}",
        ".plot-bg{fill:#ffffff;stroke:#d1d5db;stroke-width:1}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#374151;stroke-width:1.4}",
        ".tick{font-size:12px;fill:#4b5563}",
        ".axis-label{font-size:14px;font-weight:650;fill:#374151}",
        ".side-title{font-size:14px;font-weight:700;fill:#111827}",
        ".side-row{font-size:12px;fill:#374151}",
        "</style>",
        f'<text x="{LEFT}" y="34" class="title">PathL raw length outcome map</text>',
        f'<text x="{MAP_WIDTH - RIGHT}" y="34" text-anchor="end" class="subtitle">{html.escape(csv_name)}; n={len(records)} test/conf/branch groups</text>',
        f'<rect x="{LEFT}" y="{TOP}" width="{plot_width}" height="{plot_height}" class="plot-bg"/>',
    ]

    for tick in nice_ticks(y_min, y_max):
        y = y_scale(tick)
        parts.append(f'<line x1="{LEFT}" y1="{y:.2f}" x2="{LEFT + plot_width}" y2="{y:.2f}" class="grid"/>')
        parts.append(f'<text x="{LEFT - 12}" y="{y + 4:.2f}" text-anchor="end" class="tick">{fmt_num(tick)}</text>')
    for tick in nice_ticks(x_min, x_max):
        x = x_scale(tick)
        parts.append(f'<line x1="{x:.2f}" y1="{TOP}" x2="{x:.2f}" y2="{TOP + plot_height}" class="grid"/>')
        parts.append(f'<text x="{x:.2f}" y="{TOP + plot_height + 26}" text-anchor="middle" class="tick">{fmt_num(tick)}</text>')

    for row in ordered:
        status = str(row["status"])
        color = STATUS_STYLE[status][0]
        radius = 3.2 if status == "ok" else 5.7
        tooltip = (
            f"testId={html.escape(str(row['testId']))}, confId={html.escape(str(row['confId']))}, branch={html.escape(str(row['branch']))}&#10;"
            f"status={html.escape(status)}&#10;"
            f"PathLength={float(row['PathLength']):.4f} mm, RotLength={float(row['RotLength']):.4f} deg&#10;"
            f"rows={int(row['rows'])}, FoundBranch mismatch rows={int(row['FoundBranchMismatchRows'])}&#10;"
            f"max PathDist={float(row['MaxPathDist']):.6f}, max RotDist={float(row['MaxRotDist']):.6f}"
        )
        parts.append(
            f'<circle cx="{x_scale(float(row["PathLength"])):.2f}" cy="{y_scale(float(row["RotLength"])):.2f}" '
            f'r="{radius}" fill="{color}" opacity="0.72" stroke="#111827" stroke-width="0.35"><title>{tooltip}</title></circle>'
        )

    parts.extend(
        [
            f'<line x1="{LEFT}" y1="{TOP + plot_height}" x2="{LEFT + plot_width}" y2="{TOP + plot_height}" class="axis"/>',
            f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{TOP + plot_height}" class="axis"/>',
            f'<text x="{LEFT + plot_width / 2}" y="{MAP_HEIGHT - 28}" text-anchor="middle" class="axis-label">PathLength [mm]</text>',
            f'<text x="28" y="{TOP + plot_height / 2}" transform="rotate(-90 28 {TOP + plot_height / 2})" text-anchor="middle" class="axis-label">RotLength [deg]</text>',
        ]
    )

    side_x = MAP_WIDTH - RIGHT + 28
    y = TOP + 10
    parts.append(f'<text x="{side_x}" y="{y}" class="side-title">Groups</text>')
    y += 28
    for status, (_, label) in STATUS_STYLE.items():
        parts.append(f'<circle cx="{side_x + 7}" cy="{y - 4}" r="5" fill="{STATUS_STYLE[status][0]}" opacity="0.78"/>')
        parts.append(f'<text x="{side_x + 22}" y="{y}" class="legend">{html.escape(label)}: {status_counts[status]}</text>')
        y += 24
    y += 18
    parts.append(f'<text x="{side_x}" y="{y}" class="side-title">Worst issue groups</text>')
    y += 22
    for row in worst:
        label = f"{row['testId']}/{row['confId']} {row['branch']}  P{fmt_num(float(row['PathLength']))} R{fmt_num(float(row['RotLength']))}"
        parts.append(f'<text x="{side_x}" y="{y}" class="side-row">{html.escape(label)}</text>')
        y += 18

    parts.append("</svg>")
    return "\n".join(parts)


def bin_records(records: list[dict[str, float | str | int]], key: str) -> list[dict[str, float | int]]:
    values = [float(row[key]) for row in records]
    lo = min(values)
    hi = max(values)
    if lo == hi:
        hi = lo + 1
    width = (hi - lo) / BIN_COUNT
    bins = [
        {
            "from": lo + index * width,
            "to": lo + (index + 1) * width,
            "total": 0,
            "distance": 0,
            "branch": 0,
        }
        for index in range(BIN_COUNT)
    ]
    for row in records:
        value = float(row[key])
        index = min(BIN_COUNT - 1, max(0, int((value - lo) / width)))
        bins[index]["total"] = int(bins[index]["total"]) + 1
        if row["status"] == "distance warning":
            bins[index]["distance"] = int(bins[index]["distance"]) + 1
        elif row["status"] == "branch/incomplete":
            bins[index]["branch"] = int(bins[index]["branch"]) + 1
    return bins


def draw_hist_panel(
    bins: list[dict[str, float | int]],
    title: str,
    x_label: str,
    top: float,
    height: float,
) -> list[str]:
    left = LEFT
    right = HIST_WIDTH - RIGHT
    bottom = top + height
    plot_width = right - left
    max_total = max(int(row["total"]) for row in bins) or 1

    def x_scale(index: int) -> float:
        return left + index / len(bins) * plot_width

    def y_count(value: int) -> float:
        return bottom - value / max_total * height

    parts = [
        f'<text x="{left}" y="{top - 18}" class="side-title">{html.escape(title)}</text>',
        f'<rect x="{left}" y="{top}" width="{plot_width}" height="{height}" class="plot-bg"/>',
    ]
    for tick in nice_ticks(0, max_total):
        y = y_count(int(tick))
        parts.append(f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" class="grid"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" class="tick">{fmt_num(tick)}</text>')

    for index, row in enumerate(bins):
        x0 = x_scale(index) + 1
        x1 = x_scale(index + 1) - 1
        width = max(1, x1 - x0)
        total = int(row["total"])
        branch = int(row["branch"])
        distance = int(row["distance"])
        ok = total - branch - distance
        y = bottom
        for count, color in ((ok, "#94a3b8"), (distance, "#f59e0b"), (branch, "#dc2626")):
            if count <= 0:
                continue
            bar_h = count / max_total * height
            y -= bar_h
            tooltip = (
                f"{x_label}: {float(row['from']):.4f}..{float(row['to']):.4f}&#10;"
                f"total={total}, ok={ok}, distance={distance}, branch/incomplete={branch}"
            )
            parts.append(
                f'<rect x="{x0:.2f}" y="{y:.2f}" width="{width:.2f}" height="{bar_h:.2f}" fill="{color}" opacity="0.82"><title>{tooltip}</title></rect>'
            )

    for tick in nice_ticks(float(bins[0]["from"]), float(bins[-1]["to"])):
        t = (tick - float(bins[0]["from"])) / (float(bins[-1]["to"]) - float(bins[0]["from"]))
        x = left + t * plot_width
        parts.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{bottom}" class="grid"/>')
        parts.append(f'<text x="{x:.2f}" y="{bottom + 25}" text-anchor="middle" class="tick">{fmt_num(tick)}</text>')

    parts.extend(
        [
            f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>',
            f'<text x="{left + plot_width / 2}" y="{bottom + 54}" text-anchor="middle" class="axis-label">{html.escape(x_label)}</text>',
        ]
    )
    return parts


def make_hist_svg(csv_name: str, records: list[dict[str, float | str | int]]) -> str:
    panel_height = 285
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{HIST_WIDTH}" height="{HIST_HEIGHT}" viewBox="0 0 {HIST_WIDTH} {HIST_HEIGHT}">',
        "<style>",
        "svg{background:#f8fafc;color:#111827;font-family:Segoe UI,Arial,sans-serif}",
        ".title{font-size:24px;font-weight:700;fill:#111827}",
        ".subtitle,.legend{font-size:13px;fill:#4b5563}",
        ".plot-bg{fill:#ffffff;stroke:#d1d5db;stroke-width:1}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#374151;stroke-width:1.4}",
        ".tick{font-size:12px;fill:#4b5563}",
        ".axis-label{font-size:14px;font-weight:650;fill:#374151}",
        ".side-title{font-size:14px;font-weight:700;fill:#111827}",
        "</style>",
        f'<text x="{LEFT}" y="34" class="title">PathL raw length distribution</text>',
        f'<text x="{HIST_WIDTH - RIGHT}" y="34" text-anchor="end" class="subtitle">{html.escape(csv_name)}; stacked by group status</text>',
    ]
    parts.extend(draw_hist_panel(bin_records(records, "PathLength"), "PathLength distribution", "PathLength [mm]", TOP, panel_height))
    parts.extend(draw_hist_panel(bin_records(records, "RotLength"), "RotLength distribution", "RotLength [deg]", TOP + panel_height + 105, panel_height))

    side_x = HIST_WIDTH - RIGHT + 28
    y = TOP + 30
    for color, label in (("#94a3b8", "OK"), ("#f59e0b", "distance > limit"), ("#dc2626", "branch mismatch / incomplete")):
        parts.append(f'<rect x="{side_x}" y="{y - 12}" width="18" height="18" fill="{color}" opacity="0.82"/>')
        parts.append(f'<text x="{side_x + 28}" y="{y + 2}" class="legend">{html.escape(label)}</text>')
        y += 28

    parts.append("</svg>")
    return "\n".join(parts)


def write_summary(path: Path, csv_name: str, records: list[dict[str, float | str | int]], map_path: Path, hist_path: Path) -> None:
    counts = Counter(str(row["status"]) for row in records)
    path_lengths = [float(row["PathLength"]) for row in records]
    rot_lengths = [float(row["RotLength"]) for row in records]
    lines = [
        f"# PathL Length Overview ({csv_name})",
        "",
        f"- Groups: {len(records)}",
        f"- OK groups: {counts['ok']}",
        f"- Distance-warning groups: {counts['distance warning']}",
        f"- Branch/incomplete groups: {counts['branch/incomplete']}",
        f"- PathLength range: {min(path_lengths):.4f}..{max(path_lengths):.4f} mm",
        f"- RotLength range: {min(rot_lengths):.4f}..{max(rot_lengths):.4f} deg",
        f"- Outcome map: `{map_path.as_posix()}`",
        f"- Distribution graph: `{hist_path.as_posix()}`",
        "",
        "Lengths are read from raw `pathl.csv` rows and summarized per `testId/confId/branch` group only to avoid duplicate sample rows.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    records = read_groups(csv_path)

    map_path = out_dir / f"pathl_length_outcome_map_{args.suffix}.svg"
    hist_path = out_dir / f"pathl_length_outcome_hist_{args.suffix}.svg"
    summary_path = out_dir / f"pathl_length_overview_{args.suffix}.md"

    map_path.write_text(make_map_svg(csv_path.name, records), encoding="utf-8")
    hist_path.write_text(make_hist_svg(csv_path.name, records), encoding="utf-8")
    write_summary(summary_path, csv_path.name, records, map_path, hist_path)

    print(map_path)
    print(hist_path)
    print(summary_path)


if __name__ == "__main__":
    main()
