# ABB MoveL CSV Schema Notes

## Keys

- `testId` pairs records across all CSV files.
- `success_<version>.csv` can contain multiple rows per `testId`, typically one per `confId`/branch candidate.
- `pathl_<version>.csv` can contain many rows per `testId` and `confId`.

## RAPID Replay Declarations

Replay modules are generated from versioned `tests_<version>.csv` and `success_<version>.csv` files. Fresh `tests.csv`, `success.csv`, and `pathl.csv` exports are renamed to the next version before analysis.

- `rA_<version>_t<testId>`: `robtarget` from `A_x/y/z`, `A_q1/q2/q3/q4`, and `A_cf1/cf4/cf6/cfx`.
- `rB_<version>_t<testId>`: `robtarget` from `B_x/y/z`, `B_q1/q2/q3/q4`, and `B_cf1/cf4/cf6/cfx`.
- `rB_<version>_t<testId>_c<confId>`: `robtarget` copied from `B_x/y/z` and `B_q1/q2/q3/q4`, with `confdata` from `success.B*_cf1`, `success.B*_cf4`, `success.B*_cf6`, and `success.B*_cfx`.
- `jA_<version>_t<testId>`: `jointtarget` from `A_rax1..6`.
- `jB_<version>_t<testId>`: `jointtarget` from `B_rax1..6`.
- `jBseed_<version>_t<testId>`: `jointtarget` from `Bseed_rax1..6`.

The replay export intentionally does not use arrays so individual test declarations are easy to search by name.

## Joint Target Groups

Joint axes use suffixes `rax1` through `rax6`.

- `C_rax*`: actual robot end joint target after successful MoveL execution.
- `CalcC_rax*`: predicted final joint target.
- `PathL_rax*`: predicted PathL final joint target in the success table.
- `ControlShort_rax*` and `ControlLong_rax*`: current control predictions from the test table.
- `FinestStepS` and `FinestStepL`: smallest subdivision step reached while checking short/long trajectory continuity.
- `ControlShortMaxAx1/4/6` and `ControlLongMaxAx1/4/6`: largest sampled joint jumps used with `FinestStepS/L` to decide whether the branch is singular/unavailable.
- `LiftShort_rax*` and `LiftLong_rax*`: legacy lifted predictions from the test table.

Values like `9E+9` indicate unavailable/invalid prediction branches and should be ignored for normal equality checks.

## Singular Branch Rule

For each short/long branch in `tests_<version>.csv`:

- If `FinestStepS/L <= 0.0001` and the matching control max jump on axes 1/4/6 is greater than `60` degrees, the branch is unavailable.
- Unavailable branches must have `bOKshort/bOKlong = FALSE`.
- Unavailable branches must set `stErrShort/stErrLong` to `SINGULAR`.

## Core Comparisons

For each `success` row:

- Compare `C_rax*` vs `CalcC_rax*`.
- Compare `C_rax*` vs `PathL_rax*`.
- Check that exactly one of `ControlMatchShort` and `ControlMatchLong` is true.
- Check that exactly one of `MatchesShort` and `MatchesLong` is true.
- Compare the selected control branch label with the selected legacy branch label.
- Check the singular branch rule before interpreting successful branch matches.

## PathL Diagnostics

For each `pathl` row:

- `branch S/L`: expected branch label, usually `S` or `L`.
- `FoundBranch`: branch detected by the PathL prediction.
- `CfxOK`: whether the configuration/external axis constraint was satisfied.
- `PathDist`: distance residual for path prediction.
- `Rotdist`: rotation residual for orientation prediction.
- `RatioPath` and `RatioRot`: normalized path/rotation progress values.

The compact analyzer summarizes PathL ratio pairing and ratio/distance precision. It does not emit row-level anomaly tables.

## PathL Ratio Pairing

For each `testId/confId/branch` group, PathL samples are expected to be ordered as 100 pairs:

- Odd row in the pair: path-based ratio sample; read `RatioPath`.
- Even row in the pair: rotation-based ratio sample; read `RatioRot`.
- Newer CSV versions include `ExpectedRatio`; use that as the expected sample value for both path and rotation ratio precision.
- Older CSV versions without `ExpectedRatio` fall back to `(pairIndex + 1) / 100`, where the pair index is zero-based in code.

Important interpretation rules:

- `0` is a valid measured ratio value and must be compared with the expected ratio.
- Do not treat a zero ratio as an absent path or rotation result.
- New CSV versions use `999` as the explicit sentinel meaning the ratio source was not used.
- Older CSV versions may use `0` in unused ratio columns, so those columns are ambiguous unless the row position identifies the active source.
- Values in `[0, 0.01]` are not out-of-range. They may be inaccurate for the expected sample, but they are not invalid.
- Out-of-range means `< 0` or `> 1`.
- For ratio precision, use absolute error:
  - odd rows: `abs(RatioPath - ExpectedRatio)`.
  - even rows: `abs(RatioRot - ExpectedRatio)`.

Use these statistics to find practical switching boundaries:

- Short `PathLength` can make path-based ratio less precise.
- Short `RotLength` can make rotation-based ratio less precise.
- If both `PathLength` and `RotLength` are very short and both absolute errors are high, classify the case as below ratio resolution rather than choosing either ratio source.
