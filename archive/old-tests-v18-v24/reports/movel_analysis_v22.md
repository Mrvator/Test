# ABB MoveL Analysis v22

## Summary

- Tests: 35
- Tests with success rows: 33
- Success rows: 37
- Tests without success rows: 2
- PathL diagnostic rows: 10076
- PathL groups by test/conf/branch: 64
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## PathL Length Overview

Lengths here are read from raw `pathl.csv` values. The graph script groups duplicate sample rows by `testId/confId/branch`, but it does not recalculate `PathLength` or `RotLength` from A/B poses.

- Outcome map: `reports/pathl_length_outcome_map_v22.svg`
- Distribution graph: `reports/pathl_length_outcome_hist_v22.svg`
- Detail summary: `reports/pathl_length_overview_v22.md`

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=32, L=12
- Found branches without matching successful control branch: S=0, L=12

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 32 | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| L | 12 | 12 | 100.000 | 0.200000 | 0.200000 | 0.200000 | 0.037343 | 0.252896 | 0.252896 |

## Legacy MaxWin Verification

- Verdict: FAIL
- Limit: 240.000 deg
- Values over limit: 5

`Short/LongMaxWinAx[1/4/6]` is the largest legacy 1/1000-sampled joint jump across a 1/10 path window. Values above the limit mean the current coarse verification can miss a large rotation jump.

| sample | n | mean | median | p95 | max | over 240.000 | testId at max | branch | axis | column |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 99 | 0.012913 | 0.006287 | 0.068115 | 0.108614 | 0 | 2 | S | Ax4 | ShortMaxWinAx4 |
| found not in success | 36 | 103.638 | 88.7788 | 298.022 | 298.102 | 5 | 31 | L | Ax6 | LongMaxWinAx6 |

### MaxWin Limit Violations

| sample | testId | branch | axis | column | MaxWin | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| found not in success | 31 | L | Ax6 | LongMaxWinAx6 | 298.102 | 0.200000 | empty |
| found not in success | 22 | L | Ax4 | LongMaxWinAx4 | 298.022 | 0.200000 | empty |
| found not in success | 20 | L | Ax6 | LongMaxWinAx6 | 280.690 | 0.200000 | empty |
| found not in success | 35 | L | Ax6 | LongMaxWinAx6 | 255.303 | 0.200000 | empty |
| found not in success | 12 | L | Ax6 | LongMaxWinAx6 | 242.672 | 0.200000 | empty |

## Legacy MaxWin2 Verification

- Verdict: FAIL
- Limit: 240.000 deg
- Values over limit: 12

`Short/LongMaxWin2Ax[1/4/6]` is the largest legacy 1/1000-sampled joint jump across a 1/10 path window. Values above the limit mean the current coarse verification can miss a large rotation jump.

| sample | n | mean | median | p95 | max | over 240.000 | testId at max | branch | axis | column |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 99 | 0.128206 | 0.062698 | 0.670731 | 1.0839 | 0 | 2 | S | Ax4 | ShortMaxWin2Ax4 |
| found not in success | 36 | 140.000 | 73.5263 | 353.507 | 353.929 | 12 | 22 | L | Ax4 | LongMaxWin2Ax4 |

### MaxWin2 Limit Violations

| sample | testId | branch | axis | column | MaxWin2 | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| found not in success | 22 | L | Ax4 | LongMaxWin2Ax4 | 353.929 | 0.200000 | empty |
| found not in success | 31 | L | Ax6 | LongMaxWin2Ax6 | 353.507 | 0.200000 | empty |
| found not in success | 14 | L | Ax6 | LongMaxWin2Ax6 | 352.681 | 0.200000 | empty |
| found not in success | 20 | L | Ax6 | LongMaxWin2Ax6 | 351.927 | 0.200000 | empty |
| found not in success | 35 | L | Ax6 | LongMaxWin2Ax6 | 348.939 | 0.200000 | empty |
| found not in success | 12 | L | Ax6 | LongMaxWin2Ax6 | 346.377 | 0.200000 | empty |
| found not in success | 28 | L | Ax4 | LongMaxWin2Ax4 | 344.375 | 0.200000 | empty |
| found not in success | 24 | L | Ax6 | LongMaxWin2Ax6 | 332.948 | 0.200000 | empty |
| found not in success | 17 | L | Ax4 | LongMaxWin2Ax4 | 331.425 | 0.200000 | empty |
| found not in success | 27 | L | Ax4 | LongMaxWin2Ax4 | 329.297 | 0.200000 | empty |
| found not in success | 34 | L | Ax6 | LongMaxWin2Ax6 | 302.856 | 0.200000 | empty |
| found not in success | 2 | L | Ax4 | LongMaxWin2Ax4 | 272.422 | 0.200000 | empty |

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 33 | 0.200000 | 0.200000 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 0 | n/a | n/a | n/a | n/a | n/a |
| L successful | 0 | n/a | n/a | n/a | n/a | n/a |
| L found unsuccessful | 12 | 0.200000 | 0.200000 | 0.200000 | 0.200000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 4
- CalcC/PathL mismatches: 4
- Worst valid delta: test 16, C vs CalcC, axis 5, 0.012900 deg

