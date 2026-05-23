# ABB MoveL Analysis v21

## Summary

- Tests: 5098
- Tests with success rows: 4664
- Success rows: 5376
- Tests without success rows: 434
- PathL diagnostic rows: 1449646
- PathL groups by test/conf/branch: 8886
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Test Length Distribution

`successful testIds` means a `testId` has at least one row in `success.csv`; `successful test/conf rows` uses every successful `success.csv` row. `unsuccessful testIds` means no success row exists for that `testId`.
Lengths prefer logged `pathl.csv` values for matching `testId/confId` when present and fall back to A/B pose calculation from `tests.csv` otherwise.

| sample | rows | PathLength min | PathLength mean | PathLength median | PathLength p95 | PathLength max | RotLength min | RotLength mean | RotLength median | RotLength p95 | RotLength max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all testIds | 5098 | 1.2062 | 9.5830 | 9.7617 | 13.8075 | 16.4037 | 0.193827 | 2.1517 | 0.972763 | 1.3757 | 359.322 |
| successful testIds | 4664 | 1.2062 | 9.6128 | 9.7709 | 13.8379 | 16.4037 | 0.193827 | 1.4178 | 0.970347 | 1.3751 | 180.000 |
| successful test/conf rows | 5376 | 1.2062 | 9.5947 | 9.7660 | 13.7969 | 16.4037 | 0.193827 | 1.7546 | 0.969136 | 1.3671 | 359.166 |
| unsuccessful testIds | 434 | 1.8728 | 9.2626 | 9.4287 | 13.6550 | 15.9083 | 0.219333 | 10.0380 | 0.974695 | 1.4223 | 359.322 |

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=4593, L=2044
- Found branches without matching successful control branch: S=62, L=2032

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 4593 | 62 | 1.3499 | 0.200000 | 0.200000 | 0.200000 | 0.074327 | 0.570120 | 1350.000 |
| L | 2044 | 2032 | 99.4129 | 0.200000 | 0.200000 | 0.200000 | 0.028736 | 0.236248 | 1193.840 |

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 4664 | 0.100000 | 0.199979 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 62 | 0.000100 | 0.185485 | 0.200000 | 0.200000 | 0.200000 |
| L successful | 12 | 0.000781 | 0.001628 | 0.001563 | 0.003125 | 0.003125 |
| L found unsuccessful | 2032 | 0.000100 | 0.191928 | 0.200000 | 0.200000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 700
- CalcC/PathL mismatches: 700
- Worst valid delta: test 2231, C vs CalcC, axis 6, 0.232800 deg

