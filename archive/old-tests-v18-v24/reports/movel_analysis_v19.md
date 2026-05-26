# ABB MoveL Analysis v19

## Summary

- Tests: 7287
- Tests with success rows: 6432
- Success rows: 7729
- Tests without success rows: 854
- PathL diagnostic rows: 1545910
- PathL groups by test/conf/branch: 7730
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=6675, L=3098
- Found branches without matching successful control branch: S=530, L=1715

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 6675 | 530 | 7.9401 | 0.075000 | 0.200000 | 0.200000 | 0.600507 | 37.5521 | 1755.330 |
| L | 3098 | 1715 | 55.3583 | 0.100000 | 0.200000 | 0.200000 | 0.598451 | 14.3654 | 1568.690 |

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 6259 | 0.000100 | 0.178421 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 530 | 0.000100 | 0.092196 | 0.075000 | 0.200000 | 0.200000 |
| L successful | 1472 | 0.001563 | 0.112775 | 0.100000 | 0.200000 | 0.200000 |
| L found unsuccessful | 1715 | 0.000100 | 0.081003 | 0.100000 | 0.200000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 0
- CalcC/PathL mismatches: 0
- Worst valid delta: test 1499, C vs CalcC, axis 1, 0.005000 deg

None.

## Branch Matching

- Control branch counts: S=6258, L=1471, none=0
- ControlMatchShort XOR ControlMatchLong violations: 0
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=6145, L=1383, none=201
- Legacy/control branch disagreements: 201
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

