# ABB MoveL Analysis v18

## Test Run Parameters

- XYZ offsets: 0..100 mm
- XZY rotations: 0..100 deg

## Summary

- Tests: 5217
- Tests with success rows: 4515
- Success rows: 5436
- Tests without success rows: 702
- PathL diagnostic rows: 1087200
- PathL groups by test/conf/branch: 5436
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=4747, L=2146
- Found branches without matching successful control branch: S=406, L=1180

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 4747 | 406 | 8.5528 | 0.050000 | 0.200000 | 0.200000 | 0.775933 | 45.7918 | 1744.040 |
| L | 2146 | 1180 | 54.9860 | 0.100000 | 0.200000 | 0.200000 | 0.598460 | 18.2491 | 1509.760 |

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 4413 | 0.000195 | 0.179109 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 406 | 0.000100 | 0.087737 | 0.050000 | 0.200000 | 0.200000 |
| L successful | 1023 | 0.002344 | 0.109686 | 0.100000 | 0.200000 | 0.200000 |
| L found unsuccessful | 1180 | 0.000100 | 0.083049 | 0.100000 | 0.200000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 0
- CalcC/PathL mismatches: 0
- Worst valid delta: test 1822, C vs CalcC, axis 1, 0.005000 deg

None.

## Branch Matching

- Control branch counts: S=4413, L=1023, none=0
- ControlMatchShort XOR ControlMatchLong violations: 0
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=4341, L=966, none=129
- Legacy/control branch disagreements: 129
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

