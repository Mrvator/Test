# ABB MoveL Analysis v16

## Summary

- Tests: 1191
- Tests with success rows: 633
- Success rows: 838
- Tests without success rows: 558
- PathL diagnostic rows: 167786
- PathL groups by test/conf/branch: 839
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=785, L=586
- Found branches without matching successful control branch: S=277, L=274

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 785 | 277 | 35.2866 | 0.100000 | 0.200000 | 0.200000 | 0.529910 | 31.6296 | 938.402 |
| L | 586 | 274 | 46.7577 | 0.050000 | 0.200000 | 0.200000 | 0.945239 | 21.5629 | 255.227 |

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 518 | 0.000391 | 0.137983 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 277 | 0.000100 | 0.097249 | 0.100000 | 0.200000 | 0.200000 |
| L successful | 320 | 0.001563 | 0.095309 | 0.100000 | 0.200000 | 0.200000 |
| L found unsuccessful | 274 | 0.000195 | 0.065202 | 0.050000 | 0.200000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 0
- CalcC/PathL mismatches: 0
- Worst valid delta: test 769, C vs CalcC, axis 1, 0.004652 deg

None.

## Branch Matching

- Control branch counts: S=518, L=320, none=0
- ControlMatchShort XOR ControlMatchLong violations: 0
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=508, L=312, none=18
- Legacy/control branch disagreements: 18
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

