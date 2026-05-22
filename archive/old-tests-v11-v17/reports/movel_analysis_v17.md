# ABB MoveL Analysis v17

## Summary

- Tests: 924
- Tests with success rows: 804
- Success rows: 1017
- Tests without success rows: 120
- PathL diagnostic rows: 203400
- PathL groups by test/conf/branch: 1017
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=830, L=484
- Found branches without matching successful control branch: S=98, L=235

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 830 | 98 | 11.8072 | 0.100000 | 0.200000 | 0.200000 | 0.594418 | 33.7029 | 59.1274 |
| L | 484 | 235 | 48.5537 | 0.100000 | 0.200000 | 0.200000 | 0.508310 | 6.1685 | 41.0250 |

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 750 | 0.006250 | 0.174717 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 98 | 0.000781 | 0.093184 | 0.100000 | 0.200000 | 0.200000 |
| L successful | 267 | 0.003125 | 0.128663 | 0.100000 | 0.200000 | 0.200000 |
| L found unsuccessful | 235 | 0.000781 | 0.092291 | 0.100000 | 0.200000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 0
- CalcC/PathL mismatches: 0
- Worst valid delta: test 396, C vs CalcC, axis 1, 0.003000 deg

None.

## Branch Matching

- Control branch counts: S=750, L=267, none=0
- ControlMatchShort XOR ControlMatchLong violations: 0
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=732, L=249, none=36
- Legacy/control branch disagreements: 36
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