None.

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 966 |
| L | none | 57 |
| S | S | 4341 |
| S | none | 72 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 4413 | 0.025976 | 0.005083 | 0.025659 | 49.7370 | 0.000195 |
| S ControlMaxAx4 successful | 4413 | 0.318490 | 0.111691 | 0.937344 | 304.024 | 0.000195 |
| S ControlMaxAx6 successful | 4413 | 0.305362 | 0.109602 | 0.930126 | 262.349 | 0.000195 |
| S ControlMaxAx1 unsuccessful | 804 | 2.7537 | 0.005707 | 0.039769 | 1295.980 | 0.000100 |
| S ControlMaxAx4 unsuccessful | 804 | 16.7022 | 0.248155 | 23.8030 | 1744.040 | 0.000100 |
| S ControlMaxAx6 unsuccessful | 804 | 17.7584 | 0.231873 | 25.5688 | 1744.000 | 0.000100 |
| L ControlMaxAx1 successful | 1023 | 0.028822 | 0.015030 | 0.062515 | 3.2841 | 0.012500 |
| L ControlMaxAx4 successful | 1023 | 0.876896 | 0.352396 | 3.7053 | 18.4243 | 0.002344 |
| L ControlMaxAx6 successful | 1023 | 0.887546 | 0.362041 | 3.6818 | 18.5995 | 0.002344 |
| L ControlMaxAx1 unsuccessful | 4194 | 197.884 | 0.022673 | 1336.830 | 1754.490 | 0.000100 |
| L ControlMaxAx4 unsuccessful | 4194 | 228.949 | 1.2842 | 1358.060 | 1798.060 | 0.000100 |
| L ControlMaxAx6 unsuccessful | 4194 | 254.133 | 1.3022 | 1557.360 | 1799.790 | 0.000100 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 16308 | 0.327812 | 0.079407 | 1.3334 | 136.408 | 3189 | S | Ax4 | 42.4772 | 136.408 | 100.556 |
| found unsuccessful | 4758 | 3.8448 | 0.348407 | 17.6938 | 179.999 | 3363 | S | Ax4 | 0.002201 | 179.999 | 179.962 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 3189 | S | 42.4772 | 136.408 | 100.556 | Ax4 | 136.408 | 0.000195 | empty |
| successful | 91 | L | 0.029251 | 19.2488 | 19.4240 | Ax6 | 19.4240 | 0.002344 | empty |
| successful | 1546 | L | 0.089416 | 17.8701 | 17.6279 | Ax4 | 17.8701 | 0.003125 | empty |
| successful | 657 | L | 0.013702 | 15.5989 | 15.7444 | Ax6 | 15.7444 | 0.003125 | empty |
| successful | 95 | L | 0.022675 | 14.6254 | 14.7524 | Ax6 | 14.7524 | 0.003125 | empty |
| successful | 2859 | L | 0.015961 | 14.5700 | 14.7187 | Ax6 | 14.7187 | 0.003125 | empty |
| successful | 2957 | S | 14.6581 | 12.5997 | 2.9033 | Ax1 | 14.6581 | 0.003125 | empty |
| successful | 1380 | L | 0.023460 | 14.0313 | 13.8684 | Ax4 | 14.0313 | 0.006250 | empty |
| successful | 1140 | L | 0.026001 | 11.9211 | 11.7656 | Ax4 | 11.9211 | 0.003125 | empty |
| successful | 1139 | L | 0.017876 | 11.2927 | 11.5026 | Ax6 | 11.5026 | 0.003125 | empty |
| found unsuccessful | 3363 | S | 0.002201 | 179.999 | 179.962 | Ax4 | 179.999 | 0.000100 | SINGULAR |
| found unsuccessful | 4836 | S | 0.006454 | 173.869 | 173.856 | Ax4 | 173.869 | 0.000100 | SINGULAR |
| found unsuccessful | 4855 | L | 0.032703 | 166.223 | 165.997 | Ax4 | 166.223 | 0.000100 | SINGULAR |
| found unsuccessful | 3228 | S | 0.002487 | 160.715 | 160.695 | Ax4 | 160.715 | 0.000100 | SINGULAR |
| found unsuccessful | 5147 | S | 0.026932 | 159.480 | 159.477 | Ax4 | 159.480 | 0.000100 | SINGULAR |
| found unsuccessful | 5217 | S | 0.003464 | 148.522 | 148.600 | Ax6 | 148.600 | 0.000100 | SINGULAR |
| found unsuccessful | 1814 | S | 0.016457 | 141.958 | 141.929 | Ax4 | 141.958 | 0.000100 | empty |
| found unsuccessful | 790 | L | 0.018448 | 140.541 | 140.279 | Ax4 | 140.541 | 0.000100 | SINGULAR |
| found unsuccessful | 2248 | L | 70.5999 | 136.893 | 88.7021 | Ax4 | 136.893 | 0.000195 | empty |
| found unsuccessful | 203 | L | 0.016625 | 126.363 | 126.223 | Ax4 | 126.363 | 0.000391 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 4739 | 0.026406 | 0.005417 | 0.029182 | 42.4772 |
| S legacy WinAx1 | 4739 | 0.179311 | 0.054031 | 0.290859 | 104.677 |
| S legacy Win2Ax1 | 4739 | 1.2026 | 0.531525 | 2.8166 | 168.319 |
| S legacy MaxAx4 | 4739 | 0.890339 | 0.152786 | 2.5025 | 141.958 |
| S legacy WinAx4 | 4739 | 5.6878 | 1.5150 | 21.4455 | 176.346 |
| S legacy Win2Ax4 | 4739 | 26.1787 | 13.4456 | 106.629 | 187.343 |
| S legacy MaxAx6 | 4739 | 0.877016 | 0.149689 | 2.4788 | 141.929 |
| S legacy WinAx6 | 4739 | 5.6220 | 1.4783 | 21.5011 | 176.059 |
| S legacy Win2Ax6 | 4739 | 25.9304 | 13.3384 | 107.743 | 181.274 |
| L legacy MaxAx1 | 2143 | 0.065859 | 0.015892 | 0.060902 | 70.5999 |
| L legacy WinAx1 | 2143 | 0.387781 | 0.158680 | 0.608883 | 165.977 |
| L legacy Win2Ax1 | 2143 | 2.5372 | 1.5548 | 5.7460 | 168.889 |
| L legacy MaxAx4 | 2143 | 2.8296 | 0.549786 | 9.5938 | 136.893 |
| L legacy WinAx4 | 2143 | 15.3532 | 5.3598 | 75.9692 | 242.612 |
| L legacy Win2Ax4 | 2143 | 59.1134 | 43.7293 | 154.052 | 291.920 |
| L legacy MaxAx6 | 2143 | 2.8020 | 0.550507 | 9.8500 | 126.223 |
| L legacy WinAx6 | 2143 | 15.2503 | 5.4084 | 76.0187 | 175.963 |
| L legacy Win2Ax6 | 2143 | 59.2112 | 43.9334 | 158.921 | 194.027 |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 4739 | 0.996796 | 0.780501 | 0.439317 |
| S | 4 | 4739 | 0.912423 | 0.605940 | 0.347874 |
| S | 6 | 4739 | 0.899309 | 0.590995 | 0.336315 |
| L | 1 | 2143 | 0.998459 | 0.907203 | 0.599471 |
| L | 4 | 2143 | 0.943641 | 0.704259 | 0.410939 |
| L | 6 | 2143 | 0.939768 | 0.680352 | 0.369146 |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 0
- Groups with row count != 200: 0
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 543600
- Ratio pair/order issues: 237475
- Mean PathDist: 0.135238
- Max PathDist: 0.928805
- Mean Rotdist: 0.086848
- Max Rotdist: 5.4058

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 543600 | 0.170473 | 0.150345 | 0.385487 | 0.912012 |
| PathDist measured from RotRatio rows | 543600 | 0.100003 | 0.016180 | 0.369474 | 0.928805 |
| Rotdist measured from PathRatio rows | 543600 | 0.162832 | 0.096913 | 0.551073 | 5.4058 |
| Rotdist measured from RotRatio rows | 543600 | 0.010863 | 0.000000 | 0.039565 | 0.193827 |

