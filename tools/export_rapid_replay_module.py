#!/usr/bin/env python3
"""Export ABB RAPID target declarations for replaying MoveL CSV tests."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


EXTAX_UNKNOWN = ["9E+09"] * 6
AXES = range(1, 7)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="CSV suffix, for example v11")
    parser.add_argument("--root", default=".", help="Folder with tests/success CSV files")
    parser.add_argument("--test-id", action="append", default=[], help="Export only this testId; can be repeated")
    parser.add_argument("--conf-id", action="append", default=[], help="Export only this confId; can be repeated")
    parser.add_argument(
        "--all-tests",
        action="store_true",
        help="Export target declarations for all tests, not only tests with success rows",
    )
    parser.add_argument("--module-name", default=None, help="RAPID module name")
    parser.add_argument("--out", default=None, help="Output .mod path")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def rapid_num(value: str | None) -> str:
    if value is None or value == "":
        return "0"
    value = value.strip()
    if value.upper() in {"TRUE", "FALSE"}:
        return value.upper()
    return value


def rapid_name(prefix: str, version: str, test_id: str, conf_id: str | None = None) -> str:
    if conf_id is None:
        return f"{prefix}_{version}_t{test_id}"
    return f"{prefix}_{version}_t{test_id}_c{conf_id}"


def default_module_name(version: str, test_ids: list[str], conf_ids: list[str]) -> str:
    parts = [f"ReplayTargets_{version}"]
    if test_ids:
        parts.append("t" + "_".join(test_ids))
    if conf_ids:
        parts.append("c" + "_".join(conf_ids))
    return "_".join(parts)


def vector(row: dict[str, str], columns: list[str]) -> str:
    return "[" + ",".join(rapid_num(row.get(column)) for column in columns) + "]"


def robtarget(row: dict[str, str], prefix: str) -> str:
    pos = vector(row, [f"{prefix}_x", f"{prefix}_y", f"{prefix}_z"])
    quat = vector(row, [f"{prefix}_q1", f"{prefix}_q2", f"{prefix}_q3", f"{prefix}_q4"])
    conf = vector(row, [f"{prefix}_cf1", f"{prefix}_cf4", f"{prefix}_cf6", f"{prefix}_cfx"])
    extax = "[" + ",".join(EXTAX_UNKNOWN) + "]"
    return f"[{pos},{quat},{conf},{extax}]"


def robtarget_with_conf(posquat_row: dict[str, str], prefix: str, conf_row: dict[str, str]) -> str:
    pos = vector(posquat_row, [f"{prefix}_x", f"{prefix}_y", f"{prefix}_z"])
    quat = vector(posquat_row, [f"{prefix}_q1", f"{prefix}_q2", f"{prefix}_q3", f"{prefix}_q4"])
    conf = vector(conf_row, ["B*_cf1", "B*_cf4", "B*_cf6", "B*_cfx"])
    extax = "[" + ",".join(EXTAX_UNKNOWN) + "]"
    return f"[{pos},{quat},{conf},{extax}]"


def jointtarget(row: dict[str, str], prefix: str) -> str:
    robax = vector(row, [f"{prefix}_rax{axis}" for axis in AXES])
    extax = "[" + ",".join(EXTAX_UNKNOWN) + "]"
    return f"[{robax},{extax}]"


def has_value(row: dict[str, str], column: str) -> bool:
    return row.get(column, "").strip() != ""


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    version = args.version
    tests = read_csv(root / f"tests_{version}.csv")
    success = read_csv(root / f"success_{version}.csv")

    test_filter = set(args.test_id)
    conf_filter = set(args.conf_id)

    if test_filter:
        tests = [row for row in tests if row.get("testId") in test_filter]
        success = [row for row in success if row.get("testId") in test_filter]
    if conf_filter:
        success = [row for row in success if row.get("confId") in conf_filter]

    success_by_test: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in success:
        success_by_test[row["testId"]].append(row)

    if not args.all_tests:
        tests = [row for row in tests if row.get("testId") in success_by_test]

    tests = sorted(tests, key=lambda row: int(row["testId"]))
    tests_by_id = {row["testId"]: row for row in tests}
    success = sorted(success, key=lambda row: (int(row["testId"]), int(row["confId"])))

    module_name = args.module_name or default_module_name(version, args.test_id, args.conf_id)
    lines = [
        f"MODULE {module_name}",
        f"    ! Generated from tests_{version}.csv and success_{version}.csv.",
        "    ! Target names include version and testId. B* variants include version, testId, and confId.",
        "",
    ]

    if tests:
        lines.append("    ! Robtargets and jointtargets for replay")
    for row in tests:
        test_id = row["testId"]
        lines.extend(
            [
                f"    CONST robtarget {rapid_name('rA', version, test_id)} := {robtarget(row, 'A')};",
                f"    CONST robtarget {rapid_name('rB', version, test_id)} := {robtarget(row, 'B')};",
            ]
        )
        for success_row in sorted(success_by_test.get(test_id, []), key=lambda item: int(item["confId"])):
            lines.append(
                f"    CONST robtarget {rapid_name('rB', version, test_id, success_row['confId'])} := {robtarget_with_conf(row, 'B', success_row)};"
            )
        lines.extend(
            [
                f"    CONST jointtarget {rapid_name('jA', version, test_id)} := {jointtarget(row, 'A')};",
                f"    CONST jointtarget {rapid_name('jB', version, test_id)} := {jointtarget(row, 'B')};",
                f"    CONST jointtarget {rapid_name('jBseed', version, test_id)} := {jointtarget(row, 'Bseed')};",
            ]
        )
        if has_value(row, "Bseed"):
            lines.append(f"    CONST num {rapid_name('seedB', version, test_id)} := {rapid_num(row.get('Bseed'))};")
        lines.append("")

    lines.append("ENDMODULE")

    out_path = Path(args.out) if args.out else root / "rapid" / f"ReplayTargets_{version}.mod"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    print(f"exported_tests={len(tests)}")
    print(f"exported_success_conf_rows={len(success)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