None.

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 249 |
| L | none | 18 |
| S | S | 732 |
| S | none | 18 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 750 | 0.009549 | 0.005808 | 0.026693 | 0.471665 | 0.100000 |
| S ControlMaxAx4 successful | 750 | 0.291118 | 0.132236 | 0.997746 | 8.4849 | 0.006250 |
| S ControlMaxAx6 successful | 750 | 0.292005 | 0.132651 | 1.0131 | 8.5391 | 0.006250 |
| S ControlMaxAx1 unsuccessful | 174 | 34.9233 | 0.007596 | 0.074111 | 1358.610 | 0.000100 |
| S ControlMaxAx4 unsuccessful | 174 | 48.7664 | 0.363850 | 58.6979 | 1706.450 | 0.000100 |
| S ControlMaxAx6 unsuccessful | 174 | 36.2553 | 0.297469 | 51.8427 | 1751.760 | 0.000100 |
| L ControlMaxAx1 successful | 267 | 0.018601 | 0.012070 | 0.057042 | 0.207924 | 0.100000 |
| L ControlMaxAx4 successful | 267 | 0.634768 | 0.267854 | 2.2507 | 11.4028 | 0.003125 |
| L ControlMaxAx6 successful | 267 | 0.634105 | 0.263666 | 2.3791 | 11.6196 | 0.003125 |
| L ControlMaxAx1 unsuccessful | 657 | 147.176 | 0.018028 | 956.148 | 1520.610 | 0.000100 |
| L ControlMaxAx4 unsuccessful | 657 | 192.775 | 0.791694 | 1354.570 | 1797.880 | 0.000100 |
| L ControlMaxAx6 unsuccessful | 657 | 185.875 | 0.819977 | 1437.390 | 1797.720 | 0.000100 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 3051 | 0.333261 | 0.100250 | 1.4722 | 12.4672 | 452 | L | Ax6 | 0.103653 | 12.2502 | 12.4672 |
| found unsuccessful | 999 | 1.7497 | 0.298157 | 6.4875 | 59.2277 | 43 | S | Ax6 | 0.013138 | 59.1040 | 59.2277 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 452 | L | 0.103653 | 12.2502 | 12.4672 | Ax6 | 12.4672 | 0.003125 | empty |
| successful | 15 | S | 0.006447 | 9.1482 | 9.2023 | Ax6 | 9.2023 | 0.006250 | empty |
| successful | 588 | S | 0.004448 | 7.5894 | 7.5303 | Ax4 | 7.5894 | 0.012500 | empty |
| successful | 308 | S | 0.004996 | 7.5608 | 7.5200 | Ax4 | 7.5608 | 0.050000 | empty |
| successful | 304 | S | 0.005478 | 7.3396 | 7.3943 | Ax6 | 7.3943 | 0.006250 | empty |
| successful | 190 | S | 0.015457 | 7.3018 | 7.3827 | Ax6 | 7.3827 | 0.006250 | empty |
| successful | 10 | L | 0.015713 | 6.2020 | 6.3783 | Ax6 | 6.3783 | 0.012500 | empty |
| successful | 837 | S | 0.008519 | 6.2256 | 6.3426 | Ax6 | 6.3426 | 0.006250 | empty |
| successful | 162 | L | 0.210907 | 5.2901 | 5.5285 | Ax6 | 5.5285 | 0.012500 | empty |
| successful | 814 | S | 0.006466 | 5.3029 | 5.3555 | Ax6 | 5.3555 | 0.050000 | empty |
| found unsuccessful | 43 | S | 0.013138 | 59.1040 | 59.2277 | Ax6 | 59.2277 | 0.000781 | empty |
| found unsuccessful | 771 | S | 0.001312 | 53.5935 | 53.4953 | Ax4 | 53.5935 | 0.000781 | empty |
| found unsuccessful | 517 | S | 0.024956 | 49.2531 | 49.2125 | Ax4 | 49.2531 | 0.000781 | empty |
| found unsuccessful | 30 | S | 0.005615 | 42.3436 | 42.2820 | Ax4 | 42.3436 | 0.001563 | empty |
| found unsuccessful | 897 | S | 0.009022 | 41.3483 | 41.4800 | Ax6 | 41.4800 | 0.001563 | empty |
| found unsuccessful | 5 | L | 0.011749 | 39.7278 | 39.6259 | Ax4 | 39.7278 | 0.000781 | empty |
| found unsuccessful | 381 | L | 0.015411 | 32.4893 | 32.6585 | Ax6 | 32.6585 | 0.001563 | empty |
| found unsuccessful | 296 | S | 0.003635 | 25.5042 | 25.4510 | Ax4 | 25.5042 | 0.003125 | empty |
| found unsuccessful | 626 | L | 0.014053 | 24.4345 | 24.6790 | Ax6 | 24.6790 | 0.001563 | empty |
| found unsuccessful | 612 | S | 0.007648 | 22.4854 | 22.5750 | Ax6 | 22.5750 | 0.001563 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 830 | 0.014416 | 0.006334 | 0.027626 | 2.7862 |
| S legacy WinAx1 | 830 | 0.125646 | 0.063255 | 0.276184 | 13.6304 |
| S legacy Win2Ax1 | 830 | 1.0332 | 0.617582 | 2.7539 | 47.1665 |
| S legacy MaxAx4 | 830 | 0.911175 | 0.193793 | 2.7015 | 59.1040 |
| S legacy WinAx4 | 830 | 6.2392 | 1.8978 | 26.5462 | 159.897 |
| S legacy Win2Ax4 | 830 | 29.7397 | 16.8160 | 112.346 | 182.677 |
| S legacy MaxAx6 | 830 | 0.908832 | 0.184666 | 2.7157 | 59.2277 |
| S legacy WinAx6 | 830 | 6.2094 | 1.8159 | 26.1472 | 161.135 |
| S legacy Win2Ax6 | 830 | 29.4244 | 16.0043 | 110.387 | 183.067 |
| L legacy MaxAx1 | 484 | 0.032133 | 0.012703 | 0.066956 | 4.0087 |
| L legacy WinAx1 | 484 | 0.317199 | 0.126949 | 0.669365 | 38.4623 |
| L legacy Win2Ax1 | 484 | 2.4873 | 1.2560 | 5.8810 | 117.048 |
| L legacy MaxAx4 | 484 | 1.2744 | 0.460888 | 4.5921 | 39.7278 |
| L legacy WinAx4 | 484 | 10.7635 | 4.5982 | 41.3401 | 150.605 |
| L legacy Win2Ax4 | 484 | 53.0910 | 36.6086 | 143.494 | 183.742 |
| L legacy MaxAx6 | 484 | 1.2598 | 0.439590 | 4.4787 | 39.6259 |
| L legacy WinAx6 | 484 | 10.6187 | 4.3678 | 40.4876 | 149.586 |
| L legacy Win2Ax6 | 484 | 52.0815 | 37.6277 | 142.764 | 187.583 |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 830 | 0.417468 | 0.611588 | 0.974249 |
| S | 4 | 830 | 0.986528 | 0.864036 | 0.520812 |
| S | 6 | 830 | 0.986463 | 0.864040 | 0.524657 |
| L | 1 | 484 | 0.999082 | 0.998898 | 0.890006 |
| L | 4 | 484 | 0.992248 | 0.905781 | 0.571547 |
| L | 6 | 484 | 0.992265 | 0.906695 | 0.586803 |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 0
- Groups with row count != 200: 0
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 101700
- Ratio pair/order issues: 76199
- Mean PathDist: 0.119944
- Max PathDist: 0.862053
- Mean Rotdist: 0.926594
- Max Rotdist: 31.6479

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 101700 | 0.170398 | 0.151743 | 0.382316 | 0.862053 |
| PathDist measured from RotRatio rows | 101700 | 0.069490 | 0.004406 | 0.324596 | 0.715279 |
| Rotdist measured from PathRatio rows | 101700 | 1.8433 | 1.1562 | 5.8517 | 31.6479 |
| Rotdist measured from RotRatio rows | 101700 | 0.009898 | 0.000000 | 0.039565 | 0.096913 |