### PathL Sample Group Issues

None.

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - expected 0.01 step) | 543600 | 0.004691 | 0.002899 | 0.010548 | 0.033792 |
| abs(RatioRot - expected 0.01 step) | 543600 | 0.003159 | 0.000003 | 0.008392 | 0.009517 |
| abs(RatioPath - RatioRot) | 543600 | 0.001702 | 0.001219 | 0.004985 | 0.033562 |

### Shortest PathLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4445 | 7 | S | 12.2351 | 119.602 | 100 | 0.004642 | 0.014988 | 0.015267 | 0.020674 | 0.024403 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 5148 | 3 | S | 15.2211 | 127.097 | 100 | 0.000752 | 0.005686 | 0.006679 | 0.008061 | 0.008074 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000001 | 0.000001 |
| 5148 | 2 | L | 15.2211 | 232.903 | 100 | 0.000000 | 0.003950 | 0.003821 | 0.007496 | 0.007551 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 4516 | 2 | S | 15.5954 | 129.114 | 100 | 0.000189 | 0.008021 | 0.008030 | 0.013233 | 0.013277 | 100 | 0.000000 | 0.000001 | 0.000001 | 0.000002 | 0.000002 |
| 1615 | 4 | S | 17.2171 | 111.721 | 100 | 0.001505 | 0.007360 | 0.007573 | 0.010865 | 0.011409 | 100 | 0.000000 | 0.001096 | 0.000002 | 0.007357 | 0.007414 |
| 4623 | 4 | S | 18.6802 | 84.9608 | 100 | 0.000000 | 0.001773 | 0.001602 | 0.003867 | 0.005947 | 100 | 0.000001 | 0.006638 | 0.007502 | 0.007707 | 0.007745 |
| 2601 | 5 | L | 18.6802 | 275.039 | 100 | 0.000000 | 0.001736 | 0.001630 | 0.003628 | 0.004316 | 100 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 562 | 2 | S | 18.6803 | 84.9608 | 100 | 0.001354 | 0.005697 | 0.006396 | 0.009324 | 0.009520 | 100 | 0.007023 | 0.007619 | 0.007695 | 0.008141 | 0.008170 |
| 1346 | 9 | S | 18.6803 | 84.9608 | 100 | 0.005400 | 0.008156 | 0.008452 | 0.010650 | 0.010819 | 100 | 0.007407 | 0.007534 | 0.007523 | 0.007699 | 0.007725 |
| 2385 | 5 | S | 18.6803 | 84.9608 | 100 | 0.004300 | 0.007561 | 0.007675 | 0.009955 | 0.010140 | 100 | 0.007798 | 0.008240 | 0.008289 | 0.008405 | 0.008426 |