None.

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 1383 |
| L | none | 88 |
| S | S | 6145 |
| S | none | 113 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 6259 | 0.012059 | 0.004739 | 0.021395 | 9.3030 | 0.006250 |
| S ControlMaxAx4 successful | 6259 | 0.412738 | 0.110895 | 1.0077 | 910.124 | 0.000100 |
| S ControlMaxAx6 successful | 6259 | 0.410004 | 0.106349 | 1.0062 | 910.235 | 0.000100 |
| S ControlMaxAx1 unsuccessful | 1028 | 3.2410 | 0.005663 | 0.038195 | 1364.400 | 0.000100 |
| S ControlMaxAx4 unsuccessful | 1028 | 12.8730 | 0.255911 | 23.8965 | 1755.240 | 0.000100 |
| S ControlMaxAx6 unsuccessful | 1028 | 15.6817 | 0.240769 | 23.8988 | 1783.810 | 0.000100 |
| L ControlMaxAx1 successful | 1472 | 0.022494 | 0.013808 | 0.066177 | 0.636699 | 0.025000 |
| L ControlMaxAx4 successful | 1472 | 0.852787 | 0.331526 | 3.7304 | 24.6319 | 0.001563 |
| L ControlMaxAx6 successful | 1472 | 0.858552 | 0.330757 | 3.6559 | 24.5277 | 0.001563 |
| L ControlMaxAx1 unsuccessful | 5815 | 202.310 | 0.021605 | 1343.210 | 1766.170 | 0.000100 |
| L ControlMaxAx4 unsuccessful | 5815 | 234.414 | 1.2379 | 1410.700 | 1799.490 | 0.000100 |
| L ControlMaxAx6 unsuccessful | 5815 | 250.839 | 1.2260 | 1533.390 | 1799.660 | 0.000100 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 23193 | 0.319105 | 0.079102 | 1.3239 | 25.8365 | 490 | L | Ax4 | 0.073177 | 25.8365 | 25.7323 |
| found unsuccessful | 6735 | 3.3365 | 0.342667 | 14.1064 | 171.302 | 3962 | S | Ax6 | 0.006882 | 171.211 | 171.302 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 490 | L | 0.073177 | 25.8365 | 25.7323 | Ax4 | 25.8365 | 0.001563 | empty |
| successful | 4189 | L | 0.016174 | 24.1107 | 24.2556 | Ax6 | 24.2556 | 0.001563 | empty |
| successful | 4645 | S | 8.5848 | 23.1902 | 15.5929 | Ax4 | 23.1902 | 0.001563 | empty |
| successful | 6450 | L | 0.305328 | 18.6211 | 19.0667 | Ax6 | 19.0667 | 0.003125 | empty |
| successful | 4816 | L | 0.008817 | 17.7477 | 17.9084 | Ax6 | 17.9084 | 0.003125 | empty |
| successful | 3558 | L | 0.021083 | 16.9118 | 16.7779 | Ax4 | 16.9118 | 0.003125 | empty |
| successful | 4118 | L | 0.013592 | 14.1629 | 14.3707 | Ax6 | 14.3707 | 0.003125 | empty |
| successful | 1598 | L | 0.011459 | 13.6349 | 13.4256 | Ax4 | 13.6349 | 0.003125 | empty |
| successful | 2878 | L | 0.010971 | 13.2590 | 13.4278 | Ax6 | 13.4278 | 0.003125 | empty |
| successful | 6914 | L | 0.011284 | 11.3640 | 11.6348 | Ax6 | 11.6348 | 0.006250 | empty |
| found unsuccessful | 3962 | S | 0.006882 | 171.211 | 171.302 | Ax6 | 171.302 | 0.000100 | SINGULAR |
| found unsuccessful | 6043 | L | 0.014427 | 161.034 | 160.883 | Ax4 | 161.034 | 0.000100 | SINGULAR |
| found unsuccessful | 2505 | L | 0.016846 | 159.021 | 159.179 | Ax6 | 159.179 | 0.000100 | SINGULAR |
| found unsuccessful | 5749 | L | 0.015026 | 155.493 | 155.634 | Ax6 | 155.634 | 0.000100 | SINGULAR |
| found unsuccessful | 2617 | S | 0.001987 | 146.800 | 146.742 | Ax4 | 146.800 | 0.100000 | empty |
| found unsuccessful | 1335 | S | 0.004616 | 145.239 | 145.272 | Ax6 | 145.272 | 0.000100 | SINGULAR |
| found unsuccessful | 2047 | L | 0.014313 | 141.041 | 140.894 | Ax4 | 141.041 | 0.000100 | SINGULAR |
| found unsuccessful | 1338 | S | 0.005600 | 139.285 | 139.222 | Ax4 | 139.285 | 0.000100 | SINGULAR |
| found unsuccessful | 6365 | L | 0.031057 | 134.941 | 135.127 | Ax6 | 135.127 | 0.000100 | SINGULAR |
| found unsuccessful | 5886 | L | 0.017105 | 130.949 | 131.061 | Ax6 | 131.061 | 0.000195 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 6668 | 0.014094 | 0.005096 | 0.023361 | 10.4749 |
| S legacy WinAx1 | 6668 | 0.131496 | 0.050850 | 0.232712 | 84.8556 |
| S legacy Win2Ax1 | 6668 | 0.992560 | 0.501398 | 2.2984 | 157.365 |
| S legacy MaxAx4 | 6668 | 0.840426 | 0.146626 | 2.3537 | 146.800 |
| S legacy WinAx4 | 6668 | 5.3894 | 1.4485 | 21.5467 | 174.311 |
| S legacy Win2Ax4 | 6668 | 25.8456 | 13.2508 | 106.498 | 183.053 |
| S legacy MaxAx6 | 6668 | 0.836852 | 0.145142 | 2.3227 | 146.742 |
| S legacy WinAx6 | 6668 | 5.3576 | 1.4383 | 21.2559 | 174.264 |
| S legacy Win2Ax6 | 6668 | 25.6399 | 12.8263 | 104.790 | 183.600 |
| L legacy MaxAx1 | 3091 | 0.025013 | 0.014793 | 0.070740 | 2.1240 |
| L legacy WinAx1 | 3091 | 0.249060 | 0.147645 | 0.703667 | 20.9364 |
| L legacy Win2Ax1 | 3091 | 2.3250 | 1.4498 | 6.6117 | 102.938 |
| L legacy MaxAx4 | 3091 | 2.4627 | 0.548508 | 9.1894 | 130.949 |
| L legacy WinAx4 | 3091 | 14.8092 | 5.4165 | 72.1006 | 177.079 |
| L legacy Win2Ax4 | 3091 | 58.5960 | 43.6729 | 154.885 | 191.124 |
| L legacy MaxAx6 | 3091 | 2.4591 | 0.544662 | 9.1852 | 131.061 |
| L legacy WinAx6 | 3091 | 14.7741 | 5.3152 | 71.2424 | 176.489 |
| L legacy Win2Ax6 | 3091 | 58.2529 | 42.5267 | 156.694 | 195.095 |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 6668 | 0.997943 | 0.973028 | 0.766900 |
| S | 4 | 6668 | 0.869686 | 0.716391 | 0.397712 |
| S | 6 | 6668 | 0.869505 | 0.716396 | 0.396506 |
| L | 1 | 3091 | 0.991707 | 0.993186 | 0.967649 |
| L | 4 | 3091 | 0.924799 | 0.632171 | 0.356251 |
| L | 6 | 3091 | 0.924744 | 0.630516 | 0.342823 |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 0
- Groups with row count != 200: 1
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 772955
- Ratio pair/order issues: 608754
- Mean PathDist: 0.128804
- Max PathDist: 0.947203
- Mean Rotdist: 0.740979
- Max Rotdist: 42.5545

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 772955 | 0.163123 | 0.143366 | 0.374096 | 0.947203 |
| PathDist measured from RotRatio rows | 772955 | 0.094485 | 0.014503 | 0.340196 | 0.906777 |
| Rotdist measured from PathRatio rows | 772955 | 1.4713 | 0.794257 | 5.1536 | 42.5545 |
| Rotdist measured from RotRatio rows | 772955 | 0.010689 | 0.000000 | 0.039565 | 0.201741 |