| testId | confId | comparison | max abs deg | axis | control branch |
| --- | --- | --- | --- | --- | --- |
| 24 | 2 | C vs PathL | n/a | n/a | none |
| 24 | 2 | CalcC vs PathL | n/a | n/a | none |
| 27 | 4 | C vs PathL | n/a | n/a | none |
| 27 | 4 | CalcC vs PathL | n/a | n/a | none |
| 34 | 5 | C vs PathL | n/a | n/a | none |
| 34 | 5 | CalcC vs PathL | n/a | n/a | none |
| 35 | 5 | C vs PathL | n/a | n/a | none |
| 35 | 5 | CalcC vs PathL | n/a | n/a | none |

## Branch Matching

- Control branch counts: S=33, L=0, none=4
- ControlMatchShort XOR ControlMatchLong violations: 37
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=32, L=4, none=1
- Legacy/control branch disagreements: 5
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

| testId | confId | ControlMatchShort | ControlMatchLong |
| --- | --- | --- | --- |
| 1 | 9 | True | True |
| 2 | 8 | True | True |
| 3 | 9 | True | True |
| 4 | 2 | True | True |
| 5 | 7 | True | True |
| 6 | 5 | True | True |
| 7 | 2 | True | True |
| 8 | 5 | True | True |
| 9 | 6 | True | True |
| 10 | 8 | True | True |
| 11 | 7 | True | True |
| 12 | 2 | True | True |
| 13 | 2 | True | True |
| 14 | 8 | True | True |
| 15 | 2 | True | True |
| 16 | 2 | True | True |
| 17 | 7 | True | True |
| 19 | 8 | True | True |
| 20 | 2 | True | True |
| 21 | 5 | True | True |
| 22 | 2 | True | True |
| 23 | 5 | True | True |
| 24 | 2 | False | False |
| 24 | 5 | True | True |
| 25 | 2 | True | True |
| 26 | 5 | True | True |
| 27 | 4 | False | False |
| 27 | 5 | True | True |
| 28 | 4 | True | True |
| 29 | 5 | True | True |
| 30 | 1 | True | True |
| 31 | 4 | True | True |
| 32 | 2 | True | True |
| 34 | 2 | True | True |
| 34 | 5 | False | False |
| 35 | 5 | False | False |
| 35 | 8 | True | True |

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| S | S | 32 |
| S | none | 1 |
| none | L | 4 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 33 | 0.000348 | 0.000144 | 0.001605 | 0.002405 | 0.200000 |
| S ControlMaxAx4 successful | 33 | 0.001845 | 0.001187 | 0.007218 | 0.010812 | 0.200000 |
| S ControlMaxAx6 successful | 33 | 0.001837 | 0.000865 | 0.007542 | 0.010269 | 0.200000 |
| S ControlMaxAx1 unsuccessful | 2 | 0.000178 | 0.000178 | 0.000198 | 0.000198 | 0.200000 |
| S ControlMaxAx4 unsuccessful | 2 | 0.000475 | 0.000475 | 0.000850 | 0.000850 | 0.200000 |
| S ControlMaxAx6 unsuccessful | 2 | 0.000510 | 0.000510 | 0.000690 | 0.000690 | 0.200000 |
| L ControlMaxAx1 successful | 0 | n/a | n/a | n/a | n/a | n/a |
| L ControlMaxAx4 successful | 0 | n/a | n/a | n/a | n/a | n/a |
| L ControlMaxAx6 successful | 0 | n/a | n/a | n/a | n/a | n/a |
| L ControlMaxAx1 unsuccessful | 35 | 0.001500 | 0.001052 | 0.004773 | 0.007967 | 0.200000 |
| L ControlMaxAx4 unsuccessful | 35 | 0.036536 | 0.022206 | 0.135239 | 0.252896 | 0.200000 |
| L ControlMaxAx6 unsuccessful | 35 | 0.036978 | 0.019988 | 0.155678 | 0.239473 | 0.200000 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 99 | 0.001340 | 0.000675 | 0.006882 | 0.010863 | 2 | S | Ax4 | 0.000039 | 0.010863 | 0.010346 |
| found unsuccessful | 36 | 25.9322 | 24.9841 | 62.1649 | 107.542 | 31 | L | Ax6 | 0.772049 | 62.1649 | 107.542 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 2 | S | 0.000039 | 0.010863 | 0.010346 | Ax4 | 0.010863 | 0.200000 | empty |
| successful | 9 | S | 0.000183 | 0.007812 | 0.008118 | Ax6 | 0.008118 | 0.200000 | empty |
| successful | 34 | S | 0.000473 | 0.005997 | 0.006882 | Ax6 | 0.006882 | 0.200000 | empty |
| successful | 19 | S | 0.000153 | 0.004787 | 0.004639 | Ax4 | 0.004787 | 0.200000 | empty |
| successful | 12 | S | 0.001526 | 0.001511 | 0.003448 | Ax6 | 0.003448 | 0.200000 | empty |
| successful | 24 | S | 0.000016 | 0.002277 | 0.003090 | Ax6 | 0.003090 | 0.200000 | empty |
| successful | 20 | S | 0.002449 | 0.002800 | 0.000153 | Ax4 | 0.002800 | 0.200000 | empty |
| successful | 6 | S | 0.000116 | 0.001717 | 0.002609 | Ax6 | 0.002609 | 0.200000 | empty |
| successful | 3 | S | 0.000675 | 0.000763 | 0.002319 | Ax6 | 0.002319 | 0.200000 | empty |
| successful | 17 | S | 0.000061 | 0.002045 | 0.001221 | Ax4 | 0.002045 | 0.200000 | empty |
| found unsuccessful | 31 | L | 0.772049 | 62.1649 | 107.542 | Ax6 | 107.542 | 0.200000 | empty |
| found unsuccessful | 20 | L | 5.9640 | 10.5322 | 58.4827 | Ax6 | 58.4827 | 0.200000 | empty |
| found unsuccessful | 22 | L | 3.5970 | 54.8750 | 37.3465 | Ax4 | 54.8750 | 0.200000 | empty |
| found unsuccessful | 12 | L | 3.9682 | 16.9821 | 45.7910 | Ax6 | 45.7910 | 0.200000 | empty |
| found unsuccessful | 35 | L | 0.626938 | 22.1245 | 44.6684 | Ax6 | 44.6684 | 0.200000 | empty |
| found unsuccessful | 2 | L | 2.4963 | 41.8696 | 38.9149 | Ax4 | 41.8696 | 0.200000 | empty |
| found unsuccessful | 28 | L | 9.7204 | 39.7481 | 7.7017 | Ax4 | 39.7481 | 0.200000 | empty |
| found unsuccessful | 14 | L | 2.1246 | 37.9116 | 38.7674 | Ax6 | 38.7674 | 0.200000 | empty |
| found unsuccessful | 17 | L | 0.199295 | 35.1013 | 23.3240 | Ax4 | 35.1013 | 0.200000 | empty |
| found unsuccessful | 24 | L | 2.1010 | 26.5927 | 35.0149 | Ax6 | 35.0149 | 0.200000 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 32 | 0.000363 | 0.000153 | 0.001617 | 0.002449 |
| S legacy WinAx1 | 32 | 0.003558 | 0.001419 | 0.016060 | 0.024383 |
| S legacy Win2Ax1 | 32 | 0.035453 | 0.014095 | 0.160553 | 0.242218 |
| S legacy MaxAx4 | 32 | 0.001894 | 0.001213 | 0.007812 | 0.010863 |
| S legacy WinAx4 | 32 | 0.018270 | 0.011999 | 0.073334 | 0.108614 |
| S legacy Win2Ax4 | 32 | 0.181358 | 0.116883 | 0.726166 | 1.0839 |
| S legacy MaxAx6 | 32 | 0.001889 | 0.000946 | 0.008118 | 0.010346 |
| S legacy WinAx6 | 32 | 0.018121 | 0.008255 | 0.076569 | 0.103180 |
| S legacy Win2Ax6 | 32 | 0.179827 | 0.081490 | 0.758606 | 1.0296 |
| L legacy MaxAx1 | 0 | n/a | n/a | n/a | n/a |
| L legacy WinAx1 | 0 | n/a | n/a | n/a | n/a |
| L legacy Win2Ax1 | 0 | n/a | n/a | n/a | n/a |
| L legacy MaxAx4 | 0 | n/a | n/a | n/a | n/a |
| L legacy WinAx4 | 0 | n/a | n/a | n/a | n/a |
| L legacy Win2Ax4 | 0 | n/a | n/a | n/a | n/a |
| L legacy MaxAx6 | 0 | n/a | n/a | n/a | n/a |
| L legacy WinAx6 | 0 | n/a | n/a | n/a | n/a |
| L legacy Win2Ax6 | 0 | n/a | n/a | n/a | n/a |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 32 | 0.999892 | 0.999972 | 0.999992 |
| S | 4 | 32 | 0.997140 | 0.999893 | 0.999977 |
| S | 6 | 32 | 0.997325 | 0.999903 | 0.999980 |
| L | 1 | 0 | n/a | n/a | n/a |
| L | 4 | 0 | n/a | n/a | n/a |
| L | 6 | 0 | n/a | n/a | n/a |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 3476
- Groups with row count != 200: 26
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 5038
- Ratio pair/order issues: 5038
- Mean PathDist: 1.1277
- Max PathDist: 13.9570
- Mean Rotdist: 0.910865
- Max Rotdist: 179.981

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 5038 | 0.011028 | 0.004624 | 0.038147 | 0.416003 |
| PathDist measured from RotRatio rows | 5038 | 2.2443 | 0.045172 | 9.5078 | 13.9570 |
| Rotdist measured from PathRatio rows | 5038 | 0.812830 | 0.000000 | 2.8044 | 179.981 |
| Rotdist measured from RotRatio rows | 5038 | 1.0089 | 0.000000 | 3.3066 | 179.629 |

