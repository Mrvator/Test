# ABB MoveL Analysis v13

## Summary

- Tests: 1182
- Tests with success rows: 548
- Success rows: 729
- Tests missing success rows: 634
- PathL diagnostic rows: 152494
- PathL groups by test/conf/branch: 780
- Joint tolerance: 0.01 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Success Coverage

| missing testId |
| --- |
| 5 |
| 6 |
| 8 |
| 10 |
| 11 |
| 13 |
| 15 |
| 19 |
| 20 |
| 24 |
| 29 |
| 31 |
| 32 |
| 33 |
| 35 |
| 36 |
| 37 |
| 38 |
| 39 |
| 42 |
| 44 |
| 45 |
| 47 |
| 51 |
| 53 |
| 54 |
| 56 |
| 61 |
| 62 |
| 63 |
| 65 |
| 66 |
| 67 |
| 69 |
| 70 |
| 71 |
| 74 |
| 76 |
| 77 |
| 78 |
... 594 more omitted by report limit.

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 15
- CalcC/PathL mismatches: 15
- Worst valid delta: test 1162, C vs CalcC, axis 1, 0.004885 deg

| testId | confId | comparison | max abs deg | axis | control branch |
| --- | --- | --- | --- | --- | --- |
| 72 | 2 | C vs PathL | n/a | n/a | none |
| 72 | 2 | CalcC vs PathL | n/a | n/a | none |
| 154 | 1 | C vs PathL | n/a | n/a | none |
| 154 | 1 | CalcC vs PathL | n/a | n/a | none |
| 168 | 4 | C vs PathL | n/a | n/a | none |
| 168 | 4 | CalcC vs PathL | n/a | n/a | none |
| 234 | 4 | C vs PathL | n/a | n/a | none |
| 234 | 4 | CalcC vs PathL | n/a | n/a | none |
| 377 | 4 | C vs PathL | n/a | n/a | none |
| 377 | 4 | CalcC vs PathL | n/a | n/a | none |
| 552 | 3 | C vs PathL | n/a | n/a | none |
| 552 | 3 | CalcC vs PathL | n/a | n/a | none |
| 558 | 2 | C vs PathL | n/a | n/a | none |
| 558 | 2 | CalcC vs PathL | n/a | n/a | none |
| 610 | 4 | C vs PathL | n/a | n/a | none |
| 610 | 4 | CalcC vs PathL | n/a | n/a | none |
| 614 | 8 | C vs PathL | n/a | n/a | none |
| 614 | 8 | CalcC vs PathL | n/a | n/a | none |
| 686 | 2 | C vs PathL | n/a | n/a | none |
| 686 | 2 | CalcC vs PathL | n/a | n/a | none |
| 855 | 7 | C vs PathL | n/a | n/a | none |
| 855 | 7 | CalcC vs PathL | n/a | n/a | none |
| 859 | 8 | C vs PathL | n/a | n/a | none |
| 859 | 8 | CalcC vs PathL | n/a | n/a | none |
| 951 | 1 | C vs PathL | n/a | n/a | none |
| 951 | 1 | CalcC vs PathL | n/a | n/a | none |
| 1027 | 5 | C vs PathL | n/a | n/a | none |
| 1027 | 5 | CalcC vs PathL | n/a | n/a | none |
| 1145 | 5 | C vs PathL | n/a | n/a | none |
| 1145 | 5 | CalcC vs PathL | n/a | n/a | none |

## Branch Matching

- Control branch counts: S=454, L=260, none=15
- Legacy/control flag differences: 30
- Selected control target mismatches: 0

### Legacy vs Control Differences

| testId | confId | MatchesShort | MatchesLong | ControlMatchShort | ControlMatchLong |
| --- | --- | --- | --- | --- | --- |
| 72 | 2 | False | True | False | False |
| 72 | 5 | True | False | True | True |
| 154 | 1 | False | True | False | False |
| 168 | 4 | True | False | False | False |
| 234 | 4 | True | False | False | False |
| 333 | 4 | False | False | True | False |
| 369 | 2 | False | False | True | False |
| 377 | 4 | False | True | False | False |
| 510 | 5 | True | False | True | True |
| 516 | 5 | False | False | True | False |
| 516 | 8 | False | False | False | True |
| 552 | 3 | True | False | False | False |
| 558 | 2 | False | True | False | False |
| 610 | 1 | True | False | True | True |
| 610 | 4 | False | True | False | False |
| 614 | 8 | True | False | False | False |
| 641 | 5 | False | False | True | False |
| 686 | 2 | True | False | False | False |
| 745 | 2 | False | False | True | False |
| 767 | 5 | False | False | True | False |
| 855 | 7 | True | False | False | False |
| 859 | 8 | False | True | False | False |
| 951 | 1 | False | True | False | False |
| 951 | 4 | True | False | True | True |
| 982 | 5 | False | False | True | False |
| 1019 | 5 | False | False | True | False |
| 1027 | 5 | False | True | False | False |
| 1083 | 5 | False | False | True | False |
| 1145 | 2 | True | False | True | True |
| 1145 | 5 | False | True | False | False |

