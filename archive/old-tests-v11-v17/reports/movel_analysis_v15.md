# ABB MoveL Analysis v15

## Summary

- Tests: 7
- Tests with success rows: 6
- Success rows: 7
- Tests missing success rows: 1
- PathL diagnostic rows: 1400
- PathL groups by test/conf/branch: 7
- Joint tolerance: 0.01 deg
- Finest step singular limit: 0.000100
- Max allowed joint jump: 60.0000 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Success Coverage

| missing testId |
| --- |
| 7 |

## Singular Branch Classification

- Expected singular branches from finest-step/jump rule: S=0, L=0
- Reported `stErr* = SINGULAR`: S=0, L=0
- Rule/status mismatches: 0

None.

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 0
- CalcC/PathL mismatches: 0
- Worst valid delta: test 1, C vs CalcC, axis 1, 0.001500 deg

None.

## Branch Matching

- Control branch counts: S=5, L=2, none=0
- Selected control target mismatches: 0

### Control Target Mismatches

None.

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 0
- Mean PathDist: 0.108258
- Max PathDist: 0.497020
- Mean Rotdist: 0.019053
- Max Rotdist: 0.137056

### PathL Anomalies

None.

### Worst PathDist By Test

| testId | max PathDist |
| --- | --- |
| 6 | 0.497020 |
| 2 | 0.480036 |
| 4 | 0.456330 |
| 1 | 0.344860 |
| 3 | 0.333549 |
| 5 | 0.237451 |

### Worst Rotdist By Test

| testId | max Rotdist |
| --- | --- |
| 3 | 0.137056 |
| 1 | 0.088469 |
| 2 | 0.079129 |
| 4 | 0.068528 |
| 5 | 0.055953 |
| 6 | 0.055953 |

## Suggested Next Investigations

- Inspect missing success rows first; these are failed or unrecorded MoveL executions.
- For joint mismatches, compare the reported axis against RAPID configuration changes and quaternion branch choice.
- For PathL anomalies, inspect the same `testId/confId/branch` in the raw PathL rows and verify branch interpolation state.