### PathL Sample Group Issues

| testId | confId | branch | rows | expected |
| --- | --- | --- | --- | --- |
| 1 | 9 | L | 98 | 200 |
| 3 | 9 | L | 98 | 200 |
| 4 | 2 | L | 98 | 200 |
| 5 | 7 | L | 98 | 200 |
| 6 | 5 | L | 98 | 200 |
| 7 | 2 | L | 98 | 200 |
| 8 | 5 | L | 98 | 200 |
| 9 | 6 | L | 98 | 200 |
| 10 | 8 | L | 98 | 200 |
| 11 | 7 | L | 98 | 200 |
| 12 | 2 | L | 30 | 200 |
| 14 | 8 | L | 98 | 200 |
| 15 | 2 | L | 98 | 200 |
| 16 | 2 | L | 98 | 200 |
| 17 | 7 | L | 94 | 200 |
| 19 | 8 | L | 98 | 200 |
| 20 | 2 | L | 98 | 200 |
| 21 | 5 | L | 98 | 200 |
| 23 | 5 | L | 98 | 200 |
| 25 | 2 | L | 98 | 200 |
| 26 | 5 | L | 98 | 200 |
| 28 | 4 | L | 98 | 200 |
| 29 | 5 | L | 98 | 200 |
| 30 | 1 | L | 98 | 200 |
| 31 | 4 | L | 98 | 200 |
| 32 | 2 | L | 98 | 200 |

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - expected 0.01 step) | 5038 | 0.009339 | 0.009449 | 0.010153 | 0.074084 |
| abs(RatioRot - expected 0.01 step) | 5038 | 0.239665 | 0.009224 | 0.910000 | 0.990000 |
| abs(RatioPath - RatioRot) | 5038 | 0.237643 | 0.001503 | 0.919816 | 1.0000 |

