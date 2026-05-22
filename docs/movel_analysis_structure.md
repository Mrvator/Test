# MoveL Analysis Structure

This workspace is organized so every ABB RobotStudio MoveL/autohoming CSV version can be analyzed the same way.

## Inputs

Place newly exported CSV logs in the workspace root, then rename them before analysis:

- `tests.csv`
- `success.csv`
- `pathl.csv`

Use the next version suffix, for example after `v14`:

```powershell
Rename-Item tests.csv tests_v15.csv
Rename-Item success.csv success_v15.csv
Rename-Item pathl.csv pathl_v15.csv
```

Example:

```powershell
python tools/analyze_movel_csv.py --version v15
```

## Workflow Files

- `skills/abb-movel-analysis/SKILL.md`: compact agent workflow for this analysis.
- `skills/abb-movel-analysis/references/schema.md`: column groups, pairing rules, and comparison logic.
- `config/movel_analysis_profile.json`: tolerances and report limits.
- `tools/analyze_movel_csv.py`: deterministic analyzer that generates Markdown.
- `tools/export_rapid_replay_module.py`: deterministic RAPID module exporter for replay targets.
- `reports/movel_analysis_<version>.md`: generated report for the versioned CSV files.
- `rapid/ReplayTargets_<version>.mod`: generated RAPID replay module for versioned replay targets.

## Current Core Checks

- `testId` coverage between `tests` and `success`.
- `C_rax*` vs `CalcC_rax*`.
- `C_rax*` vs `PathL_rax*`.
- `CalcC_rax*` vs `PathL_rax*`.
- Singular/unavailable short and long branch classification from `FinestStepS/L`, max sampled jump, `bOKshort/bOKlong`, and `stErrShort/stErrLong`.
- Selected `ControlShort_rax*`/`ControlLong_rax*` target vs `PathL_rax*`.
- PathL diagnostic anomaly statistics by `CfxOK`, `FoundBranch`, `PathDist`, and `Rotdist`.

The continuity rule is: if `FinestStepS/L <= 0.0001` and the matching max joint jump is greater than `60` degrees, the branch is unavailable and must report `stErrShort/stErrLong = SINGULAR`.

## Replay Export

Generate target declarations for successful tests:

```powershell
python tools/export_rapid_replay_module.py --version v15
```

The RAPID module uses scalar target declarations only. Target names include the CSV/test version to avoid collisions across exports:

- `rA_v15_t1`, `rB_v15_t1`
- `rB_v15_t1_c5` as `rB_v15_t1` with `B*_cf1/4/6/x` from `success_v15.csv`
- `jA_v15_t1`, `jB_v15_t1`, `jBseed_v15_t1`
- `seedB_v15_t1` when `tests_v15.csv` includes the `Bseed` PRNG input column

## Next Extensions

- Add Cartesian distance checks for the sampled continuous line trajectory.
- Add quaternion interpolation residuals for short/long branch selection.
- Add per-axis histograms once the current continuity checks are stable.