### PathL Sample Group Issues

| testId | confId | branch | rows | expected |
| --- | --- | --- | --- | --- |
| 3371 | 5 | S | 110 | 200 |

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - expected 0.01 step) | 772955 | 0.013215 | 0.009957 | 0.036731 | 0.273638 |
| abs(RatioRot - expected 0.01 step) | 772955 | 0.003356 | 0.000003 | 0.008466 | 0.009313 |
| abs(RatioPath - RatioRot) | 772955 | 0.011861 | 0.008109 | 0.035186 | 0.266239 |

### Shortest PathLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4708 | 4 | S | 1.2062 | 31.3718 | 100 | 0.010000 | 0.116550 | 0.110513 | 0.146759 | 0.146902 | 100 | 0.007550 | 0.008009 | 0.008022 | 0.008577 | 0.008609 |
| 4723 | 4 | S | 1.7790 | 88.5191 | 100 | 0.010000 | 0.094366 | 0.094890 | 0.117895 | 0.118490 | 100 | 0.006966 | 0.007371 | 0.007506 | 0.007608 | 0.007632 |
| 3347 | 2 | S | 1.8679 | 84.9608 | 100 | 0.000000 | 0.033550 | 0.032153 | 0.079103 | 0.081413 | 100 | 0.007109 | 0.007736 | 0.007665 | 0.008160 | 0.008185 |
| 3519 | 9 | S | 1.8680 | 84.9608 | 100 | 0.000000 | 0.025810 | 0.024358 | 0.045025 | 0.058492 | 100 | 0.000000 | 0.004514 | 0.006674 | 0.008096 | 0.008469 |
| 98 | 1 | S | 1.8680 | 84.9608 | 100 | 0.000000 | 0.058792 | 0.062825 | 0.081501 | 0.081911 | 100 | 0.000000 | 0.005033 | 0.007856 | 0.007988 | 0.008132 |
| 4316 | 4 | S | 1.8680 | 84.9608 | 100 | 0.000506 | 0.108717 | 0.120715 | 0.186759 | 0.192590 | 100 | 0.000010 | 0.006461 | 0.006732 | 0.008090 | 0.008193 |
| 2104 | 5 | S | 1.8680 | 84.9608 | 100 | 0.010000 | 0.023202 | 0.025319 | 0.029589 | 0.029627 | 100 | 0.007813 | 0.008363 | 0.008406 | 0.008445 | 0.008463 |
| 6724 | 9 | S | 1.8680 | 84.9608 | 100 | 0.000113 | 0.015786 | 0.016032 | 0.026798 | 0.027512 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000001 |
| 6320 | 2 | S | 1.8680 | 84.9608 | 100 | 0.000000 | 0.024544 | 0.026514 | 0.046101 | 0.046273 | 100 | 0.000000 | 0.004680 | 0.007584 | 0.008139 | 0.008181 |
| 3298 | 4 | S | 1.8680 | 84.9608 | 100 | 0.000000 | 0.015779 | 0.014627 | 0.028244 | 0.035590 | 100 | 0.000000 | 0.007886 | 0.008037 | 0.008416 | 0.008433 |