### Shortest RotLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-expected) n | abs(RatioPath-expected) min | abs(RatioPath-expected) mean | abs(RatioPath-expected) median | abs(RatioPath-expected) p95 | abs(RatioPath-expected) max | abs(RatioRot-expected) n | abs(RatioRot-expected) min | abs(RatioRot-expected) mean | abs(RatioRot-expected) median | abs(RatioRot-expected) p95 | abs(RatioRot-expected) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4834 | 4 | S | 84.6303 | 21.4425 | 100 | 0.002110 | 0.007500 | 0.008393 | 0.009550 | 0.009565 | 100 | 0.000001 | 0.006926 | 0.008088 | 0.008853 | 0.008890 |
| 654 | 7 | S | 84.6304 | 21.4425 | 100 | 0.007259 | 0.009045 | 0.009401 | 0.009765 | 0.009769 | 100 | 0.006619 | 0.007983 | 0.008163 | 0.008711 | 0.008724 |
| 704 | 8 | S | 119.723 | 21.8293 | 100 | 0.009532 | 0.009610 | 0.009610 | 0.009681 | 0.009690 | 100 | 0.008881 | 0.008932 | 0.008940 | 0.008962 | 0.008966 |
| 2196 | 5 | S | 119.723 | 21.8293 | 100 | 0.000483 | 0.006172 | 0.007760 | 0.008818 | 0.008853 | 100 | 0.000000 | 0.003992 | 0.005258 | 0.006316 | 0.006392 |
| 2293 | 2 | S | 124.563 | 21.8293 | 100 | 0.009056 | 0.009122 | 0.009112 | 0.009238 | 0.009262 | 100 | 0.008496 | 0.008567 | 0.008568 | 0.008622 | 0.008624 |
| 388 | 5 | S | 128.622 | 21.8293 | 100 | 0.007415 | 0.008896 | 0.009100 | 0.009263 | 0.009286 | 100 | 0.007712 | 0.008855 | 0.008988 | 0.009099 | 0.009138 |
| 1667 | 5 | S | 128.622 | 21.8293 | 100 | 0.002763 | 0.006394 | 0.006956 | 0.007754 | 0.007871 | 100 | 0.000047 | 0.005559 | 0.006688 | 0.007279 | 0.007386 |
| 2100 | 5 | S | 128.622 | 21.8293 | 100 | 0.000892 | 0.004697 | 0.006459 | 0.007332 | 0.008094 | 100 | 0.000001 | 0.004640 | 0.007536 | 0.008711 | 0.009191 |
| 2566 | 9 | S | 128.622 | 21.8293 | 100 | 0.007077 | 0.007600 | 0.008015 | 0.008046 | 0.008049 | 100 | 0.007635 | 0.008024 | 0.008303 | 0.008361 | 0.008368 |
| 3221 | 6 | S | 128.622 | 21.8293 | 100 | 0.006926 | 0.008058 | 0.008133 | 0.008230 | 0.008247 | 100 | 0.007217 | 0.008212 | 0.008281 | 0.008310 | 0.008357 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioPath differs from sample | 226602 |
| RatioRot differs from sample | 212653 |
| pair ratios differ | 17716 |
| RatioPath not increasing | 974 |
| RatioPath outside 0..1 | 0 |
| odd row is not PathRatio | 0 |
| RatioRot outside 0..1 | 0 |