None.

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 312 |
| L | none | 8 |
| S | S | 508 |
| S | none | 10 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 518 | 0.465976 | 0.102718 | 0.948607 | 81.6027 | 0.000391 |
| S ControlMaxAx4 successful | 518 | 0.757494 | 0.219243 | 2.5592 | 23.4305 | 0.001563 |
| S ControlMaxAx6 successful | 518 | 0.809920 | 0.237607 | 2.2711 | 71.1849 | 0.000391 |
| S ControlMaxAx1 unsuccessful | 673 | 55.2574 | 0.244410 | 440.351 | 1663.470 | 0.000100 |
| S ControlMaxAx4 unsuccessful | 673 | 31.2574 | 0.844915 | 148.162 | 1534.930 | 0.000100 |
| S ControlMaxAx6 unsuccessful | 673 | 67.1293 | 0.793857 | 512.739 | 1786.820 | 0.000100 |
| L ControlMaxAx1 successful | 320 | 0.341376 | 0.091261 | 0.678666 | 25.9010 | 0.001563 |
| L ControlMaxAx4 successful | 320 | 1.1920 | 0.471487 | 4.3732 | 28.0563 | 0.001563 |
| L ControlMaxAx6 successful | 320 | 1.0375 | 0.504969 | 4.1223 | 8.7605 | 0.005469 |
| L ControlMaxAx1 unsuccessful | 871 | 29.3217 | 0.194166 | 36.8287 | 1594.840 | 0.000100 |
| L ControlMaxAx4 unsuccessful | 871 | 56.9285 | 1.5032 | 165.639 | 1798.450 | 0.000100 |
| L ControlMaxAx6 unsuccessful | 871 | 46.8179 | 1.4369 | 151.107 | 1798.450 | 0.000100 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 2514 | 0.919051 | 0.286473 | 3.4819 | 73.7698 | 370 | S | Ax1 | 73.7698 | 9.4756 | 68.2855 |
| found unsuccessful | 1653 | 4.0379 | 0.492493 | 19.9194 | 158.069 | 217 | S | Ax6 | 0.312642 | 157.991 | 158.069 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 370 | S | 73.7698 | 9.4756 | 68.2855 | Ax1 | 73.7698 | 0.000391 | empty |
| successful | 46 | S | 29.4453 | 21.6827 | 7.9039 | Ax1 | 29.4453 | 0.200000 | empty |
| successful | 136 | L | 28.2660 | 29.1874 | 6.7401 | Ax4 | 29.1874 | 0.001563 | empty |
| successful | 136 | S | 23.2959 | 23.7259 | 5.8597 | Ax4 | 23.7259 | 0.001563 | empty |
| successful | 697 | S | 0.750278 | 22.5719 | 21.9382 | Ax4 | 22.5719 | 0.001563 | empty |
| successful | 103 | S | 5.3821 | 12.7845 | 13.4354 | Ax6 | 13.4354 | 0.003125 | empty |
| successful | 840 | L | 0.124588 | 11.1085 | 10.9348 | Ax4 | 11.1085 | 0.005469 | empty |
| successful | 828 | L | 8.8983 | 10.1159 | 1.8880 | Ax4 | 10.1159 | 0.006250 | empty |
| successful | 184 | S | 10.0936 | 6.9799 | 3.2997 | Ax1 | 10.0936 | 0.004395 | empty |
| successful | 719 | S | 0.254318 | 9.6829 | 9.7812 | Ax6 | 9.7812 | 0.006250 | empty |
| found unsuccessful | 217 | S | 0.312642 | 157.991 | 158.069 | Ax6 | 158.069 | 0.000100 | empty |
| found unsuccessful | 503 | S | 0.330257 | 140.153 | 140.115 | Ax4 | 140.153 | 0.000100 | SINGULAR |
| found unsuccessful | 86 | S | 85.4476 | 134.252 | 91.2622 | Ax4 | 134.252 | 0.000195 | empty |
| found unsuccessful | 161 | L | 0.055725 | 124.706 | 124.949 | Ax6 | 124.949 | 0.000195 | empty |
| found unsuccessful | 709 | S | 0.137193 | 104.698 | 104.805 | Ax6 | 104.805 | 0.000391 | empty |
| found unsuccessful | 545 | S | 0.333916 | 92.2048 | 92.2472 | Ax6 | 92.2472 | 0.000391 | empty |
| found unsuccessful | 47 | L | 81.9625 | 57.3153 | 25.3484 | Ax1 | 81.9625 | 0.000391 | empty |
| found unsuccessful | 919 | L | 0.126663 | 75.5954 | 75.3983 | Ax4 | 75.5954 | 0.000577 | empty |
| found unsuccessful | 85 | S | 0.383093 | 67.9762 | 68.4749 | Ax6 | 68.4749 | 0.000781 | empty |
| found unsuccessful | 85 | L | 0.438099 | 61.6201 | 61.8755 | Ax6 | 61.8755 | 0.000781 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 784 | 0.831007 | 0.116320 | 2.0584 | 85.4476 |
| S legacy WinAx1 | 784 | 4.7817 | 1.1574 | 20.3758 | 171.544 |
| S legacy Win2Ax1 | 784 | 20.4523 | 11.3879 | 91.0181 | 179.142 |
| S legacy MaxAx4 | 784 | 2.6276 | 0.468914 | 9.4406 | 157.991 |
| S legacy WinAx4 | 784 | 14.0681 | 4.3837 | 65.3521 | 230.787 |
| S legacy Win2Ax4 | 784 | 50.5915 | 33.2629 | 152.020 | 265.773 |
| S legacy MaxAx6 | 784 | 2.5509 | 0.458534 | 9.2015 | 158.069 |
| S legacy WinAx6 | 784 | 13.7153 | 4.2544 | 64.9782 | 184.371 |
| S legacy Win2Ax6 | 784 | 50.3554 | 34.2664 | 146.771 | 252.166 |
| L legacy MaxAx1 | 586 | 0.662651 | 0.106273 | 1.4282 | 81.9625 |
| L legacy WinAx1 | 586 | 3.6527 | 1.0491 | 14.2115 | 155.999 |
| L legacy Win2Ax1 | 586 | 18.4987 | 10.0570 | 80.2128 | 173.803 |
| L legacy MaxAx4 | 586 | 3.1966 | 0.896900 | 14.0647 | 124.706 |
| L legacy WinAx4 | 586 | 19.6535 | 8.5333 | 83.1899 | 174.345 |
| L legacy Win2Ax4 | 586 | 70.3892 | 56.5892 | 159.368 | 235.782 |
| L legacy MaxAx6 | 586 | 2.9549 | 0.851942 | 12.1392 | 124.949 |
| L legacy WinAx6 | 586 | 18.5324 | 8.2278 | 76.8891 | 176.768 |
| L legacy Win2Ax6 | 586 | 69.1880 | 57.6112 | 159.695 | 217.804 |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 784 | 0.964000 | 0.733162 | 0.448924 |
| S | 4 | 784 | 0.864417 | 0.531198 | 0.294232 |
| S | 6 | 784 | 0.861704 | 0.509310 | 0.290768 |
| L | 1 | 586 | 0.889475 | 0.566915 | 0.295333 |
| L | 4 | 586 | 0.904806 | 0.588645 | 0.310226 |
| L | 6 | 586 | 0.907591 | 0.604265 | 0.348692 |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 0
- Groups with row count != 200: 1
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 83893
- Ratio pair/order issues: 183
- Mean PathDist: 0.092576
- Max PathDist: 0.665011
- Mean Rotdist: 0.021185
- Max Rotdist: 0.362616

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 83893 | 0.174389 | 0.148265 | 0.401323 | 0.665011 |
| PathDist measured from RotRatio rows | 83893 | 0.010762 | 0.000273 | 0.056924 | 0.658884 |
| Rotdist measured from PathRatio rows | 83893 | 0.032555 | 0.039565 | 0.096913 | 0.362616 |
| Rotdist measured from RotRatio rows | 83893 | 0.009814 | 0.000000 | 0.039565 | 0.111906 |
| PathDist ambiguous ratio rows | 0 | n/a | n/a | n/a | n/a |
| Rotdist ambiguous ratio rows | 0 | n/a | n/a | n/a | n/a |

