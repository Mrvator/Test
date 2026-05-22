---
name: abb-movel-analysis
description: Analyze structured ABB RobotStudio MoveL/autohoming CSV logs across tests, success rows, PathL samples, predicted joint targets, singular branch classification, and PathRatio/RotRatio precision. Use when comparing C_rax, CalcC_rax, PathL_rax, ControlShort/ControlLong, FinestStepS/L, stErrShort/stErrLong, branch matches, continuous linear trajectory prediction behavior, PathL ratio accuracy, or thresholds for switching ratio calculation between path length and rotation length.
---

# ABB MoveL Analysis

## Use This Workflow

1. If the user uploaded fresh `tests.csv`, `success.csv`, and `pathl.csv`, rename them to the next version first, for example `tests_v15.csv`, `success_v15.csv`, and `pathl_v15.csv`.
2. Read `references/schema.md` when column meaning, pairing rules, or expected comparisons are unclear.
3. Run the deterministic analyzer:

```powershell
python tools/analyze_movel_csv.py --version v15
```

4. Review the generated report in `reports/movel_analysis_<version>.md`.
5. When the user asks for deeper investigation, use the report's anomaly tables as the entry points and inspect the matching `testId` rows in the CSV files.

## Default Analysis Questions

Always answer these first:

- Does every generated test have a matching success row?
- For each success row, does the actual end joint target `C_rax` match the predicted `CalcC_rax` within tolerance?
- Does `PathL_rax` match both `C_rax` and `CalcC_rax` within tolerance?
- Which interpolation branch won: `ControlMatchShort` or `ControlMatchLong`?
- Do branches that hit `FinestStepS/L <= 0.0001` with a max jump greater than 60 degrees report `stErrShort/stErrLong = SINGULAR`?
- Do PathL samples keep `CfxOK = TRUE` and `FoundBranch` equal to `branch S/L`?
- Which tests have large path distance or rotation distance residuals?
- How accurate is `RatioPath` on odd PathL rows versus `RatioRot` on even PathL rows?
- At what `PathLength`/`RotLength` ranges does one ratio source become unreliable enough to switch to the other source?
- Which cases are below practical ratio resolution because both `PathLength` and `RotLength` are too small?

## PathL Ratio Analysis

Use PathL ratio diagnostics to estimate decision boundaries for ratio calculation:

- Treat each `testId/confId/branch` PathL group as 100 pairs: odd rows are `PathRatio`, even rows are `RotRatio`.
- Treat zero ratio values as valid measured results. Do not infer missing data from `0`.
- From the new CSV convention onward, treat ratio value `999` as the explicit sentinel for "this ratio source was not used".
- Older CSV versions may still contain `0` in unused ratio columns, which is ambiguous because `0` can also be a real measured result.
- Compare odd-row `RatioPath` and even-row `RatioRot` against the expected sample ratio `(pairIndex + 1) / 100`.
- Use absolute error `abs(RatioPath - expected)` and `abs(RatioRot - expected)` when measuring precision.
- Flag out-of-range ratio only when the measured value is `< 0` or `> 1`; values between `0` and `0.01` are allowed.
- Summarize ratio precision by `PathLength` and `RotLength`, especially the shortest path and rotation groups.
- Look for the switch region where `RatioPath` error grows on short path lengths while `RatioRot` remains accurate, and the opposite region where rotation is too short.
- Mark cases where both `PathLength` and `RotLength` are too short as below ratio resolution instead of forcing a path-vs-rotation winner.

When reporting ratio behavior, prefer compact statistics over row dumps:

- Include `testId`, `confId`, `branch`, `PathLength`, and `RotLength`.
- For odd rows, report statistics of `abs(RatioPath - expected)`.
- For even rows, report statistics of `abs(RatioRot - expected)`.
- Use `n/min/mean/median/p95/max` unless the user asks for examples.

## File Roles

- `tests_<version>.csv`: generated input tests, branch predictions, finest step diagnostics, and branch errors.
- `success_<version>.csv`: successful RobotStudio runs and final/predicted joint target comparisons.
- `pathl_<version>.csv`: sampled PathL prediction diagnostics per `testId`, `confId`, and branch.
- `config/movel_analysis_profile.json`: tolerances and report limits.
- `tools/analyze_movel_csv.py`: repeatable analyzer.
- `tools/export_rapid_replay_module.py`: exports one RAPID target module for replaying successful tests.

## Replay Export

When the user needs to replay tests in RobotStudio, export a RAPID module:

```powershell
python tools/export_rapid_replay_module.py --version v15
```

Exported target declarations are scalar `CONST` values, not arrays:

- `rA_<version>_t<testId>` and `rB_<version>_t<testId>` as `robtarget`.
- `rB_<version>_t<testId>_c<confId>` as a copy of `rB_<version>_t<testId>` with `confdata` from `success_<version>.B*_cf1/4/6/x`.
- `jA_<version>_t<testId>`, `jB_<version>_t<testId>`, and `jBseed_<version>_t<testId>` as `jointtarget`.
- `bStarCf1_t<testId>_c<confId>`, `bStarCf4_t<testId>_c<confId>`, `bStarCf6_t<testId>_c<confId>`, and `bStarCfx_t<testId>_c<confId>` as `num`.

## Reporting Style

Keep reports concise and structured:

- Summary counts first.
- Then missing success rows and mismatch tables.
- Then singular branch classification and branch/control consistency.
- Then PathL sampling diagnostics.
- End with suggested next investigations by `testId`.

Do not rewrite CSVs. Treat source logs as immutable evidence.