### Shortest RotLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 249 | 5 | S | 11.3228 | 18.9264 | 100 | 0.008490 | 0.008587 | 0.008592 | 0.008668 | 0.008674 | 100 | 0.009024 | 0.009067 | 0.009071 | 0.009096 | 0.009098 |
| 1815 | 9 | S | 11.3228 | 18.9264 | 100 | 0.006723 | 0.007757 | 0.007824 | 0.008616 | 0.008661 | 100 | 0.008229 | 0.008663 | 0.008806 | 0.008843 | 0.008844 |
| 3255 | 1 | S | 11.3228 | 18.9264 | 100 | 0.000000 | 0.008007 | 0.009030 | 0.014599 | 0.017576 | 100 | 0.000002 | 0.003064 | 0.000008 | 0.008488 | 0.008610 |
| 4810 | 2 | S | 8.4631 | 21.4425 | 100 | 0.018969 | 0.027191 | 0.023320 | 0.044035 | 0.050031 | 100 | 0.000045 | 0.007810 | 0.008031 | 0.008611 | 0.008670 |
| 2771 | 9 | S | 11.9723 | 21.8293 | 100 | 0.000006 | 0.000757 | 0.000229 | 0.003536 | 0.003569 | 100 | 0.007956 | 0.008172 | 0.008136 | 0.008584 | 0.008618 |
| 3226 | 8 | S | 12.8621 | 21.8293 | 100 | 0.004449 | 0.007047 | 0.007177 | 0.008656 | 0.008757 | 100 | 0.007101 | 0.008459 | 0.008634 | 0.009131 | 0.009165 |
| 756 | 6 | S | 12.8622 | 21.8293 | 100 | 0.000000 | 0.001636 | 0.001537 | 0.003597 | 0.003814 | 100 | 0.007608 | 0.008272 | 0.008261 | 0.008671 | 0.008695 |
| 4067 | 2 | S | 12.8622 | 21.8293 | 100 | 0.005461 | 0.007116 | 0.006848 | 0.009260 | 0.009868 | 100 | 0.007528 | 0.008171 | 0.007994 | 0.008617 | 0.008623 |
| 613 | 8 | S | 12.9221 | 21.8293 | 100 | 0.001807 | 0.004972 | 0.005035 | 0.007503 | 0.007603 | 100 | 0.008306 | 0.008816 | 0.008803 | 0.009201 | 0.009235 |
| 6183 | 9 | S | 12.9221 | 21.8293 | 100 | 0.001476 | 0.003830 | 0.003569 | 0.006799 | 0.006832 | 100 | 0.007416 | 0.007735 | 0.007687 | 0.008265 | 0.008330 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioPath differs from sample | 531316 |
| pair ratios differ | 460365 |
| RatioRot differs from sample | 319498 |
| RatioPath not increasing | 8571 |
| RatioPath outside 0..1 | 0 |
| odd row is not PathRatio | 0 |
| RatioRot outside 0..1 | 0 |