| testId | confId | comparison | max abs deg | axis | control branch |
| --- | --- | --- | --- | --- | --- |
| 4 | 7 | C vs PathL | n/a | n/a | none |
| 4 | 7 | CalcC vs PathL | n/a | n/a | none |
| 7 | 8 | C vs PathL | n/a | n/a | none |
| 7 | 8 | CalcC vs PathL | n/a | n/a | none |
| 20 | 4 | C vs PathL | n/a | n/a | none |
| 20 | 4 | CalcC vs PathL | n/a | n/a | none |
| 37 | 5 | C vs PathL | n/a | n/a | none |
| 37 | 5 | CalcC vs PathL | n/a | n/a | none |
| 48 | 8 | C vs PathL | n/a | n/a | none |
| 48 | 8 | CalcC vs PathL | n/a | n/a | none |
| 55 | 1 | C vs PathL | n/a | n/a | none |
| 55 | 1 | CalcC vs PathL | n/a | n/a | none |
| 66 | 4 | C vs PathL | n/a | n/a | none |
| 66 | 4 | CalcC vs PathL | n/a | n/a | none |
| 81 | 5 | C vs PathL | n/a | n/a | none |
| 81 | 5 | CalcC vs PathL | n/a | n/a | none |
| 87 | 4 | C vs PathL | n/a | n/a | none |
| 87 | 4 | CalcC vs PathL | n/a | n/a | none |
| 90 | 2 | C vs PathL | n/a | n/a | none |
| 90 | 2 | CalcC vs PathL | n/a | n/a | none |
| 101 | 6 | C vs PathL | n/a | n/a | none |
| 101 | 6 | CalcC vs PathL | n/a | n/a | none |
| 105 | 2 | C vs PathL | n/a | n/a | none |
| 105 | 2 | CalcC vs PathL | n/a | n/a | none |
| 118 | 1 | C vs PathL | n/a | n/a | none |
| 118 | 1 | CalcC vs PathL | n/a | n/a | none |
| 127 | 5 | C vs PathL | n/a | n/a | none |
| 127 | 5 | CalcC vs PathL | n/a | n/a | none |
| 134 | 9 | C vs PathL | n/a | n/a | none |
| 134 | 9 | CalcC vs PathL | n/a | n/a | none |
| 142 | 8 | C vs PathL | n/a | n/a | none |
| 142 | 8 | CalcC vs PathL | n/a | n/a | none |
| 163 | 4 | C vs PathL | n/a | n/a | none |
| 163 | 4 | CalcC vs PathL | n/a | n/a | none |
| 166 | 5 | C vs PathL | n/a | n/a | none |
| 166 | 5 | CalcC vs PathL | n/a | n/a | none |
| 178 | 5 | C vs PathL | n/a | n/a | none |
| 178 | 5 | CalcC vs PathL | n/a | n/a | none |
| 182 | 4 | C vs PathL | n/a | n/a | none |
| 182 | 4 | CalcC vs PathL | n/a | n/a | none |
... 1360 more omitted by report limit.

## Branch Matching

- Control branch counts: S=4664, L=12, none=700
- ControlMatchShort XOR ControlMatchLong violations: 5207
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=4528, L=648, none=200
- Legacy/control branch disagreements: 772
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

