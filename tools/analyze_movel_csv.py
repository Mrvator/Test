#!/usr/bin/env python3
"""Generate a repeatable Markdown analysis for ABB MoveL/autohoming CSV logs."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Iterable


AXES = range(1, 7)
PATHL_SAMPLES_PER_BRANCH = 100
PATHL_ZERO_TOL = 1e-9
PATHL_UNUSED_RATIO_SENTINEL = 999.0
PATHL_PATH_LENGTH_BUCKETS = [
    (1.0, "<1"),
    (10.0, "<10"),
    (100.0, "<100"),
    (math.inf, ">=100"),
]
PATHL_ROT_LENGTH_BUCKETS = [
    (1.0, "<1"),
    (10.0, "<10"),
    (90.0, "<90"),
    (180.0, "<180"),
    (270.0, "<270"),
    (350.0, "<350"),
    (359.0, "<359"),
    (math.inf, ">=359"),
]
PATHL_PRECISION_METRICS = [
    "PathRatio error",
    "RotRatio error",
    "PathDist from PathRatio rows",
    "PathDist from RotRatio rows",
    "RotDist from PathRatio rows",
    "RotDist from RotRatio rows",
]

@dataclass(frozen=True)
class Delta:
    max_abs: float
    axis: int
    values: list[float]
    valid: bool


@dataclass(frozen=True)
class JumpMax:
    value: float
    test_id: str
    conf_id: str
    branch: str
    axis: int
    row: dict[str, str] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="CSV suffix, for example v15")
    parser.add_argument("--root", default=".", help="Folder with tests/success/pathl CSV files")
    parser.add_argument(
        "--config",
        default="config/movel_analysis_profile.json",
        help="Analysis profile JSON with tolerances",
    )
    parser.add_argument("--out", default=None, help="Output Markdown path")
    parser.add_argument(
        "--fail-on-maxwin2-limit",
        action="store_true",
        help="Return a non-zero exit code when legacy MaxWin2 exceeds the configured limit",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def csv_path(root: Path, stem: str, version: str) -> Path:
    return root / f"{stem}_{version}.csv"


def read_tests_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=";")
        header = next(reader)
        validate_tests_header(header, path)
        rows: list[dict[str, str]] = []
        for line_number, raw_row in enumerate(reader, start=2):
            if len(raw_row) != len(header):
                raise ValueError(
                    f"{path}: line {line_number} has {len(raw_row)} fields, "
                    f"but header has {len(header)} fields"
                )
            row = dict(zip(header, raw_row))
            rows.append(row)
        return rows


def validate_tests_header(header: list[str], path: Path) -> None:
    expected_order = [
        "stErrLong",
        "FinestStepS",
        "FinestStepL",
        "ControlShort_rax1",
        "ControlShort_rax2",
        "ControlShort_rax3",
        "ControlShort_rax4",
        "ControlShort_rax5",
        "ControlShort_rax6",
        "ControlLong_rax1",
        "ControlLong_rax2",
        "ControlLong_rax3",
        "ControlLong_rax4",
        "ControlLong_rax5",
        "ControlLong_rax6",
        "ControlShortMaxAx1",
    ]
    missing = [column for column in expected_order if column not in header]
    if missing:
        raise ValueError(f"{path}: tests CSV is missing required columns: {', '.join(missing)}")

    positions = [header.index(column) for column in expected_order]
    if positions != sorted(positions):
        raise ValueError(
            f"{path}: unexpected tests CSV column order after stErrLong; "
            "expected FinestStepS/L before ControlShort/ControlLong columns"
        )


def load_profile(path: Path) -> dict[str, float | int]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_float(value: str | None) -> float:
    if value is None or value == "":
        return math.nan
    try:
        return float(value)
    except ValueError:
        return math.nan


def as_bool(value: str | None) -> bool:
    return str(value).strip().upper() == "TRUE"


def as_upper(value: str | None) -> str:
    return str(value or "").strip().upper()


def joint_vector(row: dict[str, str], prefix: str) -> list[float]:
    return [as_float(row.get(f"{prefix}_rax{axis}")) for axis in AXES]


def is_valid_vector(values: Iterable[float], invalid_abs_min: float) -> bool:
    vals = list(values)
    return all(math.isfinite(v) and abs(v) < invalid_abs_min for v in vals)


def vector_delta(
    left: list[float], right: list[float], invalid_abs_min: float
) -> Delta:
    if not is_valid_vector(left, invalid_abs_min) or not is_valid_vector(right, invalid_abs_min):
        return Delta(math.nan, 0, [], False)
    values = [abs(a - b) for a, b in zip(left, right)]
    max_abs = max(values)
    return Delta(max_abs, values.index(max_abs) + 1, values, True)


def fmt_num(value: float) -> str:
    if not math.isfinite(value):
        return "n/a"
    if abs(value) >= 100:
        return f"{value:.3f}"
    if abs(value) >= 1:
        return f"{value:.4f}"
    return f"{value:.6f}"


def fmt_axis(axis: int) -> str:
    return f"Ax{axis}" if axis else "n/a"


def md_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    if not rows:
        return ["None."]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def stats_summary(values: Iterable[float]) -> dict[str, float | int]:
    finite = sorted(value for value in values if math.isfinite(value))
    if not finite:
        return {
            "n": 0,
            "min": math.nan,
            "mean": math.nan,
            "median": math.nan,
            "p95": math.nan,
            "max": math.nan,
        }
    p95_index = min(len(finite) - 1, math.ceil(len(finite) * 0.95) - 1)
    return {
        "n": len(finite),
        "min": finite[0],
        "mean": mean(finite),
        "median": median(finite),
        "p95": finite[p95_index],
        "max": finite[-1],
    }




def stats_row_full(label: str, values: Iterable[float]) -> list[object]:
    stats = stats_summary(values)
    return [
        label,
        stats["n"],
        fmt_num(float(stats["min"])),
        fmt_num(float(stats["mean"])),
        fmt_num(float(stats["median"])),
        fmt_num(float(stats["p95"])),
        fmt_num(float(stats["max"])),
    ]


def bucket_label(value: float, buckets: list[tuple[float, str]]) -> str:
    if not math.isfinite(value):
        return "n/a"
    for upper_bound, label in buckets:
        if value < upper_bound:
            return label
    return buckets[-1][1]


def add_metric(metrics: dict[str, list[float]], label: str, value: float) -> None:
    if math.isfinite(value):
        metrics[label].append(value)


def metric_bucket_rows(
    bucket_metrics: dict[str, dict[str, list[float]]],
    bucket_labels: Iterable[str],
) -> list[list[object]]:
    rows: list[list[object]] = []
    for bucket in bucket_labels:
        for metric in PATHL_PRECISION_METRICS:
            rows.append([bucket, *stats_row_full(metric, bucket_metrics[bucket][metric])])
    return rows


def is_unused_ratio_sentinel(value: float) -> bool:
    return math.isfinite(value) and abs(value - PATHL_UNUSED_RATIO_SENTINEL) <= PATHL_ZERO_TOL


def used_ratio_value(value: str | None) -> float:
    ratio = as_float(value)
    if math.isfinite(ratio) and abs(ratio - PATHL_UNUSED_RATIO_SENTINEL) <= PATHL_ZERO_TOL:
        return math.nan
    return ratio


def pathl_path_length(row: dict[str, str]) -> float:
    return as_float(row.get("PathLength") or row.get("PathLenght") or row.get("PathLenth"))


def pathl_rot_dist(row: dict[str, str]) -> float:
    return as_float(row.get("RotDist") or row.get("Rotdist"))


def test_path_length(row: dict[str, str]) -> float:
    return as_float(row.get("PathLength") or row.get("PathLenght") or row.get("PathLenth"))


def test_rot_length(row: dict[str, str]) -> float:
    return as_float(row.get("RotLength"))


def pathl_expected_ratio(row: dict[str, str], pair_index: int) -> float:
    expected_ratio = as_float(row.get("ExpectedRatio"))
    if math.isfinite(expected_ratio):
        return expected_ratio
    return (pair_index + 1) / PATHL_SAMPLES_PER_BRANCH






def legacy_max_ax_values(row: dict[str, str], branch: str) -> dict[int, float]:
    return {axis: branch_axis_jump(row, "", branch, axis) for axis in (1, 4, 6)}






def branch_conf_id(
    row: dict[str, str],
    branch: str,
    conf_ids_by_branch: dict[tuple[str, str], list[str]],
) -> str:
    conf_ids = conf_ids_by_branch.get((row.get("testId", ""), branch), [])
    return ",".join(conf_ids) if conf_ids else "n/a"


def jump_metric_values(row: dict[str, str] | None, branch: str, axis: int) -> list[str]:
    if row is None or branch not in ("S", "L") or axis not in (1, 4, 6):
        return ["n/a", "n/a", "n/a"]
    return [
        fmt_num(branch_axis_jump(row, "", branch, axis)),
        fmt_num(branch_win_jump(row, branch, "Win", axis)),
        fmt_num(branch_win_jump(row, branch, "Win2", axis)),
    ]


def legacy_max_ax_pooled_info(
    branch_rows: Iterable[tuple[dict[str, str], str]],
    conf_ids_by_branch: dict[tuple[str, str], list[str]],
) -> JumpMax:
    candidates: list[tuple[float, dict[str, str], str, int]] = [
        (value, row, branch, axis)
        for row, branch in branch_rows
        for axis, value in legacy_max_ax_values(row, branch).items()
        if math.isfinite(value)
    ]
    if not candidates:
        return JumpMax(math.nan, "n/a", "n/a", "n/a", 0)
    value, row, branch, axis = max(candidates, key=lambda item: item[0])
    return JumpMax(value, row.get("testId", ""), branch_conf_id(row, branch, conf_ids_by_branch), branch, axis, row)




def legacy_max_window_pairs(
    label: str,
    branch_rows: Iterable[tuple[dict[str, str], str]],
    window: str,
) -> list[tuple[str, float, dict[str, str], str, int, str]]:
    pairs: list[tuple[str, float, dict[str, str], str, int, str]] = []
    for row, branch in branch_rows:
        for axis in (1, 4, 6):
            column = f"{branch_name(branch)}Max{window}Ax{axis}"
            pairs.append((label, as_float(row.get(column)), row, branch, axis, column))
    return pairs




def legacy_window_pooled_info(
    pairs: Iterable[tuple[str, float, dict[str, str], str, int, str]],
    conf_ids_by_branch: dict[tuple[str, str], list[str]],
) -> JumpMax:
    finite_pairs = [pair for pair in pairs if math.isfinite(pair[1])]
    if not finite_pairs:
        return JumpMax(math.nan, "n/a", "n/a", "n/a", 0)
    _, value, row, branch, axis, _ = max(finite_pairs, key=lambda pair: pair[1])
    return JumpMax(value, row.get("testId", ""), branch_conf_id(row, branch, conf_ids_by_branch), branch, axis, row)


def aggregated_jump_summary_rows(
    successful_branch_rows: list[tuple[dict[str, str], str]],
    conf_ids_by_branch: dict[tuple[str, str], list[str]],
) -> list[list[object]]:
    successful_max_ax = legacy_max_ax_pooled_info(successful_branch_rows, conf_ids_by_branch)
    successful_max_win = legacy_window_pooled_info(
        legacy_max_window_pairs("successful", successful_branch_rows, "Win"),
        conf_ids_by_branch,
    )
    successful_max_win2 = legacy_window_pooled_info(
        legacy_max_window_pairs("successful", successful_branch_rows, "Win2"),
        conf_ids_by_branch,
    )

    rows: list[list[object]] = []
    for outcome, metric, jump_max in (
        ("Successful", "MaxAx", successful_max_ax),
        ("Successful", "MaxWin", successful_max_win),
        ("Successful", "MaxWin2", successful_max_win2),
    ):
        rows.append(
            [
                outcome,
                metric,
                fmt_num(jump_max.value),
                jump_max.test_id,
                jump_max.conf_id,
                jump_max.branch,
                fmt_axis(jump_max.axis),
                *jump_metric_values(jump_max.row, jump_max.branch, jump_max.axis),
            ]
        )
    return rows








def min_fmt(values: Iterable[float]) -> str:
    finite = [value for value in values if math.isfinite(value)]
    return fmt_num(min(finite)) if finite else "n/a"


def legacy_branch_metric_max(row: dict[str, str], branch: str, metric: str) -> tuple[float, int]:
    values: list[tuple[float, int]] = []
    for axis in (1, 4, 6):
        if metric == "MaxAx":
            value = branch_axis_jump(row, "", branch, axis)
        elif metric == "MaxWin2":
            value = branch_win_jump(row, branch, "Win2", axis)
        else:
            raise ValueError(f"unsupported branch metric: {metric}")
        if math.isfinite(value):
            values.append((value, axis))
    if not values:
        return math.nan, 0
    return max(values, key=lambda item: item[0])










def legacy_order_violation_rows(branch_rows: Iterable[tuple[dict[str, str], str]]) -> list[list[object]]:
    rows: list[list[object]] = []
    for row, branch in branch_rows:
        if not branch_ok(row, branch):
            continue
        for axis in (1, 4, 6):
            max_ax = branch_axis_jump(row, "", branch, axis)
            max_win = branch_win_jump(row, branch, "Win", axis)
            max_win2 = branch_win_jump(row, branch, "Win2", axis)
            if not all(math.isfinite(value) for value in (max_ax, max_win, max_win2)):
                continue
            if max_ax < max_win < max_win2:
                continue
            rows.append(
                [
                    row.get("testId", ""),
                    branch,
                    fmt_axis(axis),
                    fmt_num(max_ax),
                    fmt_num(max_win),
                    fmt_num(max_win2),
                    branch_ok(row, branch),
                    branch_status(row, branch)[1] or "empty",
                ]
            )
    return sorted(rows, key=lambda cells: (int(cells[0]) if str(cells[0]).isdigit() else 0, cells[1], cells[2]))


def movel_xy_records(
    success: Iterable[dict[str, str]],
    tests_by_id: dict[str, dict[str, str]],
    metric: str,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()

    for row in success:
        test_id = row.get("testId", "")
        test = tests_by_id.get(test_id)
        if not test:
            continue
        for branch, column in (("S", "MatchesShort"), ("L", "MatchesLong")):
            if not as_bool(row.get(column)):
                continue
            key = ("Successful", test_id, branch)
            if key in seen:
                continue
            seen.add(key)
            value, axis = legacy_branch_metric_max(test, branch, metric)
            path_length = test_path_length(test)
            rot_length = test_rot_length(test)
            if not math.isfinite(path_length) or not math.isfinite(rot_length) or not math.isfinite(value):
                continue
            records.append(
                {
                    "outcome": "Successful",
                    "testId": test_id,
                    "branch": branch,
                    "PathLength": path_length,
                    "RotLength": rot_length,
                    "PlotRotLength": 360.0 - rot_length if branch == "L" else rot_length,
                    "value": value,
                    "axis": axis,
                }
            )

    return records




def padded_extent(values: list[float], minimum_pad: float = 1.0) -> tuple[float, float]:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return 0.0, 1.0
    low = min(finite)
    high = max(finite)
    if low == high:
        pad = max(abs(low) * 0.05, minimum_pad)
    else:
        pad = max((high - low) * 0.05, minimum_pad)
    return low - pad, high + pad


def nice_svg_ticks(low: float, high: float, count: int = 5) -> list[float]:
    if low == high:
        return [low]
    span = high - low
    raw_step = span / max(count - 1, 1)
    power = 10 ** math.floor(math.log10(raw_step))
    step = min((1, 2, 5, 10), key=lambda value: abs(value * power - raw_step)) * power
    start = math.ceil(low / step) * step
    ticks: list[float] = []
    current = start
    while current <= high + step * 0.5:
        ticks.append(current)
        current += step
    return ticks


def color_scale(value: float, low: float, high: float) -> str:
    if not math.isfinite(value):
        return "#94a3b8"
    ratio = 0.5 if high <= low else max(0.0, min(1.0, (value - low) / (high - low)))
    stops = [(19, 120, 107), (245, 158, 11), (220, 38, 38)]
    if ratio <= 0.5:
        local = ratio * 2
        a, b = stops[0], stops[1]
    else:
        local = (ratio - 0.5) * 2
        a, b = stops[1], stops[2]
    red = round(a[0] + (b[0] - a[0]) * local)
    green = round(a[1] + (b[1] - a[1]) * local)
    blue = round(a[2] + (b[2] - a[2]) * local)
    return f"#{red:02x}{green:02x}{blue:02x}"


def make_movel_xy_svg(title: str, records: list[dict[str, object]], metric_label: str) -> str:
    width = 1220
    height = 560
    margin_left = 78
    margin_right = 44
    margin_top = 82
    margin_bottom = 118
    gap_x = 54
    gap_y = 0
    panel_width = (width - margin_left - margin_right - gap_x) / 2
    panel_height = height - margin_top - margin_bottom
    x_min, x_max = padded_extent([float(row["PathLength"]) for row in records])
    y_min, y_max = 0.0, 360.0
    finite_values = [float(row["value"]) for row in records if math.isfinite(float(row["value"]))]
    value_min = min(finite_values) if finite_values else 0.0
    value_max = max(finite_values) if finite_values else 1.0

    def panel_origin(index: int) -> tuple[float, float]:
        col = index % 2
        row = index // 2
        return margin_left + col * (panel_width + gap_x), margin_top + row * (panel_height + gap_y)

    def x_scale(value: float, left: float) -> float:
        return left + (value - x_min) / (x_max - x_min) * panel_width

    def y_scale(value: float, top: float) -> float:
        return top + panel_height - (value - y_min) / (y_max - y_min) * panel_height

    panel_defs = [
        ("Successful", "S", "Successful Short"),
        ("Successful", "L", "Successful Long"),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "svg{background:#f8fafc;color:#111827;font-family:Segoe UI,Arial,sans-serif}",
        ".title{font-size:24px;font-weight:700;fill:#111827}",
        ".subtitle,.legend{font-size:13px;fill:#4b5563}",
        ".legend-title{font-size:13px;font-weight:650;fill:#111827}",
        ".panel-title{font-size:15px;font-weight:700;fill:#111827}",
        ".plot-bg{fill:#ffffff;stroke:#d1d5db;stroke-width:1}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#374151;stroke-width:1.2}",
        ".tick{font-size:11px;fill:#4b5563}",
        ".axis-label{font-size:13px;font-weight:650;fill:#374151}",
        "</style>",
        f'<text x="{margin_left}" y="36" class="title">{html.escape(title)}</text>',
        f'<text x="{width - margin_right}" y="36" text-anchor="end" class="subtitle">n={len(records)} test/branch points</text>',
    ]

    for index, (outcome, branch, panel_title) in enumerate(panel_defs):
        left, top = panel_origin(index)
        bottom = top + panel_height
        right = left + panel_width
        panel_records = [
            row for row in records if row["outcome"] == outcome and row["branch"] == branch
        ]
        parts.append(
            f'<text x="{left}" y="{top - 18}" class="panel-title">{html.escape(panel_title)} ({len(panel_records)})</text>'
        )
        parts.append(f'<rect x="{left}" y="{top}" width="{panel_width}" height="{panel_height}" class="plot-bg"/>')
        for tick in (0.0, 90.0, 180.0, 270.0, 360.0):
            y = y_scale(tick, top)
            parts.append(f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" class="grid"/>')
            parts.append(f'<text x="{left - 10}" y="{y + 4:.2f}" text-anchor="end" class="tick">{fmt_num(tick)}</text>')
        for tick in nice_svg_ticks(x_min, x_max):
            x = x_scale(tick, left)
            parts.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{bottom}" class="grid"/>')
            parts.append(f'<text x="{x:.2f}" y="{bottom + 22}" text-anchor="middle" class="tick">{fmt_num(tick)}</text>')
        parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" class="axis"/>')
        parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="axis"/>')
        parts.append(f'<text x="{left + panel_width / 2}" y="{bottom + 48}" text-anchor="middle" class="axis-label">PathLength [mm]</text>')
        parts.append(
            f'<text x="{left - 54}" y="{top + panel_height / 2}" transform="rotate(-90 {left - 54} {top + panel_height / 2})" '
            f'text-anchor="middle" class="axis-label">RotLength [deg]</text>'
        )
        for row in panel_records:
            value = float(row["value"])
            axis = int(row["axis"]) if row["axis"] else 0
            tooltip = (
                f"testId={html.escape(str(row['testId']))}, branch={html.escape(str(row['branch']))}&#10;"
                f"outcome={html.escape(str(row['outcome']))}&#10;"
                f"PathLength={float(row['PathLength']):.6g} mm&#10;"
                f"RotLength={float(row['RotLength']):.6g} deg, plotted={float(row['PlotRotLength']):.6g} deg&#10;"
                f"{html.escape(metric_label)}={value:.6g}, axis={fmt_axis(axis)}"
            )
            parts.append(
                f'<circle cx="{x_scale(float(row["PathLength"]), left):.2f}" cy="{y_scale(float(row["PlotRotLength"]), top):.2f}" '
                f'r="4.0" fill="{color_scale(value, value_min, value_max)}" opacity="0.78" stroke="#111827" stroke-width="0.35">'
                f"<title>{tooltip}</title></circle>"
            )

    legend_x = margin_left
    legend_y = height - 72
    legend_width = 420
    legend_height = 14
    legend_segments = 70
    parts.append(f'<text x="{legend_x}" y="{legend_y - 14}" class="legend-title">{html.escape(metric_label)} color legend</text>')
    for index in range(legend_segments):
        ratio = index / max(legend_segments - 1, 1)
        value = value_min + (value_max - value_min) * ratio
        x = legend_x + legend_width * index / legend_segments
        segment_width = legend_width / legend_segments + 0.7
        parts.append(
            f'<rect x="{x:.2f}" y="{legend_y}" width="{segment_width:.2f}" height="{legend_height}" '
            f'fill="{color_scale(value, value_min, value_max)}"/>'
        )
    parts.append(
        f'<rect x="{legend_x}" y="{legend_y}" width="{legend_width}" height="{legend_height}" '
        f'fill="none" stroke="#374151" stroke-width="0.8"/>'
    )
    for ratio in (0.0, 0.25, 0.5, 0.75, 1.0):
        value = value_min + (value_max - value_min) * ratio
        x = legend_x + legend_width * ratio
        parts.append(f'<line x1="{x:.2f}" y1="{legend_y + legend_height}" x2="{x:.2f}" y2="{legend_y + legend_height + 5}" stroke="#374151" stroke-width="0.8"/>')
        parts.append(f'<text x="{x:.2f}" y="{legend_y + legend_height + 21}" text-anchor="middle" class="tick">{fmt_num(value)}</text>')
    parts.append(
        f'<text x="{legend_x + legend_width + 28}" y="{legend_y + 11}" class="legend">'
        "Long panels use 360 - RotLength.</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def branch_label(row: dict[str, str]) -> str:
    if as_bool(row.get("ControlMatchShort")):
        return "S"
    if as_bool(row.get("ControlMatchLong")):
        return "L"
    return "none"


def legacy_branch_label(row: dict[str, str]) -> str:
    if as_bool(row.get("MatchesShort")):
        return "S"
    if as_bool(row.get("MatchesLong")):
        return "L"
    return "none"


def legacy_matched_branches(row: dict[str, str]) -> list[str]:
    branches: list[str] = []
    if as_bool(row.get("MatchesShort")):
        branches.append("S")
    if as_bool(row.get("MatchesLong")):
        branches.append("L")
    return branches


def branch_name(branch: str) -> str:
    return "Short" if branch == "S" else "Long"


def branch_ok(row: dict[str, str], branch: str) -> bool:
    return as_bool(row.get("bOKshort" if branch == "S" else "bOKlong"))






def branch_axis_jump(row: dict[str, str], family: str, branch: str, axis: int) -> float:
    return as_float(row.get(f"{family}{branch_name(branch)}MaxAx{axis}"))


def branch_win_jump(row: dict[str, str], branch: str, window: str, axis: int) -> float:
    return as_float(row.get(f"{branch_name(branch)}Max{window}Ax{axis}"))


def branch_finest(row: dict[str, str], branch: str) -> float:
    column = "FinestStepS" if branch == "S" else "FinestStepL"
    return as_float(row.get(column))




def branch_status(row: dict[str, str], branch: str) -> tuple[bool, str]:
    if branch == "S":
        return as_bool(row.get("bOKshort")), as_upper(row.get("stErrShort"))
    return as_bool(row.get("bOKlong")), as_upper(row.get("stErrLong"))












def main() -> int:
    args = parse_args()
    root = Path(args.root)
    version = args.version
    profile = load_profile(root / args.config)
    joint_tol = float(profile["joint_abs_tolerance_deg"])
    legacy_max_win2_limit = float(profile["legacy_max_win2_limit_deg"])
    invalid_abs_min = float(profile["invalid_joint_abs_min"])
    max_rows = int(profile["max_anomaly_rows"])

    tests_path = csv_path(root, "tests", version)
    success_path = csv_path(root, "success", version)
    pathl_path = csv_path(root, "pathl", version)
    tests = read_tests_csv(tests_path)
    success = read_csv(success_path)
    pathl = read_csv(pathl_path)

    test_path_length_stats = stats_summary(test_path_length(row) for row in tests)
    test_rot_length_stats = stats_summary(test_rot_length(row) for row in tests)
    test_finest_step_stats = stats_summary(
        branch_finest(row, branch)
        for row in tests
        for branch in ("S", "L")
    )

    tests_by_id = {row["testId"]: row for row in tests}
    success_by_test: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in success:
        success_by_test[row["testId"]].append(row)
    missing_success = sorted(set(tests_by_id) - set(success_by_test), key=lambda value: int(value))

    successful_legacy_branch_keys = {
        (row["testId"], branch)
        for row in success
        for branch in legacy_matched_branches(row)
    }
    conf_id_sets_by_branch: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in success:
        for branch in legacy_matched_branches(row):
            conf_id_sets_by_branch[(row["testId"], branch)].add(row.get("confId", ""))
    conf_ids_by_branch = {
        key: sorted(values, key=lambda value: (not value.isdigit(), int(value) if value.isdigit() else value))
        for key, values in conf_id_sets_by_branch.items()
    }

    max_deltas = Counter()
    branch_compare = Counter()
    xor_rows: list[list[object]] = []
    legacy_xor_rows: list[list[object]] = []
    control_xor_violation_keys: set[tuple[str, str]] = set()

    for row in success:
        test_id = row["testId"]
        conf_id = row.get("confId", "")
        c = joint_vector(row, "C")
        calc = joint_vector(row, "CalcC")
        path = joint_vector(row, "PathL")
        for name, delta in (
            ("C vs CalcC", vector_delta(c, calc, invalid_abs_min)),
            ("C vs PathL", vector_delta(c, path, invalid_abs_min)),
        ):
            if not delta.valid or delta.max_abs > joint_tol:
                max_deltas[name] += 1

        control_short = as_bool(row.get("ControlMatchShort"))
        control_long = as_bool(row.get("ControlMatchLong"))
        if control_short == control_long:
            control_xor_violation_keys.add((test_id, conf_id))
            xor_rows.append([test_id, conf_id, control_short, control_long])

        legacy_short = as_bool(row.get("MatchesShort"))
        legacy_long = as_bool(row.get("MatchesLong"))
        if legacy_short == legacy_long:
            legacy_xor_rows.append([test_id, conf_id, legacy_short, legacy_long])

        branch_compare[(branch_label(row), legacy_branch_label(row))] += 1

    legacy_branch_samples = [
        {"branch": branch, "successful": (row["testId"], branch) in successful_legacy_branch_keys, "row": row}
        for row in tests
        for branch in ("S", "L")
    ]
    successful_legacy_branch_rows = [
        (sample["row"], str(sample["branch"]))
        for sample in legacy_branch_samples
        if sample["successful"]
    ]
    successful_legacy_branch_rows_by_branch = {
        branch: [(row, row_branch) for row, row_branch in successful_legacy_branch_rows if row_branch == branch]
        for branch in ("S", "L")
    }
    aggregated_jump_summary_by_branch = {
        branch: aggregated_jump_summary_rows(
            successful_legacy_branch_rows_by_branch[branch],
            conf_ids_by_branch,
        )
        for branch in ("S", "L")
    }
    legacy_max_win2_violation_count = sum(
        1
        for row, branch in successful_legacy_branch_rows
        for axis in (1, 4, 6)
        if branch_win_jump(row, branch, "Win2", axis) > legacy_max_win2_limit
    )

    path_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    pathl_precision_values: dict[str, list[float]] = defaultdict(list)
    pathl_precision_by_path_bucket: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    pathl_precision_by_rot_bucket: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in pathl:
        path_groups[(row.get("testId", ""), row.get("confId", ""))].append(row)

    pathl_bad_group_count = 0
    pathl_bad_pair_count = 0
    pathl_row_count_distribution = Counter(len(rows) for rows in path_groups.values())
    common_rows_per_group = (
        pathl_row_count_distribution.most_common(1)[0][0] if pathl_row_count_distribution else 0
    )
    pathl_row_count_consistent = len(pathl_row_count_distribution) <= 1
    pathl_row_count_even = all(row_count % 2 == 0 for row_count in pathl_row_count_distribution)

    for (test_id, conf_id), rows in sorted(
        path_groups.items(), key=lambda item: (int(item[0][0] or 0), int(item[0][1] or 0))
    ):
        if (not pathl_row_count_consistent and len(rows) != common_rows_per_group) or len(rows) % 2:
            pathl_bad_group_count += 1

        for pair_index in range(len(rows) // 2):
            path_row = rows[pair_index * 2]
            rot_row = rows[pair_index * 2 + 1]
            path_expected_ratio = pathl_expected_ratio(path_row, pair_index)
            rot_expected_ratio = pathl_expected_ratio(rot_row, pair_index)

            path_ratio = used_ratio_value(path_row.get("RatioPath"))
            path_ratio_rot_column = as_float(path_row.get("RatioRot"))
            rot_ratio_path_column = as_float(rot_row.get("RatioPath"))
            rot_ratio = used_ratio_value(rot_row.get("RatioRot"))
            path_expected_diff = abs(path_ratio - path_expected_ratio)
            rot_expected_diff = abs(rot_ratio - rot_expected_ratio)
            path_length = pathl_path_length(path_row)
            rot_length = as_float(path_row.get("RotLength"))
            path_bucket = bucket_label(path_length, PATHL_PATH_LENGTH_BUCKETS)
            rot_bucket = bucket_label(rot_length, PATHL_ROT_LENGTH_BUCKETS)
            metric_values = {
                "PathRatio error": path_expected_diff,
                "RotRatio error": rot_expected_diff,
                "PathDist from PathRatio rows": as_float(path_row.get("PathDist")),
                "PathDist from RotRatio rows": as_float(rot_row.get("PathDist")),
                "RotDist from PathRatio rows": pathl_rot_dist(path_row),
                "RotDist from RotRatio rows": pathl_rot_dist(rot_row),
            }
            for metric, value in metric_values.items():
                add_metric(pathl_precision_values, metric, value)
                add_metric(pathl_precision_by_path_bucket[path_bucket], metric, value)
                add_metric(pathl_precision_by_rot_bucket[rot_bucket], metric, value)

            problems = [
                not math.isfinite(path_ratio),
                not math.isfinite(rot_ratio),
                math.isfinite(path_ratio) and not (0.0 <= path_ratio <= 1.0),
                math.isfinite(rot_ratio) and not (0.0 <= rot_ratio <= 1.0),
                not is_unused_ratio_sentinel(path_ratio_rot_column),
                not is_unused_ratio_sentinel(rot_ratio_path_column),
            ]
            if any(problems):
                pathl_bad_pair_count += 1

    pathl_pairing_status = (
        "OK"
        if pathl_row_count_consistent and pathl_row_count_even and pathl_bad_pair_count == 0
        else "FAIL"
    )
    pathl_pairing_rows_text = (
        f"{common_rows_per_group} rows per group"
        if pathl_row_count_consistent and path_groups
        else "row counts " + (
            ", ".join(
                f"{row_count} rows: {group_count} groups"
                for row_count, group_count in sorted(pathl_row_count_distribution.items())
            ) or "no groups"
        )
    )
    pathl_pairing_sentence = (
        f"PathL pairing check: {pathl_pairing_status}, {len(path_groups)} testId/confId groups, "
        f"{pathl_pairing_rows_text}, {pathl_bad_group_count} row count issues, "
        f"{pathl_bad_pair_count} pair issues."
    )
    pathl_precision_stat_headers = ["metric", "n", "min", "mean", "median", "p95", "max"]
    pathl_ratio_precision_rows = [
        stats_row_full("PathRatio error", pathl_precision_values["PathRatio error"]),
        stats_row_full("RotRatio error", pathl_precision_values["RotRatio error"]),
    ]
    pathl_distance_precision_rows = [
        stats_row_full(metric, pathl_precision_values[metric])
        for metric in PATHL_PRECISION_METRICS[2:]
    ]
    pathl_path_bucket_labels = [label for _, label in PATHL_PATH_LENGTH_BUCKETS]
    pathl_rot_bucket_labels = [label for _, label in PATHL_ROT_LENGTH_BUCKETS]
    pathl_bucket_headers = ["bucket", *pathl_precision_stat_headers]

    no_success_tests = [tests_by_id[test_id] for test_id in missing_success if test_id in tests_by_id]
    count_table_rows = [
        [
            "Successful",
            sum(1 for row in success if as_bool(row.get("ControlMatchShort"))),
            sum(1 for row in success if as_bool(row.get("ControlMatchLong"))),
        ],
        [
            "No success.csv record",
            sum(1 for row in no_success_tests if branch_ok(row, "S")),
            sum(1 for row in no_success_tests if branch_ok(row, "L")),
        ],
    ]
    finest_step_table_rows = [
        [
            "Successful",
            min_fmt(
                branch_finest(tests_by_id[row["testId"]], "S")
                for row in success
                if as_bool(row.get("ControlMatchShort")) and row.get("testId", "") in tests_by_id
            ),
            min_fmt(
                branch_finest(tests_by_id[row["testId"]], "L")
                for row in success
                if as_bool(row.get("ControlMatchLong")) and row.get("testId", "") in tests_by_id
            ),
        ],
        [
            "No success.csv record",
            min_fmt(branch_finest(row, "S") for row in no_success_tests if branch_ok(row, "S")),
            min_fmt(branch_finest(row, "L") for row in no_success_tests if branch_ok(row, "L")),
        ],
    ]
    order_violation_rows_by_branch = {
        branch: legacy_order_violation_rows(successful_legacy_branch_rows_by_branch[branch])
        for branch in ("S", "L")
    }

    report_dir = root / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    xy_maxax_path = report_dir / f"movel_xy_maxax_{version}.svg"
    xy_maxwin2_path = report_dir / f"movel_xy_maxwin2_{version}.svg"
    xy_maxax_records = movel_xy_records(success, tests_by_id, "MaxAx")
    xy_maxwin2_records = movel_xy_records(success, tests_by_id, "MaxWin2")
    xy_maxax_path.write_text(
        make_movel_xy_svg(
            f"MoveL XY Legacy MaxAx {version}",
            xy_maxax_records,
            "Legacy MaxAx",
        ),
        encoding="utf-8",
    )
    xy_maxwin2_path.write_text(
        make_movel_xy_svg(
            f"MoveL XY Legacy MaxWin2 {version}",
            xy_maxwin2_records,
            "Legacy MaxWin2",
        ),
        encoding="utf-8",
    )

    lines = [
        f"# ABB MoveL Analysis {version}",
        "",
        "## Header Resume",
        "",
        f"- Tests: {len(tests)}",
        f"- Successful runs: {len(success)}",
        f"- PathLength min/max: {fmt_num(float(test_path_length_stats['min']))}..{fmt_num(float(test_path_length_stats['max']))} mm",
        f"- RotLength min/max: {fmt_num(float(test_rot_length_stats['min']))}..{fmt_num(float(test_rot_length_stats['max']))} deg",
        f"- Highest FinestStep in all test data: {fmt_num(float(test_finest_step_stats['max']))} (FinestStepS/L, n={test_finest_step_stats['n']})",
        f"- Successful runs where C_rax differs from CalcC_rax by > {fmt_num(joint_tol)} deg on any axis: {max_deltas['C vs CalcC']}",
        f"- Successful runs where C_rax differs from PathL_rax by > {fmt_num(joint_tol)} deg on any axis: {max_deltas['C vs PathL']}",
        f"- Successful runs where ControlMatchShort XOR ControlMatchLong is false: {len(control_xor_violation_keys)}",
        f"- Successful runs where MatchesShort XOR MatchesLong is false: {len(legacy_xor_rows)}",
        "",
        "## Legacy XOR Violations",
        "",
    ]
    lines.extend(md_table(["testId", "confId", "MatchesShort", "MatchesLong"], legacy_xor_rows[:max_rows]))
    if len(legacy_xor_rows) > max_rows:
        lines.append(f"... {len(legacy_xor_rows) - max_rows} more omitted by report limit.")

    lines.extend(["", "## Control XOR Violations", ""])
    lines.extend(md_table(["testId", "confId", "ControlMatchShort", "ControlMatchLong"], xor_rows[:max_rows]))
    if len(xor_rows) > max_rows:
        lines.append(f"... {len(xor_rows) - max_rows} more omitted by report limit.")

    lines.extend(["", "## Legacy vs Control Branch Comparison", ""])
    lines.extend(
        md_table(
            ["control", "legacy", "rows"],
            [[control, legacy, count] for (control, legacy), count in sorted(branch_compare.items())],
        )
    )

    lines.extend(["", "## Table 1 - Successful vs No Success Branch Counts", ""])
    lines.extend(md_table(["outcome", "Short", "Long"], count_table_rows))

    lines.extend(
        [
            "",
            "## Table 2 - Aggregated Jump Summary",
            "",
            "Legacy max-jump statistics are reported only for successful branches where the corresponding `MatchesShort` or `MatchesLong` value is true.",
            "",
        ]
    )
    aggregated_jump_summary_headers = [
        "outcome",
        "metric",
        "value",
        "testId",
        "confId",
        "branch",
        "axis",
        "row MaxAx",
        "row MaxWin",
        "row MaxWin2",
    ]
    for branch, title in (("S", "Short branches"), ("L", "Long branches")):
        lines.extend(["", f"### {title}", ""])
        lines.extend(md_table(aggregated_jump_summary_headers, aggregated_jump_summary_by_branch[branch]))

    lines.extend(["", "## Table 3 - Minimum FinestStep", ""])
    lines.extend(md_table(["outcome", "Short", "Long"], finest_step_table_rows))

    lines.extend(["", "## Successful MaxAx < MaxWin < MaxWin2 Violations", ""])
    for branch, title in (("S", "Short"), ("L", "Long")):
        rows = order_violation_rows_by_branch[branch]
        lines.extend(["", f"### {title}", "", f"- Violations: {len(rows)}", ""])
        lines.extend(
            md_table(
                ["testId", "branch", "axis", "MaxAx", "MaxWin", "MaxWin2", "bOK", "stErr"],
                rows,
            )
        )

    lines.extend(
        [
            "",
            "## XY Graphs",
            "",
            f"- Legacy MaxAx: `{xy_maxax_path.as_posix()}`",
            f"- Legacy MaxWin2: `{xy_maxwin2_path.as_posix()}`",
            "",
            "Each SVG has two panels: Successful Short and Successful Long. A branch is included only when the corresponding `MatchesShort` or `MatchesLong` value is true. Long panels plot `360 - RotLength`.",
            "",
            "## PathL Ratio Analysis",
            "",
            f"- {pathl_pairing_sentence}",
            "",
            "### Ratio Precision",
            "",
        ]
    )
    lines.extend(md_table(pathl_precision_stat_headers, pathl_ratio_precision_rows))
    lines.extend(["", "### Distance Precision", ""])
    lines.extend(md_table(pathl_precision_stat_headers, pathl_distance_precision_rows))
    lines.extend(["", "### PathLength Bucket Precision", ""])
    lines.extend(
        md_table(
            pathl_bucket_headers,
            metric_bucket_rows(pathl_precision_by_path_bucket, pathl_path_bucket_labels),
        )
    )
    lines.extend(["", "### RotLength Bucket Precision", ""])
    lines.extend(
        md_table(
            pathl_bucket_headers,
            metric_bucket_rows(pathl_precision_by_rot_bucket, pathl_rot_bucket_labels),
        )
    )

    out_path = Path(args.out) if args.out else root / "reports" / f"movel_analysis_{version}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    if args.fail_on_maxwin2_limit and legacy_max_win2_violation_count:
        print(
            f"legacy MaxWin2 limit exceeded: {legacy_max_win2_violation_count} values > "
            f"{fmt_num(legacy_max_win2_limit)} deg"
        )
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