### PathL Sample Group Issues

None.

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - expected 0.01 step) | 101700 | 0.013537 | 0.010000 | 0.037979 | 0.162754 |
| abs(RatioRot - expected 0.01 step) | 101700 | 0.002209 | 0.000001 | 0.008219 | 0.009451 |
| abs(RatioPath - RatioRot) | 101700 | 0.012846 | 0.009306 | 0.036978 | 0.162759 |

### Shortest PathLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 588 | 5 | S | 1.9230 | 145.213 | 100 | 0.010000 | 0.068711 | 0.075441 | 0.099152 | 0.104195 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 214 | 5 | S | 1.9230 | 145.213 | 100 | 0.000213 | 0.027196 | 0.023444 | 0.063667 | 0.066626 | 100 | 0.000000 | 0.000001 | 0.000001 | 0.000001 | 0.000002 |
| 728 | 2 | L | 2.1311 | 220.237 | 100 | 0.000000 | 0.037187 | 0.039376 | 0.063922 | 0.072193 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 756 | 2 | S | 2.1933 | 128.407 | 100 | 0.000000 | 0.012470 | 0.011533 | 0.024978 | 0.026679 | 100 | 0.000000 | 0.000222 | 0.000001 | 0.000002 | 0.007379 |
| 143 | 5 | S | 2.4761 | 161.432 | 100 | 0.000775 | 0.086881 | 0.089661 | 0.146891 | 0.162754 | 100 | 0.000000 | 0.000001 | 0.000001 | 0.000003 | 0.000005 |
| 729 | 5 | S | 2.4761 | 161.432 | 100 | 0.000000 | 0.042695 | 0.047474 | 0.064141 | 0.065678 | 100 | 0.000000 | 0.000001 | 0.000001 | 0.000002 | 0.000002 |
| 605 | 2 | S | 2.5017 | 103.876 | 100 | 0.010000 | 0.104170 | 0.106487 | 0.142776 | 0.157489 | 100 | 0.000000 | 0.000002 | 0.000002 | 0.000003 | 0.000004 |
| 506 | 5 | S | 2.5630 | 162.855 | 100 | 0.000126 | 0.038456 | 0.045581 | 0.062128 | 0.066947 | 100 | 0.000000 | 0.000002 | 0.000001 | 0.000003 | 0.000006 |
| 506 | 4 | L | 2.5630 | 197.145 | 100 | 0.000000 | 0.038641 | 0.027387 | 0.080884 | 0.091373 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 186 | 4 | S | 2.7925 | 102.197 | 100 | 0.000668 | 0.051330 | 0.056151 | 0.078015 | 0.082080 | 100 | 0.000002 | 0.000008 | 0.000008 | 0.000019 | 0.000021 |

### Shortest RotLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 164 | 8 | S | 7.8212 | 24.4661 | 100 | 0.010000 | 0.012096 | 0.012304 | 0.012584 | 0.012681 | 100 | 0.008658 | 0.008988 | 0.008967 | 0.009174 | 0.009210 |
| 213 | 1 | S | 8.5052 | 24.4661 | 100 | 0.010000 | 0.010507 | 0.010511 | 0.010810 | 0.010851 | 100 | 0.008792 | 0.008801 | 0.008801 | 0.008809 | 0.008810 |
| 107 | 7 | S | 13.7014 | 24.4661 | 100 | 0.002589 | 0.006080 | 0.006358 | 0.006710 | 0.006786 | 100 | 0.000067 | 0.005242 | 0.005528 | 0.006674 | 0.006831 |
| 797 | 7 | S | 13.7014 | 24.4661 | 100 | 0.000000 | 0.003238 | 0.004129 | 0.006926 | 0.007313 | 100 | 0.007163 | 0.008098 | 0.008190 | 0.008517 | 0.008553 |
| 368 | 5 | S | 13.7015 | 24.4661 | 100 | 0.000000 | 0.002139 | 0.002346 | 0.003548 | 0.004681 | 100 | 0.005718 | 0.007587 | 0.007774 | 0.008061 | 0.008106 |
| 823 | 2 | S | 8.9972 | 26.0717 | 100 | 0.000682 | 0.002446 | 0.000776 | 0.004827 | 0.004837 | 100 | 0.008144 | 0.008418 | 0.008297 | 0.008712 | 0.008725 |
| 560 | 5 | S | 8.9972 | 26.0717 | 100 | 0.009631 | 0.009862 | 0.009874 | 0.010035 | 0.010062 | 100 | 0.008745 | 0.008791 | 0.008790 | 0.008822 | 0.009229 |
| 153 | 5 | S | 9.2670 | 26.0717 | 100 | 0.010000 | 0.014381 | 0.014831 | 0.015967 | 0.016126 | 100 | 0.007562 | 0.008135 | 0.008136 | 0.008837 | 0.008912 |
| 647 | 5 | S | 15.3135 | 26.0717 | 100 | 0.002028 | 0.006180 | 0.006647 | 0.010336 | 0.010935 | 100 | 0.000002 | 0.004991 | 0.007343 | 0.008218 | 0.008795 |
| 610 | 7 | S | 15.4874 | 26.0717 | 100 | 0.006685 | 0.010122 | 0.009632 | 0.014008 | 0.016950 | 100 | 0.007886 | 0.008596 | 0.008723 | 0.008880 | 0.009246 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioPath differs from sample | 68907 |
| pair ratios differ | 65152 |
| RatioRot differs from sample | 27896 |
| RatioPath not increasing | 1067 |
| RatioPath outside 0..1 | 0 |
| odd row is not PathRatio | 0 |
| RatioRot outside 0..1 | 0 |