| testId | confId | ControlMatchShort | ControlMatchLong |
| --- | --- | --- | --- |
| 1 | 5 | True | True |
| 2 | 2 | True | True |
| 3 | 4 | True | True |
| 4 | 4 | True | True |
| 4 | 7 | False | False |
| 5 | 8 | True | True |
| 7 | 5 | True | True |
| 7 | 8 | False | False |
| 8 | 8 | True | True |
| 9 | 7 | True | True |
| 10 | 4 | True | True |
| 13 | 5 | True | True |
| 14 | 5 | True | True |
| 15 | 2 | True | True |
| 16 | 8 | True | True |
| 17 | 9 | True | True |
| 18 | 2 | True | True |
| 19 | 4 | True | True |
| 20 | 1 | True | True |
| 20 | 4 | False | False |
| 21 | 8 | True | True |
| 22 | 8 | True | True |
| 23 | 1 | True | True |
| 24 | 5 | True | True |
| 25 | 5 | True | True |
| 27 | 6 | True | True |
| 28 | 4 | True | True |
| 29 | 2 | True | True |
| 30 | 2 | True | True |
| 31 | 6 | True | True |
| 32 | 9 | True | True |
| 35 | 2 | True | True |
| 36 | 2 | True | True |
| 37 | 4 | True | True |
| 37 | 5 | False | False |
| 38 | 7 | True | True |
| 40 | 5 | True | True |
| 41 | 5 | True | True |
| 42 | 4 | True | True |
| 44 | 4 | True | True |
... 5167 more omitted by report limit.

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 12 |
| S | S | 4528 |
| S | none | 136 |
| none | L | 636 |
| none | none | 64 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 4664 | 0.000490 | 0.000169 | 0.001021 | 0.173403 | 0.200000 |
| S ControlMaxAx4 successful | 4664 | 0.002995 | 0.001159 | 0.010624 | 0.436174 | 0.100000 |
| S ControlMaxAx6 successful | 4664 | 0.002896 | 0.001121 | 0.010354 | 0.396823 | 0.100000 |
| S ControlMaxAx1 unsuccessful | 434 | 0.000296 | 0.000152 | 0.000702 | 0.011853 | 0.200000 |
| S ControlMaxAx4 unsuccessful | 434 | 3.1335 | 0.001478 | 0.119858 | 1350.000 | 0.000100 |
| S ControlMaxAx6 unsuccessful | 434 | 3.1336 | 0.001583 | 0.119460 | 1350.000 | 0.000100 |
| L ControlMaxAx1 successful | 12 | 3.0204 | 2.0401 | 15.4798 | 15.4798 | 0.000781 |
| L ControlMaxAx4 successful | 12 | 31.5348 | 31.3190 | 46.1079 | 46.1079 | 0.000781 |
| L ControlMaxAx6 successful | 12 | 30.2626 | 31.8286 | 38.2464 | 38.2464 | 0.001563 |
| L ControlMaxAx1 unsuccessful | 5086 | 10.5163 | 0.001170 | 0.084430 | 1555.330 | 0.000100 |
| L ControlMaxAx4 unsuccessful | 5086 | 18.5271 | 0.026824 | 0.906769 | 1789.370 | 0.000100 |
| L ControlMaxAx6 unsuccessful | 5086 | 15.9460 | 0.025877 | 0.810534 | 1742.360 | 0.000100 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 14028 | 0.065395 | 0.000610 | 0.008224 | 47.3573 | 517 | L | Ax6 | 3.5084 | 46.3145 | 47.3573 |
| found unsuccessful | 6282 | 31.1940 | 28.4246 | 95.0646 | 179.843 | 3610 | L | Ax6 | 2.3246 | 173.317 | 179.843 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 517 | L | 3.5084 | 46.3145 | 47.3573 | Ax6 | 47.3573 | 0.001563 | empty |
| successful | 3147 | L | 15.9230 | 45.3246 | 34.7195 | Ax4 | 45.3246 | 0.000781 | empty |
| successful | 2487 | L | 2.6084 | 43.0410 | 40.4801 | Ax4 | 43.0410 | 0.001563 | empty |
| successful | 4169 | L | 0.956070 | 39.7013 | 39.9447 | Ax6 | 39.9447 | 0.001563 | empty |
| successful | 2408 | L | 2.9617 | 38.5646 | 38.7349 | Ax6 | 38.7349 | 0.001563 | empty |
| successful | 3802 | L | 3.0950 | 35.8892 | 36.8179 | Ax6 | 36.8179 | 0.001563 | empty |
| successful | 5031 | L | 1.9754 | 35.4669 | 35.8183 | Ax6 | 35.8183 | 0.001563 | empty |
| successful | 4057 | L | 1.7733 | 33.0661 | 35.2492 | Ax6 | 35.2492 | 0.001563 | empty |
| successful | 2992 | L | 1.1307 | 30.8952 | 28.4871 | Ax4 | 30.8952 | 0.001563 | empty |
| successful | 1628 | L | 2.0333 | 28.8278 | 28.1480 | Ax4 | 28.8278 | 0.001563 | empty |
| found unsuccessful | 3610 | L | 2.3246 | 173.317 | 179.843 | Ax6 | 179.843 | 0.200000 | empty |
| found unsuccessful | 4541 | L | 2.1629 | 163.323 | 179.197 | Ax6 | 179.197 | 0.200000 | empty |
| found unsuccessful | 3791 | L | 3.4121 | 69.7192 | 179.007 | Ax6 | 179.007 | 0.200000 | empty |
| found unsuccessful | 4485 | L | 1.9184 | 178.976 | 170.432 | Ax4 | 178.976 | 0.200000 | empty |
| found unsuccessful | 370 | L | 2.4650 | 178.713 | 177.600 | Ax4 | 178.713 | 0.200000 | empty |
| found unsuccessful | 2213 | L | 8.7050 | 178.145 | 157.030 | Ax4 | 178.145 | 0.200000 | empty |
| found unsuccessful | 4602 | L | 1.4560 | 177.854 | 129.978 | Ax4 | 177.854 | 0.200000 | empty |
| found unsuccessful | 1597 | L | 2.0814 | 177.741 | 148.702 | Ax4 | 177.741 | 0.200000 | empty |
| found unsuccessful | 5058 | L | 1.6163 | 171.921 | 177.484 | Ax6 | 177.484 | 0.200000 | empty |
| found unsuccessful | 2742 | L | 1.3216 | 120.414 | 177.352 | Ax6 | 177.352 | 0.200000 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 4592 | 0.000525 | 0.000179 | 0.001056 | 0.212753 |
| S legacy WinAx1 | 4592 | 0.005171 | 0.001709 | 0.010483 | 2.1198 |
| S legacy Win2Ax1 | 4592 | 0.050812 | 0.017002 | 0.104645 | 19.7113 |
| S legacy MaxAx4 | 4592 | 0.005298 | 0.001221 | 0.014755 | 1.1206 |
| S legacy WinAx4 | 4592 | 0.052054 | 0.011876 | 0.145081 | 11.1708 |
| S legacy Win2Ax4 | 4592 | 0.487307 | 0.118222 | 1.3866 | 88.7412 |
| S legacy MaxAx6 | 4592 | 0.005198 | 0.001183 | 0.014008 | 1.1201 |
| S legacy WinAx6 | 4592 | 0.051035 | 0.011561 | 0.137741 | 11.1666 |
| S legacy Win2Ax6 | 4592 | 0.477139 | 0.114715 | 1.3279 | 88.6994 |
| L legacy MaxAx1 | 95 | 4.7852 | 2.1801 | 11.8952 | 156.862 |
| L legacy WinAx1 | 95 | 9.4142 | 6.0209 | 23.7873 | 143.666 |
| L legacy Win2Ax1 | 95 | 8.0386 | 5.1747 | 18.5067 | 133.466 |
| L legacy MaxAx4 | 95 | 49.9817 | 34.8939 | 173.671 | 178.713 |
| L legacy WinAx4 | 95 | 141.925 | 144.724 | 163.389 | 182.820 |
| L legacy Win2Ax4 | 95 | 173.567 | 168.914 | 251.998 | 262.392 |
| L legacy MaxAx6 | 95 | 48.8622 | 34.8559 | 167.606 | 177.600 |
| L legacy WinAx6 | 95 | 141.564 | 143.287 | 161.589 | 171.890 |
| L legacy Win2Ax6 | 95 | 173.126 | 167.815 | 249.457 | 266.308 |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 4592 | 0.996121 | 0.996252 | 0.998573 |
| S | 4 | 4592 | 0.986791 | 0.988776 | 0.993297 |
| S | 6 | 4592 | 0.986641 | 0.988649 | 0.993177 |
| L | 1 | 95 | 0.142610 | 0.373467 | 0.293409 |
| L | 4 | 95 | -0.662917 | 0.589034 | 0.445972 |
| L | 6 | 95 | -0.620064 | 0.613127 | 0.418562 |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 514446
- Groups with row count != 200: 3073
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 724823
- Ratio pair/order issues: 723840
- Mean PathDist: 1.1240
- Max PathDist: 16.1626
- Mean Rotdist: 1.0571
- Max Rotdist: 180.000

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 724823 | 0.013932 | 0.005169 | 0.056074 | 0.908923 |
| PathDist measured from RotRatio rows | 724823 | 2.2341 | 0.057411 | 9.6781 | 16.1626 |
| Rotdist measured from PathRatio rows | 724823 | 0.966738 | 0.000000 | 2.9412 | 180.000 |
| Rotdist measured from RotRatio rows | 724823 | 1.1474 | 0.000000 | 3.3958 | 179.874 |

