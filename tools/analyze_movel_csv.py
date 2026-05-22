#!/usr/bin/env python3
"""Generate a repeatable Markdown analysis for ABB MoveL/autohoming CSV logs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Iterable


AXES = range(1, 7)
PATHL_SAMPLES_PER_BRANCH = 100
PATHL_EXPECTED_ROWS_PER_BRANCH = PATHL_SAMPLES_PER_BRANCH * 2
PATHL_RATIO_TOL = 0.006
PATHL_ZERO_TOL = 1e-9
PATHL_UNUSED_RATIO_SENTINEL = 999.0
PATHL_RATIO_EXAMPLE_LIMIT = 5
PATHL_SHORT_GROUP_LIMIT = 10
PATHL_RATIO_EXAMPLE_PROBLEMS = [
    "RatioPath not increasing",
    "RatioPath outside 0..1",
    "odd row is not PathRatio",
    "RatioRot outside 0..1",
]


@dataclass(frozen=True)
class Delta:
    max_abs: float
    axis: int
    values: list[float]
    valid: bool


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

    start = header.index("stErrLong")
    actual = header[start : start + len(expected_order)]
    if actual != expected_order:
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


def stats_row(label: str, values: Iterable[float]) -> list[object]:
    stats = stats_summary(values)
    return [
        label,
        stats["n"],
        fmt_num(float(stats["mean"])),
        fmt_num(float(stats["median"])),
        fmt_num(float(stats["p95"])),
        fmt_num(float(stats["max"])),
    ]


def is_unused_ratio_marker(value: float) -> bool:
    return math.isfinite(value) and (
        abs(value) <= PATHL_ZERO_TOL or abs(value - PATHL_UNUSED_RATIO_SENTINEL) <= PATHL_ZERO_TOL
    )


def used_ratio_value(value: str | None) -> float:
    ratio = as_float(value)
    if math.isfinite(ratio) and abs(ratio - PATHL_UNUSED_RATIO_SENTINEL) <= PATHL_ZERO_TOL:
        return math.nan
    return ratio


def pathl_short_group_stats_row(test_id: str, conf_id: str, branch: str, rows: list[dict[str, str]]) -> list[object]:
    if not rows:
        return []

    path_length = as_float(rows[0].get("PathLenth"))
    rot_length = as_float(rows[0].get("RotLength"))
    path_ratio_diffs: list[float] = []
    rot_ratio_diffs: list[float] = []

    for pair_index in range(len(rows) // 2):
        path_row = rows[pair_index * 2]
        rot_row = rows[pair_index * 2 + 1]
        expected_ratio = (pair_index + 1) / PATHL_SAMPLES_PER_BRANCH
        path_ratio = used_ratio_value(path_row.get("RatioPath"))
        rot_ratio = used_ratio_value(rot_row.get("RatioRot"))
        path_ratio_diffs.append(abs(path_ratio - expected_ratio))
        rot_ratio_diffs.append(abs(rot_ratio - expected_ratio))

    path_diff_stats = stats_summary(path_ratio_diffs)
    rot_diff_stats = stats_summary(rot_ratio_diffs)

    return [
        test_id,
        conf_id,
        branch,
        fmt_num(path_length),
        fmt_num(rot_length),
        path_diff_stats["n"],
        fmt_num(float(path_diff_stats["min"])),
        fmt_num(float(path_diff_stats["mean"])),
        fmt_num(float(path_diff_stats["median"])),
        fmt_num(float(path_diff_stats["p95"])),
        fmt_num(float(path_diff_stats["max"])),
        rot_diff_stats["n"],
        fmt_num(float(rot_diff_stats["min"])),
        fmt_num(float(rot_diff_stats["mean"])),
        fmt_num(float(rot_diff_stats["median"])),
        fmt_num(float(rot_diff_stats["p95"])),
        fmt_num(float(rot_diff_stats["max"])),
    ]


def legacy_max_ax_values(row: dict[str, str], branch: str) -> dict[int, float]:
    return {axis: branch_axis_jump(row, "", branch, axis) for axis in (1, 4, 6)}


def legacy_max_ax_row_value(row: dict[str, str], branch: str) -> tuple[float, int]:
    values = legacy_max_ax_values(row, branch)
    finite = [(value, axis) for axis, value in values.items() if math.isfinite(value)]
    if not finite:
        return math.nan, 0
    value, axis = max(finite, key=lambda item: item[0])
    return value, axis


def legacy_max_ax_boundary_row(label: str, branch_rows: Iterable[tuple[dict[str, str], str]]) -> list[object]:
    pairs: list[tuple[float, dict[str, str], str, int]] = []
    for row, branch in branch_rows:
        pairs.extend(
            (value, row, branch, axis)
            for axis, value in legacy_max_ax_values(row, branch).items()
        )

    values = [value for value, _, _, _ in pairs]
    stats = stats_summary(values)
    finite_pairs = [(value, row, branch, axis) for value, row, branch, axis in pairs if math.isfinite(value)]
    test_id_at_max = "n/a"
    branch_at_max = "n/a"
    axis_at_max: int | str = "n/a"
    max_ax_values = {1: math.nan, 4: math.nan, 6: math.nan}
    if finite_pairs:
        _, row_at_max, branch_at_max, axis_at_max = max(finite_pairs, key=lambda pair: pair[0])
        test_id_at_max = row_at_max.get("testId", "")
        max_ax_values = legacy_max_ax_values(row_at_max, branch_at_max)
    return [
        label,
        stats["n"],
        fmt_num(float(stats["mean"])),
        fmt_num(float(stats["median"])),
        fmt_num(float(stats["p95"])),
        fmt_num(float(stats["max"])),
        test_id_at_max,
        branch_at_max,
        f"Ax{axis_at_max}" if isinstance(axis_at_max, int) else axis_at_max,
        fmt_num(max_ax_values[1]),
        fmt_num(max_ax_values[4]),
        fmt_num(max_ax_values[6]),
    ]


def finest_step_stats_row(label: str, rows: Iterable[dict[str, str]], branch: str) -> list[object]:
    stats = stats_summary(branch_finest(row, branch) for row in rows)
    return [
        label,
        stats["n"],
        fmt_num(float(stats["min"])),
        fmt_num(float(stats["mean"])),
        fmt_num(float(stats["median"])),
        fmt_num(float(stats["p95"])),
        fmt_num(float(stats["max"])),
    ]


def jump_stats_row(label: str, rows: Iterable[dict[str, str]], branch: str, axis: int) -> list[object]:
    pairs = [
        (branch_axis_jump(row, "Control", branch, axis), branch_finest(row, branch))
        for row in rows
    ]
    values = [value for value, _ in pairs]
    stats = stats_summary(values)
    finite_pairs = [(value, finest) for value, finest in pairs if math.isfinite(value)]
    finest_at_max = math.nan
    if finite_pairs:
        _, finest_at_max = max(finite_pairs, key=lambda pair: pair[0])
    return [
        label,
        stats["n"],
        fmt_num(float(stats["mean"])),
        fmt_num(float(stats["median"])),
        fmt_num(float(stats["p95"])),
        fmt_num(float(stats["max"])),
        fmt_num(finest_at_max),
    ]


def pearson(xs: list[float], ys: list[float]) -> float:
    pairs = [(x, y) for x, y in zip(xs, ys) if math.isfinite(x) and math.isfinite(y)]
    if len(pairs) < 2:
        return math.nan
    px = [x for x, _ in pairs]
    py = [y for _, y in pairs]
    mx = mean(px)
    my = mean(py)
    cov = sum((x - mx) * (y - my) for x, y in pairs)
    sx = math.sqrt(sum((x - mx) ** 2 for x in px))
    sy = math.sqrt(sum((y - my) ** 2 for y in py))
    if sx == 0 or sy == 0:
        return math.nan
    return cov / (sx * sy)


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


def branch_name(branch: str) -> str:
    return "Short" if branch == "S" else "Long"


def branch_ok(row: dict[str, str], branch: str) -> bool:
    return as_bool(row.get("bOKshort" if branch == "S" else "bOKlong"))


def branch_vector(row: dict[str, str], family: str, branch: str) -> list[float]:
    return joint_vector(row, f"{family}{branch_name(branch)}")


def branch_jump(row: dict[str, str], branch: str) -> float:
    prefix = "ControlShortMaxAx" if branch == "S" else "ControlLongMaxAx"
    columns = [f"{prefix}{axis}" for axis in (1, 4, 6)]
    values = [as_float(row.get(column)) for column in columns]
    finite = [value for value in values if math.isfinite(value)]
    return max(finite) if finite else math.nan


def branch_axis_jump(row: dict[str, str], family: str, branch: str, axis: int) -> float:
    return as_float(row.get(f"{family}{branch_name(branch)}MaxAx{axis}"))


def branch_win_jump(row: dict[str, str], branch: str, window: str, axis: int) -> float:
    return as_float(row.get(f"{branch_name(branch)}Max{window}Ax{axis}"))


def branch_finest(row: dict[str, str], branch: str) -> float:
    column = "FinestStepS" if branch == "S" else "FinestStepL"
    return as_float(row.get(column))


def pathl_finest_step(row: dict[str, str], tests_by_id: dict[str, dict[str, str]]) -> float:
    test = tests_by_id.get(row.get("testId", ""))
    if not test:
        return math.nan
    branch = row.get("branch S/L", "")
    if branch not in ("S", "L"):
        return math.nan
    return branch_finest(test, branch)


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
    finest_step_limit = float(profile["finest_step_limit"])
    max_joint_jump_deg = float(profile["max_joint_jump_deg"])
    path_warn = float(profile["path_distance_warn_mm"])
    rot_warn = float(profile["rotation_distance_warn_deg"])
    invalid_abs_min = float(profile["invalid_joint_abs_min"])
    max_rows = int(profile["max_anomaly_rows"])

    tests_path = csv_path(root, "tests", version)
    success_path = csv_path(root, "success", version)
    pathl_path = csv_path(root, "pathl", version)
    tests = read_tests_csv(tests_path)
    success = read_csv(success_path)
    pathl = read_csv(pathl_path)

    tests_by_id = {row["testId"]: row for row in tests}
    success_by_test: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in success:
        success_by_test[row["testId"]].append(row)

    missing_success = sorted(set(tests_by_id) - set(success_by_test), key=lambda x: int(x))

    successful_branch_keys = {
        (row["testId"], branch_label(row)) for row in success if branch_label(row) in ("S", "L")
    }

    found_branch_counts = Counter()
    unsuccessful_found_counts = Counter()
    for row in tests:
        test_id = row["testId"]
        for branch in ("S", "L"):
            if not branch_ok(row, branch):
                continue
            found_branch_counts[branch] += 1
            if (test_id, branch) not in successful_branch_keys:
                unsuccessful_found_counts[branch] += 1

    unsuccessful_found_stats: list[list[object]] = []
    for branch in ("S", "L"):
        rows = [
            row
            for row in tests
            if branch_ok(row, branch) and (row["testId"], branch) not in successful_branch_keys
        ]
        finest_stats = stats_summary(branch_finest(row, branch) for row in rows)
        jump_stats = stats_summary(branch_jump(row, branch) for row in rows)
        found_count = found_branch_counts[branch]
        unsuccessful_count = unsuccessful_found_counts[branch]
        unsuccessful_pct = (unsuccessful_count / found_count * 100.0) if found_count else math.nan
        unsuccessful_found_stats.append(
            [
                branch,
                found_count,
                unsuccessful_count,
                fmt_num(unsuccessful_pct),
                fmt_num(float(finest_stats["median"])),
                fmt_num(float(finest_stats["p95"])),
                fmt_num(float(finest_stats["max"])),
                fmt_num(float(jump_stats["median"])),
                fmt_num(float(jump_stats["p95"])),
                fmt_num(float(jump_stats["max"])),
            ]
        )

    mismatch_rows: list[list[object]] = []
    control_rows: list[list[object]] = []
    legacy_rows: list[list[object]] = []
    xor_rows: list[list[object]] = []
    max_deltas = Counter()
    control_mismatches = Counter()
    legacy_mismatches = Counter()
    branch_compare = Counter()
    worst_delta = ("", "", Delta(0.0, 0, [], True))

    for row in success:
        test_id = row["testId"]
        conf_id = row.get("confId", "")
        c = joint_vector(row, "C")
        calc = joint_vector(row, "CalcC")
        path = joint_vector(row, "PathL")
        comparisons = [
            ("C vs CalcC", vector_delta(c, calc, invalid_abs_min)),
            ("C vs PathL", vector_delta(c, path, invalid_abs_min)),
            ("CalcC vs PathL", vector_delta(calc, path, invalid_abs_min)),
        ]
        for name, delta in comparisons:
            if delta.valid and delta.max_abs > worst_delta[2].max_abs:
                worst_delta = (test_id, name, delta)
            if not delta.valid or delta.max_abs > joint_tol:
                max_deltas[name] += 1
                mismatch_rows.append(
                    [
                        test_id,
                        conf_id,
                        name,
                        fmt_num(delta.max_abs),
                        delta.axis or "n/a",
                        branch_label(row),
                    ]
                )

        test = tests_by_id.get(test_id)
        control_short = as_bool(row.get("ControlMatchShort"))
        control_long = as_bool(row.get("ControlMatchLong"))
        if control_short == control_long:
            xor_rows.append([test_id, conf_id, control_short, control_long])

        control_selected = branch_label(row)
        legacy_selected = legacy_branch_label(row)
        branch_compare[(control_selected, legacy_selected)] += 1
        if test:
            if control_selected in ("S", "L"):
                control_delta = vector_delta(
                    c, branch_vector(test, "Control", control_selected), invalid_abs_min
                )
                if not control_delta.valid or control_delta.max_abs > joint_tol:
                    control_mismatches[control_selected] += 1
                    control_rows.append(
                        [
                            test_id,
                            conf_id,
                            control_selected,
                            f"Control{branch_name(control_selected)}",
                            fmt_num(control_delta.max_abs),
                            control_delta.axis or "n/a",
                        ]
                    )
            if legacy_selected in ("S", "L"):
                legacy_delta = vector_delta(
                    c, branch_vector(test, "Lift", legacy_selected), invalid_abs_min
                )
                if not legacy_delta.valid or legacy_delta.max_abs > joint_tol:
                    legacy_mismatches[legacy_selected] += 1
                    legacy_rows.append(
                        [
                            test_id,
                            conf_id,
                            legacy_selected,
                            f"Lift{branch_name(legacy_selected)}",
                            fmt_num(legacy_delta.max_abs),
                            legacy_delta.axis or "n/a",
                        ]
                    )

    branch_samples: list[dict[str, object]] = []
    correlation_rows: list[list[object]] = []
    for row in tests:
        test_id = row["testId"]
        for branch in ("S", "L"):
            successful = (test_id, branch) in successful_branch_keys
            branch_samples.append({"branch": branch, "successful": successful, "row": row})

    finest_step_rows: list[list[object]] = []
    for branch in ("S", "L"):
        successful_rows = [
            sample["row"]
            for sample in branch_samples
            if sample["branch"] == branch and sample["successful"]
        ]
        found_unsuccessful_rows = [
            sample["row"]
            for sample in branch_samples
            if sample["branch"] == branch
            and not sample["successful"]
            and branch_ok(sample["row"], branch)
        ]
        finest_step_rows.append(finest_step_stats_row(f"{branch} successful", successful_rows, branch))
        finest_step_rows.append(
            finest_step_stats_row(f"{branch} found unsuccessful", found_unsuccessful_rows, branch)
        )

    jump_rows: list[list[object]] = []
    for branch in ("S", "L"):
        for successful, label in ((True, "successful"), (False, "unsuccessful")):
            matching_rows = [
                sample["row"]
                for sample in branch_samples
                if sample["branch"] == branch and sample["successful"] == successful
            ]
            for axis in (1, 4, 6):
                jump_rows.append(
                    jump_stats_row(f"{branch} ControlMaxAx{axis} {label}", matching_rows, branch, axis)
                )

    successful_branch_rows = [
        (sample["row"], str(sample["branch"]))
        for sample in branch_samples
        if sample["successful"]
    ]
    found_unsuccessful_branch_rows = [
        (sample["row"], str(sample["branch"]))
        for sample in branch_samples
        if not sample["successful"] and branch_ok(sample["row"], str(sample["branch"]))
    ]
    legacy_max_ax_boundary_rows = [
        legacy_max_ax_boundary_row(
            "successful",
            successful_branch_rows,
        ),
        legacy_max_ax_boundary_row(
            "found unsuccessful",
            found_unsuccessful_branch_rows,
        ),
    ]

    legacy_max_ax_example_rows: list[list[object]] = []
    for label, rows in (
        ("successful", successful_branch_rows),
        ("found unsuccessful", found_unsuccessful_branch_rows),
    ):
        ranked_rows = sorted(
            rows,
            key=lambda item: legacy_max_ax_row_value(item[0], item[1])[0],
            reverse=True,
        )
        for row, branch in ranked_rows[:10]:
            values = legacy_max_ax_values(row, branch)
            max_value, max_axis = legacy_max_ax_row_value(row, branch)
            legacy_max_ax_example_rows.append(
                [
                    label,
                    row["testId"],
                    branch,
                    fmt_num(values[1]),
                    fmt_num(values[4]),
                    fmt_num(values[6]),
                    f"Ax{max_axis}" if max_axis else "n/a",
                    fmt_num(max_value),
                    fmt_num(branch_finest(row, branch)),
                    branch_status(row, branch)[1] or "empty",
                ]
            )

    legacy_jump_rows: list[list[object]] = []
    for branch in ("S", "L"):
        matching_target_rows = [
            row
            for row in tests
            if vector_delta(
                branch_vector(row, "Control", branch),
                branch_vector(row, "Lift", branch),
                invalid_abs_min,
            ).valid
            and vector_delta(
                branch_vector(row, "Control", branch),
                branch_vector(row, "Lift", branch),
                invalid_abs_min,
            ).max_abs
            <= joint_tol
        ]
        for axis in (1, 4, 6):
            control_values = [branch_axis_jump(row, "Control", branch, axis) for row in matching_target_rows]
            legacy_values = [branch_axis_jump(row, "", branch, axis) for row in matching_target_rows]
            win_values = [branch_win_jump(row, branch, "Win", axis) for row in matching_target_rows]
            win2_values = [branch_win_jump(row, branch, "Win2", axis) for row in matching_target_rows]
            legacy_jump_rows.append(stats_row(f"{branch} legacy MaxAx{axis}", legacy_values))
            legacy_jump_rows.append(stats_row(f"{branch} legacy WinAx{axis}", win_values))
            legacy_jump_rows.append(stats_row(f"{branch} legacy Win2Ax{axis}", win2_values))
            correlation_rows.append(
                [
                    branch,
                    axis,
                    len(matching_target_rows),
                    fmt_num(pearson(control_values, legacy_values)),
                    fmt_num(pearson(control_values, win_values)),
                    fmt_num(pearson(control_values, win2_values)),
                ]
            )

    path_groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    path_max_by_test: dict[str, dict[str, str]] = {}
    rot_max_by_test: dict[str, dict[str, str]] = {}
    path_dist_by_mode: dict[str, list[float]] = defaultdict(list)
    rot_dist_by_mode: dict[str, list[float]] = defaultdict(list)
    pathl_ratio_diff_values: dict[str, list[float]] = defaultdict(list)
    pathl_ratio_issue_counts = Counter()
    pathl_ratio_issue_examples: dict[str, list[list[object]]] = defaultdict(list)
    pathl_anomaly_row_counts = Counter()
    pathl_anomaly_dist_values: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: {"PathDist": [], "Rotdist": []}
    )
    pathl_anomaly_combination_counts = Counter()
    cfx_bad = 0
    branch_bad = 0

    def add_pathl_anomaly_stat(label: str, path_dist: float, rot_dist: float) -> None:
        pathl_anomaly_row_counts[label] += 1
        if math.isfinite(path_dist):
            pathl_anomaly_dist_values[label]["PathDist"].append(path_dist)
        if math.isfinite(rot_dist):
            pathl_anomaly_dist_values[label]["Rotdist"].append(rot_dist)

    for row in pathl:
        key = (row.get("testId", ""), row.get("confId", ""), row.get("branch S/L", ""))
        path_groups[key].append(row)
        path_dist = as_float(row.get("PathDist"))
        rot_dist = as_float(row.get("Rotdist"))
        test_id = row.get("testId", "")
        if math.isfinite(path_dist):
            previous = path_max_by_test.get(test_id)
            if previous is None or path_dist > as_float(previous.get("PathDist")):
                path_max_by_test[test_id] = row
        if math.isfinite(rot_dist):
            previous = rot_max_by_test.get(test_id)
            if previous is None or rot_dist > as_float(previous.get("Rotdist")):
                rot_max_by_test[test_id] = row
        cfx_ok = as_bool(row.get("CfxOK"))
        path_branch_ok = row.get("FoundBranch", "") == row.get("branch S/L", "")
        if not cfx_ok:
            cfx_bad += 1
        if not path_branch_ok:
            branch_bad += 1
        anomaly_reasons: list[str] = []
        if not cfx_ok:
            anomaly_reasons.append("CfxOK != TRUE")
        if not path_branch_ok:
            anomaly_reasons.append("FoundBranch mismatch")
        if math.isfinite(path_dist) and path_dist > path_warn:
            anomaly_reasons.append(f"PathDist > {fmt_num(path_warn)} mm")
        if math.isfinite(rot_dist) and rot_dist > rot_warn:
            anomaly_reasons.append(f"Rotdist > {fmt_num(rot_warn)} deg")
        if anomaly_reasons:
            add_pathl_anomaly_stat("any anomaly", path_dist, rot_dist)
            for reason in anomaly_reasons:
                add_pathl_anomaly_stat(reason, path_dist, rot_dist)
            pathl_anomaly_combination_counts[" + ".join(anomaly_reasons)] += 1

    pathl_group_rows: list[list[object]] = []
    pathl_bad_group_count = 0
    pathl_bad_pair_count = 0
    pathl_pair_count = 0
    pathl_incomplete_pair_rows = 0
    pathl_group_summaries: list[tuple[float, float, list[object]]] = []
    for (test_id, conf_id, branch), rows in sorted(
        path_groups.items(), key=lambda item: (int(item[0][0] or 0), int(item[0][1] or 0), item[0][2])
    ):
        if len(rows) != PATHL_EXPECTED_ROWS_PER_BRANCH:
            pathl_bad_group_count += 1
            pathl_group_rows.append([test_id, conf_id, branch, len(rows), PATHL_EXPECTED_ROWS_PER_BRANCH])
        if len(rows) % 2:
            pathl_incomplete_pair_rows += 1

        path_length = as_float(rows[0].get("PathLenth")) if rows else math.nan
        rot_length = as_float(rows[0].get("RotLength")) if rows else math.nan
        short_group_row = pathl_short_group_stats_row(test_id, conf_id, branch, rows)
        if short_group_row:
            pathl_group_summaries.append((path_length, rot_length, short_group_row))

        for row_index, sample_row in enumerate(rows):
            mode = "PathRatio" if row_index % 2 == 0 else "RotRatio"
            path_dist = as_float(sample_row.get("PathDist"))
            rot_dist = as_float(sample_row.get("Rotdist"))
            if math.isfinite(path_dist):
                path_dist_by_mode[mode].append(path_dist)
            if math.isfinite(rot_dist):
                rot_dist_by_mode[mode].append(rot_dist)

        previous_path_ratio = math.nan
        previous_rot_ratio = math.nan
        for pair_index in range(len(rows) // 2):
            path_row = rows[pair_index * 2]
            rot_row = rows[pair_index * 2 + 1]
            expected_ratio = (pair_index + 1) / PATHL_SAMPLES_PER_BRANCH
            pathl_pair_count += 1

            path_ratio = used_ratio_value(path_row.get("RatioPath"))
            path_ratio_rot_column = as_float(path_row.get("RatioRot"))
            rot_ratio_path_column = as_float(rot_row.get("RatioPath"))
            rot_ratio = used_ratio_value(rot_row.get("RatioRot"))
            path_expected_diff = abs(path_ratio - expected_ratio)
            rot_expected_diff = abs(rot_ratio - expected_ratio)
            pair_ratio_diff = abs(path_ratio - rot_ratio)
            pathl_ratio_diff_values["RatioPath vs expected"].append(path_expected_diff)
            pathl_ratio_diff_values["RatioRot vs expected"].append(rot_expected_diff)
            pathl_ratio_diff_values["RatioPath vs RatioRot"].append(pair_ratio_diff)

            problems: list[str] = []
            if not math.isfinite(path_ratio):
                problems.append("odd row is not PathRatio")
            if not math.isfinite(rot_ratio):
                problems.append("even row is not RotRatio")
            if math.isfinite(path_ratio) and not (0.0 <= path_ratio <= 1.0):
                problems.append("RatioPath outside 0..1")
            if math.isfinite(rot_ratio) and not (0.0 <= rot_ratio <= 1.0):
                problems.append("RatioRot outside 0..1")
            if not is_unused_ratio_marker(path_ratio_rot_column):
                problems.append("odd RatioRot has used value")
            if not is_unused_ratio_marker(rot_ratio_path_column):
                problems.append("even RatioPath has used value")
            if path_expected_diff > PATHL_RATIO_TOL:
                problems.append("RatioPath differs from sample")
            if rot_expected_diff > PATHL_RATIO_TOL:
                problems.append("RatioRot differs from sample")
            if pair_index > 0:
                if math.isfinite(path_ratio) and math.isfinite(previous_path_ratio) and not (
                    path_ratio > previous_path_ratio
                ):
                    problems.append("RatioPath not increasing")
                if math.isfinite(rot_ratio) and math.isfinite(previous_rot_ratio) and not (
                    rot_ratio > previous_rot_ratio
                ):
                    problems.append("RatioRot not increasing")
            if pair_ratio_diff > PATHL_RATIO_TOL:
                problems.append("pair ratios differ")

            if problems:
                pathl_bad_pair_count += 1
                pathl_ratio_issue_counts.update(problems)
                for problem in problems:
                    if (
                        problem in PATHL_RATIO_EXAMPLE_PROBLEMS
                        and len(pathl_ratio_issue_examples[problem]) < PATHL_RATIO_EXAMPLE_LIMIT
                    ):
                        pathl_ratio_issue_examples[problem].append(
                            [
                                problem,
                                test_id,
                                conf_id,
                                branch,
                                fmt_num(as_float(path_row.get("PathLenth"))),
                                fmt_num(as_float(path_row.get("RotLength"))),
                                pair_index + 1,
                                fmt_num(expected_ratio),
                                fmt_num(previous_path_ratio),
                                fmt_num(path_ratio),
                                fmt_num(rot_ratio),
                                "PathRatio",
                                "RotRatio",
                                fmt_num(as_float(path_row.get("PathDist"))),
                                fmt_num(as_float(rot_row.get("Rotdist"))),
                            ]
                        )

            previous_path_ratio = path_ratio
            previous_rot_ratio = rot_ratio

    worst_path_tests = sorted(
        path_max_by_test.items(), key=lambda item: as_float(item[1].get("PathDist")), reverse=True
    )[:10]
    worst_rot_tests = sorted(
        rot_max_by_test.items(), key=lambda item: as_float(item[1].get("Rotdist")), reverse=True
    )[:10]

    branch_counts = Counter(branch_label(row) for row in success)
    legacy_branch_counts = Counter(legacy_branch_label(row) for row in success)
    success_tests = len(success_by_test)
    lines: list[str] = []
    lines.extend(
        [
            f"# ABB MoveL Analysis {version}",
            "",
            "## Summary",
            "",
            f"- Tests: {len(tests)}",
            f"- Tests with success rows: {success_tests}",
            f"- Success rows: {len(success)}",
            f"- Tests without success rows: {len(missing_success)}",
            f"- PathL diagnostic rows: {len(pathl)}",
            f"- PathL groups by test/conf/branch: {len(path_groups)}",
            f"- Joint tolerance: {joint_tol} deg",
            f"- Path distance warning: {path_warn} mm",
            f"- Rotation distance warning: {rot_warn} deg",
            "",
            "## Found But Unsuccessful Branches",
            "",
            "These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.",
            "",
            f"- Found branches in tests.csv: S={found_branch_counts['S']}, L={found_branch_counts['L']}",
            f"- Found branches without matching successful control branch: S={unsuccessful_found_counts['S']}, L={unsuccessful_found_counts['L']}",
            "",
        ]
    )
    lines.extend(
        md_table(
            [
                "branch",
                "found",
                "unsuccessful",
                "unsuccessful %",
                "FinestStep median",
                "FinestStep p95",
                "FinestStep max",
                "jump median",
                "jump p95",
                "jump max",
            ],
            unsuccessful_found_stats,
        )
    )

    lines.extend(
        [
            "",
            "## FinestStep Success Boundary",
            "",
            "`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["sample", "n", "min", "mean", "median", "p95", "max"],
            finest_step_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Joint Target Consistency",
            "",
            f"- C/CalcC mismatches: {max_deltas['C vs CalcC']}",
            f"- C/PathL mismatches: {max_deltas['C vs PathL']}",
            f"- CalcC/PathL mismatches: {max_deltas['CalcC vs PathL']}",
            f"- Worst valid delta: test {worst_delta[0]}, {worst_delta[1]}, axis {worst_delta[2].axis}, {fmt_num(worst_delta[2].max_abs)} deg",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["testId", "confId", "comparison", "max abs deg", "axis", "control branch"],
            mismatch_rows[:max_rows],
        )
    )
    if len(mismatch_rows) > max_rows:
        lines.append(f"... {len(mismatch_rows) - max_rows} more omitted by report limit.")

    lines.extend(
        [
            "",
            "## Branch Matching",
            "",
            f"- Control branch counts: S={branch_counts['S']}, L={branch_counts['L']}, none={branch_counts['none']}",
            f"- ControlMatchShort XOR ControlMatchLong violations: {len(xor_rows)}",
            f"- C vs selected Control target mismatches: S={control_mismatches['S']}, L={control_mismatches['L']}",
            f"- Legacy Matches counts: S={legacy_branch_counts['S']}, L={legacy_branch_counts['L']}, none={legacy_branch_counts['none']}",
            f"- Legacy/control branch disagreements: {sum(count for pair, count in branch_compare.items() if pair[0] != pair[1])}",
            f"- C vs selected Lift target mismatches: S={legacy_mismatches['S']}, L={legacy_mismatches['L']}",
            "",
            "### Control XOR Violations",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["testId", "confId", "ControlMatchShort", "ControlMatchLong"],
            xor_rows[:max_rows],
        )
    )
    if len(xor_rows) > max_rows:
        lines.append(f"... {len(xor_rows) - max_rows} more omitted by report limit.")

    lines.extend(
        [
            "",
            "### Control Target Mismatches",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["testId", "confId", "branch", "target", "max abs deg", "axis"],
            control_rows[:max_rows],
        )
    )
    if len(control_rows) > max_rows:
        lines.append(f"... {len(control_rows) - max_rows} more omitted by report limit.")

    lines.extend(["", "### Legacy vs Control Branch Comparison", ""])
    lines.extend(
        md_table(
            ["control", "legacy", "rows"],
            [[control, legacy, count] for (control, legacy), count in sorted(branch_compare.items())],
        )
    )
    lines.extend(["", "### Legacy Lift Target Mismatches", ""])
    lines.extend(
        md_table(
            ["testId", "confId", "branch", "target", "max abs deg", "axis"],
            legacy_rows[:max_rows],
        )
    )
    if len(legacy_rows) > max_rows:
        lines.append(f"... {len(legacy_rows) - max_rows} more omitted by report limit.")

    lines.extend(
        [
            "",
            "## Control Jump Boundaries",
            "",
            "`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.",
            "",
        ]
    )
    lines.extend(md_table(["sample", "n", "mean", "median", "p95", "max", "FinestStep at max"], jump_rows))

    lines.extend(
        [
            "",
            "## Legacy 1/1000 MaxAx Boundary",
            "",
            "`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.",
            "",
            "### Successful vs Unsuccessful",
            "",
            "This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.",
            "",
        ]
    )
    max_ax_headers = [
        "sample",
        "n",
        "mean",
        "median",
        "p95",
        "max",
        "testId at max",
        "branch",
        "axis at max",
        "MaxAx1",
        "MaxAx4",
        "MaxAx6",
    ]
    lines.extend(md_table(max_ax_headers, legacy_max_ax_boundary_rows))
    lines.extend(
        [
            "",
            "### Max Examples",
            "",
        ]
    )
    lines.extend(
        md_table(
            [
                "outcome",
                "testId",
                "branch",
                "MaxAx1",
                "MaxAx4",
                "MaxAx6",
                "max axis",
                "row max",
                "FinestStep",
                "stErr",
            ],
            legacy_max_ax_example_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Legacy Jump Comparison",
            "",
            "Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.",
            "",
            "### Legacy Jump Statistics",
            "",
        ]
    )
    lines.extend(md_table(["sample", "n", "mean", "median", "p95", "max"], legacy_jump_rows))
    lines.extend(["", "### Control vs Legacy Correlation", ""])
    lines.extend(
        md_table(
            ["branch", "axis", "matching targets", "Control/Max", "Control/Win", "Control/Win2"],
            correlation_rows,
        )
    )

    path_dist_values = [as_float(row.get("PathDist")) for row in pathl if math.isfinite(as_float(row.get("PathDist")))]
    rot_dist_values = [as_float(row.get("Rotdist")) for row in pathl if math.isfinite(as_float(row.get("Rotdist")))]
    pathl_anomaly_labels = [
        "any anomaly",
        "CfxOK != TRUE",
        "FoundBranch mismatch",
        f"PathDist > {fmt_num(path_warn)} mm",
        f"Rotdist > {fmt_num(rot_warn)} deg",
    ]
    pathl_anomaly_summary_rows: list[list[object]] = []
    for label in pathl_anomaly_labels:
        path_stats = stats_summary(pathl_anomaly_dist_values[label]["PathDist"])
        rot_stats = stats_summary(pathl_anomaly_dist_values[label]["Rotdist"])
        row_count = pathl_anomaly_row_counts[label]
        pathl_anomaly_summary_rows.append(
            [
                label,
                row_count,
                fmt_num((row_count / len(pathl) * 100.0) if pathl else math.nan),
                fmt_num(float(path_stats["median"])),
                fmt_num(float(path_stats["p95"])),
                fmt_num(float(path_stats["max"])),
                fmt_num(float(rot_stats["median"])),
                fmt_num(float(rot_stats["p95"])),
                fmt_num(float(rot_stats["max"])),
            ]
        )
    pathl_anomaly_combination_rows = [
        [
            label,
            count,
            fmt_num((count / len(pathl) * 100.0) if pathl else math.nan),
        ]
        for label, count in pathl_anomaly_combination_counts.most_common()
    ]
    pathl_ratio_issue_count_rows = [[problem, count] for problem, count in pathl_ratio_issue_counts.most_common()]
    pathl_ratio_issue_count_rows.extend(
        [problem, 0] for problem in PATHL_RATIO_EXAMPLE_PROBLEMS if problem not in pathl_ratio_issue_counts
    )
    pathl_short_length_rows = [
        row
        for _, _, row in sorted(
            pathl_group_summaries,
            key=lambda item: (not math.isfinite(item[0]), item[0], item[1]),
        )[:PATHL_SHORT_GROUP_LIMIT]
    ]
    pathl_short_rot_rows = [
        row
        for _, _, row in sorted(
            pathl_group_summaries,
            key=lambda item: (not math.isfinite(item[1]), item[1], item[0]),
        )[:PATHL_SHORT_GROUP_LIMIT]
    ]
    pathl_short_group_headers = [
        "testId",
        "confId",
        "branch",
        "PathLength",
        "RotLength",
        "abs(RatioPath-expected) n",
        "abs(RatioPath-expected) min",
        "abs(RatioPath-expected) mean",
        "abs(RatioPath-expected) median",
        "abs(RatioPath-expected) p95",
        "abs(RatioPath-expected) max",
        "abs(RatioRot-expected) n",
        "abs(RatioRot-expected) min",
        "abs(RatioRot-expected) mean",
        "abs(RatioRot-expected) median",
        "abs(RatioRot-expected) p95",
        "abs(RatioRot-expected) max",
    ]
    lines.extend(
        [
            "",
            "## PathL Diagnostics",
            "",
            f"- Rows with CfxOK != TRUE: {cfx_bad}",
            f"- Rows with FoundBranch mismatch: {branch_bad}",
            f"- Groups with row count != {PATHL_EXPECTED_ROWS_PER_BRANCH}: {pathl_bad_group_count}",
            f"- Groups with dangling unpaired row: {pathl_incomplete_pair_rows}",
            f"- Ratio pairs checked: {pathl_pair_count}",
            f"- Ratio pair/order issues: {pathl_bad_pair_count}",
            f"- Mean PathDist: {fmt_num(mean(path_dist_values)) if path_dist_values else 'n/a'}",
            f"- Max PathDist: {fmt_num(max(path_dist_values)) if path_dist_values else 'n/a'}",
            f"- Mean Rotdist: {fmt_num(mean(rot_dist_values)) if rot_dist_values else 'n/a'}",
            f"- Max Rotdist: {fmt_num(max(rot_dist_values)) if rot_dist_values else 'n/a'}",
            "",
            "### PathL Distance By Ratio Source",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["metric", "n", "mean", "median", "p95", "max"],
            [
                stats_row("PathDist measured from PathRatio rows", path_dist_by_mode["PathRatio"]),
                stats_row("PathDist measured from RotRatio rows", path_dist_by_mode["RotRatio"]),
                stats_row("Rotdist measured from PathRatio rows", rot_dist_by_mode["PathRatio"]),
                stats_row("Rotdist measured from RotRatio rows", rot_dist_by_mode["RotRatio"]),
            ],
        )
    )
    lines.extend(
        [
            "",
            "### PathL Sample Group Issues",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["testId", "confId", "branch", "rows", "expected"],
            pathl_group_rows[:max_rows],
        )
    )
    if len(pathl_group_rows) > max_rows:
        lines.append(f"... {len(pathl_group_rows) - max_rows} more omitted by report limit.")

    lines.extend(
        [
            "",
            "### PathL Ratio Difference Statistics",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["metric", "n", "mean", "median", "p95", "max"],
            [
                stats_row("abs(RatioPath - expected 0.01 step)", pathl_ratio_diff_values["RatioPath vs expected"]),
                stats_row("abs(RatioRot - expected 0.01 step)", pathl_ratio_diff_values["RatioRot vs expected"]),
                stats_row("abs(RatioPath - RatioRot)", pathl_ratio_diff_values["RatioPath vs RatioRot"]),
            ],
        )
    )
    lines.extend(["", "### Shortest PathLength Ratio Behavior", ""])
    lines.extend(md_table(pathl_short_group_headers, pathl_short_length_rows))
    lines.extend(["", "### Shortest RotLength Ratio Behavior", ""])
    lines.extend(md_table(pathl_short_group_headers, pathl_short_rot_rows))
    lines.extend(["", "### PathL Ratio Issue Counts", ""])
    lines.extend(
        md_table(
            ["problem", "count"],
            pathl_ratio_issue_count_rows,
        )
    )
    lines.extend(["", "### PathL Ratio Issue Examples", ""])
    lines.extend(
        md_table(
            [
                "problem",
                "testId",
                "confId",
                "branch",
                "PathLength",
                "RotLength",
                "pair",
                "expected",
                "previous RatioPath",
                "RatioPath",
                "RatioRot",
                "odd row mode",
                "even row mode",
                "odd PathDist",
                "even Rotdist",
            ],
            [
                row
                for problem in PATHL_RATIO_EXAMPLE_PROBLEMS
                for row in pathl_ratio_issue_examples[problem]
            ],
        )
    )

    lines.extend(
        [
            "",
            "### PathL Anomaly Statistics",
            "",
        ]
    )
    lines.extend(
        md_table(
            [
                "condition",
                "rows",
                "% rows",
                "PathDist median",
                "PathDist p95",
                "PathDist max",
                "Rotdist median",
                "Rotdist p95",
                "Rotdist max",
            ],
            pathl_anomaly_summary_rows,
        )
    )
    lines.extend(["", "### PathL Anomaly Reason Combinations", ""])
    lines.extend(md_table(["conditions", "rows", "% rows"], pathl_anomaly_combination_rows))

    lines.extend(["", "### Worst PathDist By Test", ""])
    lines.extend(
        md_table(
            ["testId", "max PathDist", "PathLength", "RotLength", "FinestStep"],
            [
                [
                    test_id,
                    fmt_num(as_float(row.get("PathDist"))),
                    fmt_num(as_float(row.get("PathLenth"))),
                    fmt_num(as_float(row.get("RotLength"))),
                    fmt_num(pathl_finest_step(row, tests_by_id)),
                ]
                for test_id, row in worst_path_tests
            ],
        )
    )
    lines.extend(["", "### Worst Rotdist By Test", ""])
    lines.extend(
        md_table(
            ["testId", "max Rotdist", "PathLength", "RotLength", "FinestStep"],
            [
                [
                    test_id,
                    fmt_num(as_float(row.get("Rotdist"))),
                    fmt_num(as_float(row.get("PathLenth"))),
                    fmt_num(as_float(row.get("RotLength"))),
                    fmt_num(pathl_finest_step(row, tests_by_id)),
                ]
                for test_id, row in worst_rot_tests
            ],
        )
    )

    lines.extend(
        [
            "",
            "## Suggested Next Investigations",
            "",
            "- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.",
            "- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.",
            "- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.",
        ]
    )

    out_path = Path(args.out) if args.out else root / "reports" / f"movel_analysis_{version}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
