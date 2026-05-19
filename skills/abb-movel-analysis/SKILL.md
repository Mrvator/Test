---
name: abb-movel-analysis
description: Analyze structured ABB RobotStudio MoveL/autohoming CSV logs across tests, success rows, PathL samples, predicted joint targets, and singular branch classification. Use when comparing C_rax, CalcC_rax, PathL_rax, ControlShort/ControlLong, FinestStepS/L, stErrShort/stErrLong, branch matches, or continuous linear trajectory prediction behavior.
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