### PathL Sample Group Issues

| testId | confId | branch | rows | expected |
| --- | --- | --- | --- | --- |
| 1 | 5 | L | 98 | 200 |
| 2 | 2 | L | 98 | 200 |
| 3 | 4 | L | 54 | 200 |
| 5 | 8 | L | 94 | 200 |
| 8 | 8 | L | 98 | 200 |
| 10 | 4 | L | 98 | 200 |
| 13 | 5 | L | 98 | 200 |
| 14 | 5 | L | 98 | 200 |
| 15 | 2 | L | 98 | 200 |
| 16 | 8 | L | 98 | 200 |
| 17 | 9 | L | 70 | 200 |
| 18 | 2 | L | 98 | 200 |
| 19 | 4 | L | 98 | 200 |
| 22 | 8 | L | 2 | 200 |
| 23 | 1 | L | 88 | 200 |
| 24 | 5 | L | 98 | 200 |
| 25 | 5 | L | 98 | 200 |
| 27 | 6 | L | 98 | 200 |
| 28 | 4 | L | 98 | 200 |
| 29 | 2 | L | 98 | 200 |
| 30 | 2 | L | 98 | 200 |
| 31 | 6 | L | 98 | 200 |
| 32 | 9 | L | 22 | 200 |
| 35 | 2 | L | 98 | 200 |
| 38 | 7 | L | 98 | 200 |
| 40 | 5 | L | 98 | 200 |
| 41 | 5 | L | 98 | 200 |
| 42 | 4 | L | 98 | 200 |
| 44 | 4 | L | 98 | 200 |
| 45 | 2 | L | 98 | 200 |
| 46 | 1 | L | 98 | 200 |
| 47 | 8 | L | 98 | 200 |
| 51 | 2 | L | 98 | 200 |
| 54 | 1 | L | 98 | 200 |
| 56 | 6 | L | 98 | 200 |
| 58 | 2 | L | 98 | 200 |
| 59 | 5 | L | 98 | 200 |
| 61 | 4 | L | 98 | 200 |
| 63 | 2 | L | 98 | 200 |
| 64 | 2 | L | 98 | 200 |
... 3033 more omitted by report limit.

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - expected 0.01 step) | 724823 | 0.009410 | 0.009425 | 0.010353 | 0.363811 |
| abs(RatioRot - expected 0.01 step) | 724823 | 0.232664 | 0.009380 | 0.910000 | 0.990000 |
| abs(RatioPath - RatioRot) | 724823 | 0.230945 | 0.001742 | 0.919062 | 1.0000 |