### PathL Sample Group Issues

| testId | confId | branch | rows | expected |
| --- | --- | --- | --- | --- |
| 810 | 2 | S | 186 | 200 |

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - expected 0.01 step) | 83893 | 0.000287 | 0.000211 | 0.000636 | 0.008716 |
| abs(RatioRot - expected 0.01 step) | 83893 | 0.000017 | 0.000000 | 0.000013 | 0.007896 |
| abs(RatioPath - RatioRot) | 83893 | 0.000270 | 0.000210 | 0.000633 | 0.002443 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioPath differs from sample | 183 |
| RatioRot differs from sample | 170 |
| RatioPath outside 0.01..1 | 3 |
| RatioRot outside 0.01..1 | 3 |

### PathL Anomalies

None.

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 520 | 0.665011 | 2005.770 | 63.5035 | 0.200000 |
| 164 | 0.658884 | 361.375 | 141.614 | 0.200000 |
| 277 | 0.644401 | 1892.430 | 53.6813 | 0.100000 |
| 809 | 0.627341 | 1872.390 | 195.987 | 0.200000 |
| 1169 | 0.623696 | 1956.370 | 153.320 | 0.200000 |
| 506 | 0.623597 | 339.876 | 237.400 | 0.200000 |
| 344 | 0.619836 | 3420.890 | 236.575 | 0.200000 |
| 1165 | 0.616730 | 1132.320 | 17.2446 | 0.200000 |
| 609 | 0.615686 | 2397.450 | 137.774 | 0.200000 |
| 116 | 0.614716 | 1958.300 | 190.310 | 0.200000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 882 | 0.362616 | 693.363 | 300.725 | 0.050000 |
| 1007 | 0.311533 | 596.457 | 163.450 | 0.200000 |
| 618 | 0.303902 | 240.243 | 179.998 | 0.200000 |
| 164 | 0.290740 | 361.375 | 141.614 | 0.200000 |
| 183 | 0.256409 | 735.085 | 282.056 | 0.006250 |
| 278 | 0.237388 | 595.124 | 238.487 | 0.200000 |
| 949 | 0.230700 | 553.679 | 300.429 | 0.006250 |
| 1094 | 0.213062 | 255.398 | 269.982 | 0.200000 |
| 1173 | 0.213062 | 663.025 | 218.794 | 0.100000 |
| 165 | 0.209357 | 822.749 | 182.119 | 0.200000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
