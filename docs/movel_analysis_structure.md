# MoveL Analysis Structure

This workspace is organized so every ABB RobotStudio MoveL/autohoming CSV version can be analyzed the same way.

## Inputs

Place versioned CSV logs in the workspace root:

- `tests_<version>.csv`
- `success_<version>.csv`
- `pathl_<version>.csv`

Example:

```powershell
python tools/analyze_movel_csv.py --version v11
```

## Workflow Files

- `skills/abb-movel-analysis/SKILL.md`: compact agent workflow for this analysis.
- `skills/abb-movel-analysis/references/schema.md`: column groups, pairing rules, and comparison logic.
- `config/movel_analysis_profile.json`: tolerances and report limits.
- `tools/analyze_movel_csv.py`: deterministic analyzer that generates Markdown.
- `tools/export_rapid_replay_module.py`: deterministic RAPID module exporter for replay targets.
- `reports/movel_analysis_<version>.md`: generated report for a specific CSV suffix.
- `rapid/ReplayTargets_<version>.mod`: generated RAPID replay module.

## Current Core Checks

- `testId` coverage between `tests` and `success`.
- `C_rax*` vs `CalcC_rax*`.
- `C_rax*` vs `PathL_rax*`.
- `CalcC_rax*` vs `PathL_rax*`.
- Selected `ControlShort_rax*`/`ControlLong_rax*` target vs `PathL_rax*`.
- Legacy `MatchesShort/MatchesLong` vs newer `ControlMatchShort/ControlMatchLong`.
- PathL diagnostic anomalies by `CfxOK`, `FoundBranch`, `PathDist`, and `Rotdist`.

## Replay Export

Generate target declarations for successful tests:

```powershell
python tools/export_rapid_replay_module.py --version v11
```

The RAPID module uses scalar target declarations only. Target names include the CSV/test version to avoid collisions across exports:

- `rA_v11_t1`, `rB_v11_t1`
- `rB_v11_t1_c5` as `rB_v11_t1` with `B*_cf1/4/6/x` from `success_v11.csv`
- `jA_v11_t1`, `jB_v11_t1`, `jBseed_v11_t1`
- `seedB_v11_t1` when `tests_<version>.csv` includes the `Bseed` PRNG input column

## Next Extensions

- Add Cartesian distance checks for the sampled continuous line trajectory.
- Add quaternion interpolation residuals for short/long branch selection.
- Add per-axis histograms once enough versions are available for trend comparison.
- Add a cross-version comparison report, for example `v11` vs `v12`.