### Control Target Mismatches

None.

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 3500
- Mean PathDist: 14.6372
- Max PathDist: 4288.400
- Mean Rotdist: 2.2346
- Max Rotdist: 179.987

### PathL Anomalies

| testId | confId | branch | found | CfxOK | PathDist | Rotdist |
| --- | --- | --- | --- | --- | --- | --- |
| 51 | 3 | L | S | TRUE | 0.265642 | 3.5796 |
| 51 | 3 | L | S | TRUE | 1920.510 | 78.6184 |
| 51 | 3 | L | S | TRUE | 0.286162 | 7.1776 |
| 51 | 3 | L | S | TRUE | 1901.110 | 81.4606 |
| 51 | 3 | L | S | TRUE | 0.217853 | 10.7864 |
| 51 | 3 | L | S | TRUE | 1881.680 | 84.3021 |
| 66 | 5 | L | S | TRUE | 0.219653 | 3.5234 |
| 66 | 5 | L | S | TRUE | 153.110 | 40.4554 |
| 66 | 5 | L | S | TRUE | 0.215605 | 7.1223 |
| 66 | 5 | L | S | TRUE | 151.563 | 43.6832 |
| 66 | 5 | L | S | TRUE | 0.157832 | 10.7445 |
| 66 | 5 | L | S | TRUE | 150.010 | 46.9110 |
| 66 | 5 | L | S | TRUE | 0.169467 | 14.3373 |
| 66 | 5 | L | S | TRUE | 148.465 | 50.1387 |
| 66 | 5 | L | S | TRUE | 0.201873 | 17.9177 |
| 66 | 5 | L | S | TRUE | 146.924 | 53.3663 |
| 66 | 5 | L | S | TRUE | 0.171664 | 21.5333 |
| 66 | 5 | L | S | TRUE | 145.374 | 56.5941 |
| 66 | 5 | L | S | TRUE | 0.187784 | 25.1195 |
| 66 | 5 | L | S | TRUE | 143.832 | 59.8218 |
| 66 | 5 | L | S | TRUE | 0.156092 | 28.7366 |
| 66 | 5 | L | S | TRUE | 142.281 | 63.0496 |
| 66 | 5 | L | S | TRUE | 0.171033 | 32.3252 |
| 66 | 5 | L | S | TRUE | 140.738 | 66.2773 |
| 66 | 5 | L | S | TRUE | 0.186157 | 35.9135 |
| 66 | 5 | L | S | TRUE | 139.196 | 69.5049 |
| 66 | 5 | L | S | TRUE | 0.152036 | 39.5341 |
| 66 | 5 | L | S | TRUE | 137.643 | 72.7327 |
| 66 | 5 | L | S | TRUE | 0.160280 | 43.1261 |
| 66 | 5 | L | S | TRUE | 136.099 | 75.9604 |
| 66 | 5 | L | S | TRUE | 0.170315 | 46.7181 |
| 66 | 5 | L | S | TRUE | 134.555 | 79.1880 |
| 66 | 5 | L | S | TRUE | 0.181261 | 50.3105 |
| 66 | 5 | L | S | TRUE | 133.013 | 82.4156 |
| 66 | 5 | L | S | TRUE | 0.141310 | 53.9352 |
| 66 | 5 | L | S | TRUE | 131.457 | 85.6436 |
| 66 | 5 | L | S | TRUE | 0.145795 | 57.5311 |
| 66 | 5 | L | S | TRUE | 129.912 | 88.8713 |
| 66 | 5 | L | S | TRUE | 0.149407 | 61.1278 |
| 66 | 5 | L | S | TRUE | 128.383 | 92.0984 |
... 3559 more omitted by report limit.

### Worst PathDist By Test

| testId | max PathDist |
| --- | --- |
| 109 | 4288.400 |
| 249 | 3613.780 |
| 1149 | 3575.350 |
| 1053 | 3106.570 |
| 610 | 3037.110 |
| 272 | 2935.360 |
| 584 | 2872.260 |
| 84 | 2846.250 |
| 459 | 2818.510 |
| 668 | 2809.130 |

### Worst Rotdist By Test

| testId | max Rotdist |
| --- | --- |
| 459 | 179.987 |
| 1027 | 179.975 |
| 610 | 179.973 |
| 668 | 179.959 |
| 951 | 179.959 |
| 672 | 179.949 |
| 1149 | 179.948 |
| 584 | 179.942 |
| 1145 | 179.939 |
| 510 | 179.925 |

## Suggested Next Investigations

- Inspect missing success rows first; these are failed or unrecorded MoveL executions.
- For joint mismatches, compare the reported axis against RAPID configuration changes and quaternion branch choice.
- For PathL anomalies, inspect the same `testId/confId/branch` in the raw PathL rows and verify branch interpolation state.
