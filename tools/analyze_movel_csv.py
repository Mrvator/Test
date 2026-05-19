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
from statistics import mean
from typing import Iterable


AXES = range(1, 7)


@dataclass(frozen=True)
class Delta:
    max_abs: float
    axis: int
    values: list[float]
    valid: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="CSV suffix, for example v11")
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


def branch_label(row: dict[str, str]) -> str:
    if as_bool(row.get("ControlMatchShort")):
        return "S"
    if as_bool(row.get("ControlMatchLong")):
        return "L"
    return "none"


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    version = args.version
    profile = load_profile(root / args.config)
    joint_tol = float(profile["joint_abs_tolerance_deg"])
    path_warn = float(profile["path_distance_warn_mm"])
    rot_warn = float(profile["rotation_distance_warn_deg"])
    invalid_abs_min = float(profile["invalid_joint_abs_min"])
    max_rows = int(profile["max_anomaly_rows"])

    tests_path = root / f"tests_{version}.csv"
    success_path = root / f"success_{version}.csv"
    pathl_path = root / f"pathl_{version}.csv"
    tests = read_csv(tests_path)
    success = read_csv(success_path)
    pathl = read_csv(pathl_path)

    tests_by_id = {row["testId"]: row for row in tests}
    success_by_test: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in success:
        success_by_test[row["testId"]].append(row)

    missing_success = sorted(set(tests_by_id) - set(success_by_test), key=lambda x: int(x))

    mismatch_rows: list[list[object]] = []
    branch_rows: list[list[object]] = []
    legacy_diff_rows: list[list[object]] = []
    max_deltas = Counter()
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
        if test:
            selected = branch_label(row)
            if selected in ("S", "L"):
                prefix = "ControlShort" if selected == "S" else "ControlLong"
                control_delta = vector_delta(path, joint_vector(test, prefix), invalid_abs_min)
                if not control_delta.valid or control_delta.max_abs > joint_tol:
                    branch_rows.append(
                        [
                            test_id,
                            conf_id,
                            selected,
                            prefix,
                            fmt_num(control_delta.max_abs),
                            control_delta.axis or "n/a",
                        ]
                    )

        legacy = (as_bool(row.get("MatchesShort")), as_bool(row.get("MatchesLong")))
        control = (as_bool(row.get("ControlMatchShort")), as_bool(row.get("ControlMatchLong")))
        if legacy != control:
            legacy_diff_rows.append([test_id, conf_id, legacy[0], legacy[1], control[0], control[1]])

    path_groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    path_anomalies: list[list[object]] = []
    path_max_by_test: dict[str, float] = defaultdict(float)
    rot_max_by_test: dict[str, float] = defaultdict(float)
    cfx_bad = 0
    branch_bad = 0
    for row in pathl:
        key = (row.get("testId", ""), row.get("confId", ""), row.get("branch S/L", ""))
        path_groups[key].append(row)
        path_dist = as_float(row.get("PathDist"))
        rot_dist = as_float(row.get("Rotdist"))
        test_id = row.get("testId", "")
        if math.isfinite(path_dist):
            path_max_by_test[test_id] = max(path_max_by_test[test_id], path_dist)
        if math.isfinite(rot_dist):
            rot_max_by_test[test_id] = max(rot_max_by_test[test_id], rot_dist)
        cfx_ok = as_bool(row.get("CfxOK"))
        branch_ok = row.get("FoundBranch", "") == row.get("branch S/L", "")
        if not cfx_ok:
            cfx_bad += 1
        if not branch_ok:
            branch_bad += 1
        if (not cfx_ok) or (not branch_ok) or path_dist > path_warn or rot_dist > rot_warn:
            path_anomalies.append(
                [
                    test_id,
                    row.get("confId", ""),
                    row.get("branch S/L", ""),
                    row.get("FoundBranch", ""),
                    row.get("CfxOK", ""),
                    fmt_num(path_dist),
                    fmt_num(rot_dist),
                ]
            )

    worst_path_tests = sorted(path_max_by_test.items(), key=lambda item: item[1], reverse=True)[:10]
    worst_rot_tests = sorted(rot_max_by_test.items(), key=lambda item: item[1], reverse=True)[:10]

    branch_counts = Counter(branch_label(row) for row in success)
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
            f"- Tests missing success rows: {len(missing_success)}",
            f"- PathL diagnostic rows: {len(pathl)}",
            f"- PathL groups by test/conf/branch: {len(path_groups)}",
            f"- Joint tolerance: {joint_tol} deg",
            f"- Path distance warning: {path_warn} mm",
            f"- Rotation distance warning: {rot_warn} deg",
            "",
            "## Success Coverage",
            "",
        ]
    )
    lines.extend(md_table(["missing testId"], [[x] for x in missing_success[:max_rows]]))
    if len(missing_success) > max_rows:
        lines.append(f"... {len(missing_success) - max_rows} more omitted by report limit.")

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
            f"- Legacy/control flag differences: {len(legacy_diff_rows)}",
            f"- Selected control target mismatches: {len(branch_rows)}",
            "",
            "### Legacy vs Control Differences",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["testId", "confId", "MatchesShort", "MatchesLong", "ControlMatchShort", "ControlMatchLong"],
            legacy_diff_rows[:max_rows],
        )
    )
    lines.extend(["", "### Control Target Mismatches", ""])
    lines.extend(
        md_table(
            ["testId", "confId", "branch", "target", "max abs deg", "axis"],
            branch_rows[:max_rows],
        )
    )

    path_dist_values = [as_float(row.get("PathDist")) for row in pathl if math.isfinite(as_float(row.get("PathDist")))]
    rot_dist_values = [as_float(row.get("Rotdist")) for row in pathl if math.isfinite(as_float(row.get("Rotdist")))]
    lines.extend(
        [
            "",
            "## PathL Diagnostics",
            "",
            f"- Rows with CfxOK != TRUE: {cfx_bad}",
            f"- Rows with FoundBranch mismatch: {branch_bad}",
            f"- Mean PathDist: {fmt_num(mean(path_dist_values)) if path_dist_values else 'n/a'}",
            f"- Max PathDist: {fmt_num(max(path_dist_values)) if path_dist_values else 'n/a'}",
            f"- Mean Rotdist: {fmt_num(mean(rot_dist_values)) if rot_dist_values else 'n/a'}",
            f"- Max Rotdist: {fmt_num(max(rot_dist_values)) if rot_dist_values else 'n/a'}",
            "",
            "### PathL Anomalies",
            "",
        ]
    )
    lines.extend(
        md_table(
            ["testId", "confId", "branch", "found", "CfxOK", "PathDist", "Rotdist"],
            path_anomalies[:max_rows],
        )
    )
    if len(path_anomalies) > max_rows:
        lines.append(f"... {len(path_anomalies) - max_rows} more omitted by report limit.")

    lines.extend(["", "### Worst PathDist By Test", ""])
    lines.extend(md_table(["testId", "max PathDist"], [[k, fmt_num(v)] for k, v in worst_path_tests]))
    lines.extend(["", "### Worst Rotdist By Test", ""])
    lines.extend(md_table(["testId", "max Rotdist"], [[k, fmt_num(v)] for k, v in worst_rot_tests]))

    lines.extend(
        [
            "",
            "## Suggested Next Investigations",
            "",
            "- Inspect missing success rows first; these are failed or unrecorded MoveL executions.",
            "- For joint mismatches, compare the reported axis against RAPID configuration changes and quaternion branch choice.",
            "- For PathL anomalies, inspect the same `testId/confId/branch` in the raw PathL rows and verify branch interpolation state.",
        ]
    )

    out_path = Path(args.out) if args.out else root / "reports" / f"movel_analysis_{version}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