### PathL Ratio Issue Examples

| problem | testId | confId | branch | PathLength | RotLength | pair | expected | previous RatioPath | RatioPath | RatioRot | odd row mode | even row mode | odd PathDist | even Rotdist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RatioPath not increasing | 11 | 4 | S | 86.7290 | 91.3692 | 25 | 0.250000 | 0.240911 | 0.238878 | 0.242349 | PathRatio | RotRatio | 0.121804 | 0.000000 |
| RatioPath not increasing | 18 | 6 | S | 55.0830 | 79.0757 | 51 | 0.510000 | 0.501639 | 0.497913 | 0.503031 | PathRatio | RotRatio | 0.219049 | 0.000000 |
| RatioPath not increasing | 44 | 5 | S | 116.838 | 108.541 | 7 | 0.070000 | 0.060139 | 0.059797 | 0.062320 | PathRatio | RotRatio | 0.142498 | 0.000000 |
| RatioPath not increasing | 59 | 8 | S | 101.223 | 93.7654 | 81 | 0.810000 | 0.800069 | 0.800051 | 0.802637 | PathRatio | RotRatio | 0.228781 | 0.000000 |
| RatioPath not increasing | 63 | 3 | S | 84.3713 | 82.6325 | 8 | 0.080000 | 0.070097 | 0.069972 | 0.072238 | PathRatio | RotRatio | 0.076799 | 0.000000 |

### PathL Anomaly Statistics

| condition | rows | % rows | PathDist median | PathDist p95 | PathDist max | Rotdist median | Rotdist p95 | Rotdist max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any anomaly | 5672 | 0.521707 | 0.204815 | 0.407957 | 0.614020 | 1.2140 | 2.4374 | 5.4058 |
| CfxOK != TRUE | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| FoundBranch mismatch | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| PathDist > 1.0000 mm | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| Rotdist > 1.0000 deg | 5672 | 0.521707 | 0.204815 | 0.407957 | 0.614020 | 1.2140 | 2.4374 | 5.4058 |

### PathL Anomaly Reason Combinations

| conditions | rows | % rows |
| --- | --- | --- |
| Rotdist > 1.0000 deg | 5672 | 0.521707 |

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 3918 | 0.928805 | 93.7568 | 80.0247 | 0.200000 |
| 3436 | 0.912012 | 80.0784 | 50.3741 | 0.100000 |
| 482 | 0.908988 | 112.858 | 65.8347 | 0.200000 |
| 4768 | 0.861703 | 73.1775 | 88.0763 | 0.200000 |
| 2963 | 0.859134 | 94.6164 | 89.1171 | 0.200000 |
| 2734 | 0.842123 | 132.757 | 94.3058 | 0.200000 |
| 3559 | 0.837839 | 127.273 | 83.1285 | 0.200000 |
| 3859 | 0.834256 | 74.9303 | 78.3916 | 0.100000 |
| 1023 | 0.828597 | 68.4434 | 72.1467 | 0.200000 |
| 2773 | 0.814780 | 90.5057 | 90.6141 | 0.050000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 4914 | 5.4058 | 18.6804 | 275.039 | 0.100000 |
| 3782 | 4.2140 | 18.6803 | 275.039 | 0.200000 |
| 163 | 3.6170 | 21.3106 | 230.886 | 0.200000 |
| 2130 | 3.5544 | 42.3602 | 269.669 | 0.200000 |
| 1511 | 3.4208 | 28.5782 | 256.066 | 0.025000 |
| 4605 | 3.1099 | 21.9336 | 120.617 | 0.200000 |
| 4445 | 2.8986 | 12.2351 | 119.602 | 0.100000 |
| 5014 | 2.8799 | 41.9815 | 292.913 | 0.200000 |
| 640 | 2.8638 | 36.7293 | 231.639 | 0.200000 |
| 1958 | 2.8441 | 31.1260 | 334.338 | 0.200000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