### Shortest PathLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 605 | 8 | L | 1.2062 | 0.311533 | 49 | 0.001534 | 0.010495 | 0.009231 | 0.026673 | 0.031040 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 605 | 8 | S | 1.2062 | 0.311533 | 100 | 0.009870 | 0.010018 | 0.010017 | 0.010068 | 0.010150 | 100 | 0.008897 | 0.010828 | 0.010814 | 0.012648 | 0.013043 |
| 3739 | 2 | L | 1.5036 | 0.311533 | 49 | 0.000469 | 0.020088 | 0.007590 | 0.118155 | 0.188815 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 3739 | 2 | S | 1.5036 | 0.311533 | 100 | 0.008950 | 0.010871 | 0.009111 | 0.009207 | 0.183947 | 100 | 0.004280 | 0.010051 | 0.010087 | 0.011810 | 0.012019 |
| 1533 | 2 | S | 1.5221 | 1.1623 | 100 | 0.009473 | 0.009687 | 0.009687 | 0.009801 | 0.009831 | 100 | 0.008657 | 0.008755 | 0.008755 | 0.008837 | 0.009203 |
| 4888 | 5 | L | 1.6240 | 0.873119 | 49 | 0.009831 | 0.014508 | 0.010764 | 0.029356 | 0.039039 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 4888 | 5 | S | 1.6240 | 0.873119 | 100 | 0.009161 | 0.009263 | 0.009266 | 0.009310 | 0.009332 | 100 | 0.007686 | 0.008424 | 0.008426 | 0.009085 | 0.009162 |
| 3004 | 2 | L | 1.7217 | 1.0294 | 45 | 0.002332 | 0.024248 | 0.009272 | 0.132985 | 0.202210 | 45 | 0.550000 | 0.770000 | 0.770000 | 0.970000 | 0.990000 |
| 3004 | 2 | S | 1.7217 | 1.0294 | 100 | 0.010000 | 0.010922 | 0.010899 | 0.011194 | 0.011253 | 100 | 0.008824 | 0.008878 | 0.008851 | 0.009318 | 0.009343 |
| 4161 | 4 | L | 1.8680 | 0.935438 | 49 | 0.009971 | 0.028207 | 0.011935 | 0.124019 | 0.155372 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |

