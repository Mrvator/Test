# ABB MoveL Analysis v11

## Summary

- Tests: 498
- Tests with success rows: 237
- Success rows: 312
- Tests missing success rows: 261
- PathL diagnostic rows: 64989
- PathL groups by test/conf/branch: 332
- Joint tolerance: 0.01 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Success Coverage

| missing testId |
| --- |
| 2 |
| 3 |
| 5 |
| 6 |
| 8 |
| 10 |
| 11 |
| 13 |
| 14 |
| 15 |
| 17 |
| 18 |
| 20 |
| 21 |
| 24 |
| 25 |
| 26 |
| 29 |
| 30 |
| 32 |
| 33 |
| 34 |
| 35 |
| 36 |
| 38 |
| 39 |
| 41 |
| 42 |
| 43 |
| 44 |
| 45 |
| 47 |
| 48 |
| 49 |
| 52 |
| 54 |
| 55 |
| 57 |
| 59 |
| 60 |
... 221 more omitted by report limit.

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 6
- CalcC/PathL mismatches: 6
- Worst valid delta: test 413, C vs CalcC, axis 1, 0.004100 deg

| testId | confId | comparison | max abs deg | axis | control branch |
| --- | --- | --- | --- | --- | --- |
| 68 | 4 | C vs PathL | n/a | n/a | none |
| 68 | 4 | CalcC vs PathL | n/a | n/a | none |
| 230 | 5 | C vs PathL | n/a | n/a | none |
| 230 | 5 | CalcC vs PathL | n/a | n/a | none |
| 361 | 5 | C vs PathL | n/a | n/a | none |
| 361 | 5 | CalcC vs PathL | n/a | n/a | none |
| 392 | 2 | C vs PathL | n/a | n/a | none |
| 392 | 2 | CalcC vs PathL | n/a | n/a | none |
| 396 | 7 | C vs PathL | n/a | n/a | none |
| 396 | 7 | CalcC vs PathL | n/a | n/a | none |
| 488 | 5 | C vs PathL | n/a | n/a | none |
| 488 | 5 | CalcC vs PathL | n/a | n/a | none |

## Branch Matching

- Control branch counts: S=193, L=113, none=6
- Legacy/control flag differences: 12
- Selected control target mismatches: 0

### Legacy vs Control Differences

| testId | confId | MatchesShort | MatchesLong | ControlMatchShort | ControlMatchLong |
| --- | --- | --- | --- | --- | --- |
| 56 | 5 | False | False | True | False |
| 68 | 4 | True | False | False | False |
| 108 | 3 | False | False | False | True |
| 129 | 5 | False | False | False | True |
| 230 | 5 | False | True | False | False |
| 267 | 7 | False | False | True | False |
| 303 | 5 | False | False | False | True |
| 361 | 5 | False | True | False | False |
| 392 | 2 | False | True | False | False |
| 392 | 5 | True | False | True | True |
| 396 | 7 | False | True | False | False |
| 488 | 5 | True | False | False | False |

### Control Target Mismatches

None.

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 1108
- Mean PathDist: 10.5410
- Max PathDist: 2786.880
- Mean Rotdist: 1.6641
- Max Rotdist: 179.994

### PathL Anomalies

| testId | confId | branch | found | CfxOK | PathDist | Rotdist |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | 4 | L | S | TRUE | 0.131822 | 3.5741 |
| 29 | 4 | L | S | TRUE | 2786.880 | 177.467 |
| 29 | 4 | L | S | TRUE | 0.121077 | 7.1765 |
| 29 | 4 | L | S | TRUE | 2758.730 | 179.311 |
| 29 | 4 | L | S | TRUE | 0.107736 | 10.7795 |
| 29 | 4 | L | S | TRUE | 2730.570 | 178.845 |
| 29 | 4 | L | S | TRUE | 0.128193 | 14.3728 |
| 29 | 4 | L | S | TRUE | 2702.430 | 177.001 |
| 29 | 4 | L | S | TRUE | 0.113544 | 17.9767 |
| 29 | 4 | L | S | TRUE | 2674.270 | 175.158 |
| 29 | 4 | L | S | TRUE | 0.097936 | 21.5803 |
| 29 | 4 | L | S | TRUE | 2646.120 | 173.314 |
| 29 | 4 | L | S | TRUE | 0.115991 | 25.1746 |
| 29 | 4 | L | S | TRUE | 2617.970 | 171.470 |
| 29 | 4 | L | S | TRUE | 0.099285 | 28.7787 |
| 29 | 4 | L | S | TRUE | 2589.820 | 169.626 |
| 29 | 4 | L | S | TRUE | 0.116326 | 32.3729 |
| 29 | 4 | L | S | TRUE | 2561.680 | 167.783 |
| 29 | 4 | L | S | TRUE | 0.098513 | 35.9779 |
| 29 | 4 | L | S | TRUE | 2533.520 | 165.939 |
| 29 | 4 | L | S | TRUE | 0.115467 | 39.5717 |
| 29 | 4 | L | S | TRUE | 2505.380 | 164.095 |
| 29 | 4 | L | S | TRUE | 0.098175 | 43.1774 |
| 29 | 4 | L | S | TRUE | 2477.220 | 162.251 |
| 29 | 4 | L | S | TRUE | 0.134032 | 46.7669 |
| 29 | 4 | L | S | TRUE | 2449.080 | 160.408 |
| 29 | 4 | L | S | TRUE | 0.069488 | 50.3979 |
| 29 | 4 | L | S | TRUE | 2420.910 | 158.564 |
| 54 | 5 | L | S | TRUE | 0.028378 | 3.5905 |
| 54 | 5 | L | S | TRUE | 1185.970 | 128.489 |
| 63 | 8 | L | S | TRUE | 0.181157 | 3.5796 |
| 63 | 8 | L | S | TRUE | 1829.990 | 100.754 |
| 63 | 8 | L | S | TRUE | 0.236412 | 7.1673 |
| 63 | 8 | L | S | TRUE | 1811.530 | 103.374 |
| 63 | 8 | L | S | TRUE | 0.222064 | 10.7690 |
| 63 | 8 | L | S | TRUE | 1793.040 | 105.992 |
| 63 | 8 | L | S | TRUE | 0.209159 | 14.3707 |
| 63 | 8 | L | S | TRUE | 1774.550 | 108.611 |
| 63 | 8 | L | S | TRUE | 0.197685 | 17.9725 |
| 63 | 8 | L | S | TRUE | 1756.060 | 111.229 |
... 1068 more omitted by report limit.

### Worst PathDist By Test

| testId | max PathDist |
| --- | --- |
| 29 | 2786.880 |
| 130 | 2594.170 |
| 365 | 2431.430 |
| 230 | 2333.030 |
| 112 | 2209.350 |
| 361 | 2152.780 |
| 329 | 2139.250 |
| 396 | 2007.500 |
| 63 | 1829.990 |
| 421 | 1746.030 |

### Worst Rotdist By Test

| testId | max Rotdist |
| --- | --- |
| 392 | 179.994 |
| 396 | 179.984 |
| 130 | 179.969 |
| 421 | 179.932 |
| 361 | 179.907 |
| 112 | 179.842 |
| 230 | 179.659 |
| 29 | 179.311 |
| 63 | 163.602 |
| 329 | 139.189 |

## Suggested Next Investigations

- Inspect missing success rows first; these are failed or unrecorded MoveL executions.
- For joint mismatches, compare the reported axis against RAPID configuration changes and quaternion branch choice.
- For PathL anomalies, inspect the same `testId/confId/branch` in the raw PathL rows and verify branch interpolation state.