### PathL Ratio Issue Examples

| problem | testId | confId | branch | PathLength | RotLength | pair | expected | previous RatioPath | RatioPath | RatioRot | odd row mode | even row mode | odd PathDist | even Rotdist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RatioPath not increasing | 1 | 5 | S | 12.8634 | 102.522 | 2 | 0.020000 | 0.000000 | 0.000000 | 0.012262 | PathRatio | RotRatio | 0.144919 | 0.039565 |
| RatioPath not increasing | 1 | 5 | S | 12.8634 | 102.522 | 95 | 0.950000 | 0.950089 | 0.927941 | 0.942344 | PathRatio | RotRatio | 0.099029 | 0.000000 |
| RatioPath not increasing | 2 | 4 | S | 11.4396 | 71.2117 | 87 | 0.870000 | 0.865670 | 0.856707 | 0.870002 | PathRatio | RotRatio | 0.048023 | 0.000000 |
| RatioPath not increasing | 5 | 8 | S | 8.2388 | 124.106 | 100 | 1.0000 | 1.0000 | 1.0000 | 0.999997 | PathRatio | RotRatio | 0.445092 | 0.000000 |
| RatioPath not increasing | 7 | 3 | S | 9.1229 | 144.198 | 2 | 0.020000 | 0.000000 | 0.000000 | 0.012476 | PathRatio | RotRatio | 0.149962 | 0.039565 |

### PathL Anomaly Statistics

| condition | rows | % rows | PathDist median | PathDist p95 | PathDist max | Rotdist median | Rotdist p95 | Rotdist max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any anomaly | 56081 | 27.5718 | 0.165095 | 0.393336 | 0.742210 | 2.2559 | 7.6428 | 31.6479 |
| CfxOK != TRUE | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| FoundBranch mismatch | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| PathDist > 1.0000 mm | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| Rotdist > 1.0000 deg | 56081 | 27.5718 | 0.165095 | 0.393336 | 0.742210 | 2.2559 | 7.6428 | 31.6479 |

### PathL Anomaly Reason Combinations

| conditions | rows | % rows |
| --- | --- | --- |
| Rotdist > 1.0000 deg | 56081 | 27.5718 |

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 748 | 0.862053 | 10.5716 | 68.2783 | 0.200000 |
| 727 | 0.792902 | 11.9307 | 80.6955 | 0.200000 |
| 834 | 0.742210 | 6.2220 | 90.5995 | 0.200000 |
| 147 | 0.715279 | 10.7570 | 108.653 | 0.200000 |
| 19 | 0.714730 | 11.7533 | 60.7734 | 0.200000 |
| 205 | 0.703873 | 14.2384 | 64.5707 | 0.200000 |
| 322 | 0.699717 | 8.6785 | 86.1422 | 0.200000 |
| 309 | 0.673146 | 9.9838 | 98.7963 | 0.050000 |
| 227 | 0.672010 | 8.0709 | 127.582 | 0.100000 |
| 351 | 0.665268 | 15.4875 | 26.0717 | 0.200000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 400 | 31.6479 | 2.9659 | 273.532 | 0.050000 |
| 676 | 27.4197 | 3.1126 | 266.691 | 0.200000 |
| 143 | 26.3148 | 2.4761 | 161.432 | 0.200000 |
| 162 | 25.7732 | 4.1567 | 241.695 | 0.012500 |
| 77 | 22.1936 | 3.2381 | 193.774 | 0.050000 |
| 750 | 20.3990 | 4.1567 | 241.695 | 0.050000 |
| 123 | 19.3659 | 3.1649 | 157.019 | 0.200000 |
| 124 | 18.1040 | 4.0285 | 202.038 | 0.200000 |
| 506 | 18.0473 | 2.5630 | 197.145 | 0.012500 |
| 744 | 17.2425 | 4.8573 | 157.746 | 0.050000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