### Shortest PathLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 8 | S | 4.2325 | 0.904815 | 100 | 0.009902 | 0.009945 | 0.009944 | 0.009975 | 0.009991 | 100 | 0.008409 | 0.008593 | 0.008595 | 0.008746 | 0.008768 |
| 16 | 2 | L | 4.2924 | 0.749645 | 49 | 0.002018 | 0.011264 | 0.009148 | 0.031220 | 0.050420 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 16 | 2 | S | 4.2924 | 0.749645 | 100 | 0.009713 | 0.010412 | 0.009772 | 0.009799 | 0.074084 | 100 | 0.004833 | 0.008634 | 0.008670 | 0.008726 | 0.008734 |
| 35 | 8 | L | 4.9970 | 0.919403 | 100 | 0.000070 | 0.008612 | 0.008252 | 0.011366 | 0.023089 | 100 | 0.000000 | 0.495000 | 0.495000 | 0.940000 | 0.990000 |
| 35 | 8 | S | 4.9970 | 0.919403 | 100 | 0.008025 | 0.008142 | 0.008143 | 0.008200 | 0.008299 | 100 | 0.007379 | 0.008032 | 0.008022 | 0.008595 | 0.008732 |
| 29 | 5 | L | 5.8958 | 0.311533 | 49 | 0.000827 | 0.008725 | 0.009250 | 0.009362 | 0.010640 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 29 | 5 | S | 5.8958 | 0.311533 | 100 | 0.009179 | 0.009231 | 0.009230 | 0.009272 | 0.009286 | 100 | 0.008662 | 0.010567 | 0.010571 | 0.012288 | 0.012460 |
| 4 | 2 | L | 6.5364 | 0.771259 | 49 | 0.000412 | 0.009229 | 0.008742 | 0.021454 | 0.024199 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 4 | 2 | S | 6.5364 | 0.771259 | 100 | 0.009107 | 0.009150 | 0.009150 | 0.009165 | 0.009186 | 100 | 0.007908 | 0.007938 | 0.007925 | 0.007935 | 0.008365 |
| 23 | 5 | L | 6.6266 | 0.647703 | 49 | 0.008162 | 0.010708 | 0.008306 | 0.026116 | 0.032223 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |

### Shortest RotLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 7 | L | 8.3809 | 0.256409 | 49 | 0.009258 | 0.010052 | 0.009320 | 0.014651 | 0.021208 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 5 | 7 | S | 8.3809 | 0.256409 | 100 | 0.009191 | 0.009216 | 0.009215 | 0.009236 | 0.009240 | 100 | 0.010254 | 0.020657 | 0.010866 | 0.011420 | 0.990000 |
| 29 | 5 | L | 5.8958 | 0.311533 | 49 | 0.000827 | 0.008725 | 0.009250 | 0.009362 | 0.010640 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 29 | 5 | S | 5.8958 | 0.311533 | 100 | 0.009179 | 0.009231 | 0.009230 | 0.009272 | 0.009286 | 100 | 0.008662 | 0.010567 | 0.010571 | 0.012288 | 0.012460 |
| 9 | 6 | L | 8.8749 | 0.447624 | 49 | 0.000043 | 0.009525 | 0.008267 | 0.025759 | 0.034546 | 49 | 0.009044 | 0.729980 | 0.740000 | 0.960000 | 0.980000 |
| 9 | 6 | S | 8.8749 | 0.447624 | 100 | 0.008816 | 0.008843 | 0.008842 | 0.008863 | 0.008887 | 100 | 0.004581 | 0.005908 | 0.005862 | 0.007016 | 0.007150 |
| 23 | 5 | L | 6.6266 | 0.647703 | 49 | 0.008162 | 0.010708 | 0.008306 | 0.026116 | 0.032223 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 23 | 5 | S | 6.6266 | 0.647703 | 100 | 0.008047 | 0.008089 | 0.008090 | 0.008117 | 0.008130 | 100 | 0.007791 | 0.007910 | 0.007912 | 0.008006 | 0.008020 |
| 25 | 2 | L | 11.8719 | 0.657299 | 49 | 0.002622 | 0.009315 | 0.009354 | 0.013911 | 0.016583 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 25 | 2 | S | 11.8719 | 0.657299 | 100 | 0.009462 | 0.009490 | 0.009490 | 0.009509 | 0.009519 | 100 | 0.008173 | 0.008463 | 0.008461 | 0.008704 | 0.009205 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioRot differs from sample | 4979 |
| RatioPath differs from sample | 4893 |
| pair ratios differ | 1739 |
| RatioRot not increasing | 1707 |
| RatioPath not increasing | 24 |
| RatioPath outside 0..1 | 0 |
| odd row is not PathRatio | 0 |
| RatioRot outside 0..1 | 0 |

### PathL Ratio Issue Examples