### PathL Ratio Issue Examples

| problem | testId | confId | branch | PathLength | RotLength | pair | expected | previous RatioPath | RatioPath | RatioRot | odd row mode | even row mode | odd PathDist | even Rotdist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RatioPath not increasing | 2 | 2 | S | 11.3868 | 105.419 | 100 | 1.0000 | 1.0000 | 1.0000 | 0.996776 | PathRatio | RotRatio | 0.252746 | 0.000000 |
| RatioPath not increasing | 2 | 5 | L | 11.3868 | 254.581 | 100 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | PathRatio | RotRatio | 0.294515 | 0.000000 |
| RatioPath not increasing | 3 | 4 | S | 10.7647 | 79.6314 | 100 | 1.0000 | 1.0000 | 1.0000 | 0.992282 | PathRatio | RotRatio | 0.188376 | 0.000000 |
| RatioPath not increasing | 4 | 1 | S | 6.5364 | 74.0839 | 2 | 0.020000 | 0.000000 | 0.000000 | 0.012326 | PathRatio | RotRatio | 0.262020 | 0.000000 |
| RatioPath not increasing | 7 | 4 | S | 13.5120 | 80.1778 | 39 | 0.390000 | 0.392414 | 0.366211 | 0.389078 | PathRatio | RotRatio | 0.255976 | 0.000000 |

### PathL Anomaly Statistics

| condition | rows | % rows | PathDist median | PathDist p95 | PathDist max | Rotdist median | Rotdist p95 | Rotdist max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any anomaly | 332799 | 21.5277 | 0.172564 | 0.393546 | 0.875461 | 2.0744 | 7.4778 | 42.5545 |
| CfxOK != TRUE | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| FoundBranch mismatch | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| PathDist > 1.0000 mm | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| Rotdist > 1.0000 deg | 332799 | 21.5277 | 0.172564 | 0.393546 | 0.875461 | 2.0744 | 7.4778 | 42.5545 |

### PathL Anomaly Reason Combinations

| conditions | rows | % rows |
| --- | --- | --- |
| Rotdist > 1.0000 deg | 332799 | 21.5277 |

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 576 | 0.947203 | 10.5078 | 71.2975 | 0.100000 |
| 4303 | 0.935980 | 10.1224 | 93.7654 | 0.050000 |
| 4450 | 0.925256 | 12.7546 | 96.3829 | 0.200000 |
| 4899 | 0.906777 | 12.3636 | 94.3057 | 0.050000 |
| 7170 | 0.899253 | 9.2097 | 75.1609 | 0.025000 |
| 4891 | 0.882112 | 9.9543 | 97.3625 | 0.050000 |
| 3222 | 0.875461 | 10.6779 | 43.6792 | 0.200000 |
| 5647 | 0.863472 | 10.5632 | 71.5418 | 0.200000 |
| 5338 | 0.860622 | 7.5995 | 56.5107 | 0.050000 |
| 790 | 0.827069 | 10.9269 | 66.6320 | 0.200000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 4746 | 42.5545 | 2.3074 | 248.279 | 0.200000 |
| 4427 | 41.4194 | 2.7925 | 262.985 | 0.200000 |
| 5876 | 39.3613 | 2.8493 | 283.069 | 0.200000 |
| 7131 | 39.3283 | 2.9658 | 334.452 | 0.100000 |
| 1730 | 36.7401 | 4.1416 | 334.452 | 0.025000 |
| 5938 | 35.4551 | 2.1934 | 239.383 | 0.050000 |
| 1526 | 30.5197 | 4.1528 | 279.822 | 0.025000 |
| 5976 | 30.2458 | 6.9173 | 291.443 | 0.050000 |
| 5014 | 29.5040 | 5.8959 | 328.628 | 0.100000 |
| 2846 | 29.3855 | 5.0674 | 263.319 | 0.200000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