### Shortest RotLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2486 | 5 | L | 10.8890 | 0.193827 | 49 | 0.003854 | 0.009471 | 0.009601 | 0.010993 | 0.014015 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 2486 | 5 | S | 10.8890 | 0.193827 | 100 | 0.009550 | 0.009563 | 0.009563 | 0.009572 | 0.009578 | 100 | 0.007789 | 0.015689 | 0.015704 | 0.022825 | 0.023580 |
| 1955 | 4 | L | 8.4630 | 0.213062 | 49 | 0.001508 | 0.008398 | 0.008215 | 0.013219 | 0.019678 | 49 | 0.000835 | 0.729813 | 0.740000 | 0.960000 | 0.980000 |
| 1955 | 4 | S | 8.4630 | 0.213062 | 100 | 0.008333 | 0.008432 | 0.008433 | 0.008489 | 0.008519 | 100 | 0.000003 | 0.000339 | 0.000258 | 0.000874 | 0.001081 |
| 1092 | 4 | L | 12.8622 | 0.220287 | 49 | 0.008923 | 0.009702 | 0.009012 | 0.013243 | 0.016828 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 1092 | 4 | S | 12.8622 | 0.220287 | 100 | 0.008870 | 0.008895 | 0.008893 | 0.008906 | 0.008919 | 100 | 0.000000 | 0.016838 | 0.005840 | 0.016062 | 0.990000 |
| 1294 | 5 | L | 12.8623 | 0.220287 | 49 | 0.007191 | 0.009605 | 0.009518 | 0.010035 | 0.013223 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 1294 | 5 | S | 12.8623 | 0.220287 | 100 | 0.009464 | 0.009481 | 0.009481 | 0.009501 | 0.009507 | 100 | 0.000000 | 0.015794 | 0.005961 | 0.011919 | 0.990000 |
| 2338 | 5 | L | 12.9220 | 0.220287 | 49 | 0.009189 | 0.010465 | 0.009394 | 0.019745 | 0.021241 | 49 | 0.009156 | 0.729983 | 0.740000 | 0.960000 | 0.980000 |
| 2338 | 5 | S | 12.9220 | 0.220287 | 100 | 0.009076 | 0.009202 | 0.009198 | 0.009306 | 0.009316 | 100 | 0.000000 | 0.007867 | 0.006674 | 0.017510 | 0.018777 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioRot differs from sample | 705668 |
| RatioPath differs from sample | 701919 |
| pair ratios differ | 263341 |
| RatioRot not increasing | 253088 |
| RatioPath not increasing | 3029 |
| RatioPath outside 0..1 | 0 |
| odd row is not PathRatio | 0 |
| RatioRot outside 0..1 | 0 |

### PathL Ratio Issue Examples

| problem | testId | confId | branch | PathLength | RotLength | pair | expected | previous RatioPath | RatioPath | RatioRot | odd row mode | even row mode | odd PathDist | even Rotdist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RatioPath not increasing | 2 | 2 | L | 2.4001 | 0.774298 | 44 | 0.440000 | 0.404843 | 0.400937 | 1.0000 | PathRatio | RotRatio | 0.096564 | 3.2294 |
| RatioPath not increasing | 2 | 2 | L | 2.4001 | 0.774298 | 45 | 0.450000 | 0.400937 | 0.391319 | 1.0000 | PathRatio | RotRatio | 0.155899 | 3.7384 |
| RatioPath not increasing | 2 | 2 | L | 2.4001 | 0.774298 | 46 | 0.460000 | 0.391319 | 0.353073 | 1.0000 | PathRatio | RotRatio | 0.300442 | 4.5219 |
| RatioPath not increasing | 2 | 2 | L | 2.4001 | 0.774298 | 49 | 0.490000 | 0.562994 | 0.552816 | 1.0000 | PathRatio | RotRatio | 0.267181 | 19.5588 |
| RatioPath not increasing | 4 | 4 | L | 13.5573 | 1.1177 | 50 | 0.500000 | 0.502527 | 0.491553 | 1.0000 | PathRatio | RotRatio | 0.341994 | 179.441 |