| problem | testId | confId | branch | PathLength | RotLength | pair | expected | previous RatioPath | RatioPath | RatioRot | odd row mode | even row mode | odd PathDist | even Rotdist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RatioPath not increasing | 1 | 9 | L | 14.0643 | 0.960211 | 45 | 0.450000 | 0.449467 | 0.432814 | 1.0000 | PathRatio | RotRatio | 0.052748 | 5.2790 |
| RatioPath not increasing | 3 | 9 | L | 9.0540 | 1.1562 | 48 | 0.480000 | 0.467921 | 0.466606 | 1.0000 | PathRatio | RotRatio | 0.168671 | 14.9524 |
| RatioPath not increasing | 3 | 9 | L | 9.0540 | 1.1562 | 49 | 0.490000 | 0.466606 | 0.463085 | 1.0000 | PathRatio | RotRatio | 0.232802 | 28.8881 |
| RatioPath not increasing | 4 | 2 | L | 6.5364 | 0.771259 | 46 | 0.460000 | 0.456657 | 0.435801 | 1.0000 | PathRatio | RotRatio | 0.106725 | 5.2032 |
| RatioPath not increasing | 6 | 5 | L | 11.1813 | 0.833681 | 46 | 0.460000 | 0.453770 | 0.452678 | 1.0000 | PathRatio | RotRatio | 0.201888 | 5.6238 |

### PathL Anomaly Statistics

| condition | rows | % rows | PathDist median | PathDist p95 | PathDist max | Rotdist median | Rotdist p95 | Rotdist max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any anomaly | 3478 | 34.5177 | 0.251775 | 10.2147 | 13.9570 | 1.0704 | 8.4725 | 179.981 |
| CfxOK != TRUE | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| FoundBranch mismatch | 3476 | 34.4978 | 0.249898 | 10.2008 | 13.9570 | 1.0726 | 8.4725 | 179.981 |
| PathDist > 1.0000 mm | 1683 | 16.7031 | 6.4635 | 11.0629 | 13.9570 | 1.3825 | 8.7388 | 179.629 |
| Rotdist > 1.0000 deg | 1843 | 18.2910 | 4.8353 | 10.4638 | 13.6934 | 1.8591 | 14.3886 | 179.981 |

### PathL Anomaly Reason Combinations

| conditions | rows | % rows |
| --- | --- | --- |
| FoundBranch mismatch + PathDist > 1.0000 mm + Rotdist > 1.0000 deg | 1198 | 11.8896 |
| FoundBranch mismatch | 1150 | 11.4133 |
| FoundBranch mismatch + Rotdist > 1.0000 deg | 645 | 6.4013 |
| FoundBranch mismatch + PathDist > 1.0000 mm | 483 | 4.7936 |
| PathDist > 1.0000 mm | 2 | 0.019849 |

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 1 | 13.9570 | 14.0643 | 0.960211 | 0.200000 |
| 27 | 13.6934 | 13.7450 | 1.4830 | 0.200000 |
| 26 | 12.0229 | 12.0547 | 1.1120 | 0.200000 |
| 22 | 11.8920 | 11.9352 | 0.739130 | 0.200000 |
| 25 | 11.8268 | 11.8719 | 0.657299 | 0.200000 |
| 32 | 11.6175 | 11.6458 | 1.0675 | 0.200000 |
| 19 | 11.6172 | 11.6458 | 1.0675 | 0.200000 |
| 34 | 11.6114 | 11.6503 | 1.1730 | 0.200000 |
| 7 | 11.3636 | 11.3867 | 0.960211 | 0.200000 |
| 15 | 11.2186 | 11.2868 | 0.775308 | 0.200000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 24 | 179.981 | 8.2902 | 1.2747 | 0.200000 |
| 22 | 179.974 | 11.9352 | 0.739130 | 0.200000 |
| 35 | 179.974 | 4.9970 | 0.919403 | 0.200000 |
| 27 | 179.972 | 13.7450 | 1.4830 | 0.200000 |
| 34 | 179.961 | 11.6503 | 1.1730 | 0.200000 |
| 28 | 35.4964 | 6.7495 | 1.4353 | 0.200000 |
| 14 | 35.0989 | 9.9960 | 1.4183 | 0.200000 |
| 21 | 32.2387 | 9.1931 | 1.2966 | 0.200000 |
| 10 | 31.9951 | 7.5950 | 1.2863 | 0.200000 |
| 3 | 28.8881 | 9.0540 | 1.1555 | 0.200000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