### PathL Anomaly Statistics

| condition | rows | % rows | PathDist median | PathDist p95 | PathDist max | Rotdist median | Rotdist p95 | Rotdist max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any anomaly | 516071 | 35.5998 | 0.276169 | 10.3095 | 16.1626 | 1.0726 | 8.4412 | 180.000 |
| CfxOK != TRUE | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| FoundBranch mismatch | 514446 | 35.4877 | 0.262399 | 10.2938 | 16.1626 | 1.0734 | 8.4295 | 180.000 |
| PathDist > 1.0000 mm | 244794 | 16.8865 | 6.4718 | 11.4431 | 16.1626 | 1.3774 | 8.9745 | 179.874 |
| Rotdist > 1.0000 deg | 273443 | 18.8627 | 4.7019 | 10.5489 | 16.1626 | 1.8448 | 14.4992 | 180.000 |

### PathL Anomaly Reason Combinations

| conditions | rows | % rows |
| --- | --- | --- |
| FoundBranch mismatch + PathDist > 1.0000 mm + Rotdist > 1.0000 deg | 176633 | 12.1846 |
| FoundBranch mismatch | 175060 | 12.0761 |
| FoundBranch mismatch + Rotdist > 1.0000 deg | 96127 | 6.6311 |
| FoundBranch mismatch + PathDist > 1.0000 mm | 66626 | 4.5960 |
| PathDist > 1.0000 mm | 942 | 0.064981 |
| PathDist > 1.0000 mm + Rotdist > 1.0000 deg | 593 | 0.040907 |
| Rotdist > 1.0000 deg | 90 | 0.006208 |

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 1070 | 16.1626 | 16.4037 | 0.992280 | 0.200000 |
| 1528 | 16.0565 | 16.1249 | 0.697732 | 0.200000 |
| 3916 | 16.0478 | 16.1238 | 0.793271 | 0.200000 |
| 1395 | 15.9836 | 16.0149 | 1.2240 | 0.200000 |
| 230 | 15.8514 | 15.8983 | 1.1323 | 0.200000 |
| 1075 | 15.8074 | 15.8601 | 1.3050 | 0.200000 |
| 3259 | 15.7367 | 15.9787 | 1.4044 | 0.200000 |
| 3001 | 15.5992 | 15.6696 | 1.1710 | 0.200000 |
| 2500 | 15.5652 | 15.5967 | 1.4205 | 0.200000 |
| 3876 | 15.5525 | 15.5966 | 1.4205 | 0.200000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 516 | 180.000 | 9.2184 | 0.926188 | 0.200000 |
| 1191 | 180.000 | 13.7820 | 0.841159 | 0.200000 |
| 4760 | 180.000 | 4.2360 | 0.916845 | 0.200000 |
| 4991 | 180.000 | 13.2543 | 1.0302 | 0.200000 |
| 201 | 179.999 | 8.1273 | 0.919403 | 0.200000 |
| 640 | 179.999 | 7.8823 | 0.721989 | 0.200000 |
| 649 | 179.999 | 12.9408 | 0.952025 | 0.200000 |
| 1633 | 179.999 | 8.9738 | 1.2493 | 0.200000 |
| 1695 | 179.999 | 10.8846 | 1.0741 | 0.200000 |
| 2015 | 179.999 | 12.8634 | 0.949555 | 0.200000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
