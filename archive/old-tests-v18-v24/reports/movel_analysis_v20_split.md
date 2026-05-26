# ABB MoveL Analysis v20

## Summary

- Tests: 537
- Test PathLength range: n/a..n/a mm (n=0)
- Test RotLength range: n/a..n/a deg (n=0)
- Tests with success rows: 491
- Successful trajectories (testId+confId): 567
- Successful trajectories where PathL_rax differs from C_rax by > 1.0000 deg on any axis: 0
- Successful trajectories where PathL_rax vs C_rax cannot be compared: 2
- Successful trajectories where ControlMatchShort XOR ControlMatchLong is false: 15
- Success rows where MatchesShort XOR MatchesLong is false: 9
- Tests without success rows: 46
- Success rows: 567
- PathL diagnostic rows: 114394
- PathL groups by test/conf/branch: 578
- Joint tolerance: 1.0 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## PathL Length Overview

Lengths here are read from raw `pathl.csv` values. The graph script groups duplicate sample rows by `testId/confId/branch`, but it does not recalculate `PathLength` or `RotLength` from A/B poses.

- PathL length overview skipped: [Errno 13] Permission denied: 'reports\\pathl_length_outcome_map_v20.svg'

## Found But Unsuccessful Branches

These are only context: `success.csv` is the evaluated set because those MoveL attempts actually ran through.

- Found branches in tests.csv: S=500, L=211
- Found branches without matching successful control branch: S=12, L=143

| branch | found | unsuccessful | unsuccessful % | FinestStep median | FinestStep p95 | FinestStep max | jump median | jump p95 | jump max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 500 | 12 | 2.4000 | 0.050000 | 0.200000 | 0.200000 | 0.974920 | 18.4282 | 18.4282 |
| L | 211 | 143 | 67.7725 | 0.050000 | 0.100000 | 0.200000 | 0.945660 | 16.7517 | 118.630 |

## Joint Configuration Delta Outcome

`branch delta` is the Euclidean joint distance from `A_rax*` to the branch-specific `ControlShort/ControlLong_rax*` target. This keeps the short/long branch outcome separate and exposes long-branch 360 deg turns that raw `A_rax*` to `B_rax*` can hide.

- Binned data: `reports/joint_config_delta_bins_v20.csv`
- Likely short-only context uses branch `S`, `short_long_gap_max_deg >= 300.000`, and raw `A->B` bins.

### Branch Delta Bins

| branch | branch delta L2 bin deg | found | successful | unsuccessful | success % | max-axis median | max-axis p95 | max-axis max | turn-axis median | turn-axis p95 | turn-axis max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | 2-5 | 3 | 3 | 0 | 100.000 | 2.8225 | 3.0823 | 3.0823 | 2.4050 | 3.0823 | 3.0823 |
| S | 5-10 | 55 | 54 | 1 | 98.1818 | 5.9700 | 8.1351 | 8.8556 | 4.6960 | 8.0010 | 8.4818 |
| S | 10-20 | 204 | 204 | 0 | 100.000 | 10.4935 | 15.2160 | 16.9280 | 9.2490 | 14.6054 | 16.9280 |
| S | 20-45 | 153 | 152 | 1 | 99.3464 | 20.1987 | 31.1670 | 35.4800 | 19.6150 | 31.1340 | 35.4800 |
| S | 45-90 | 53 | 51 | 2 | 96.2264 | 41.8888 | 61.4610 | 64.6000 | 41.8888 | 61.4610 | 64.6000 |
| S | 90-180 | 20 | 16 | 4 | 80.0000 | 104.454 | 123.403 | 126.345 | 104.454 | 123.403 | 126.345 |
| S | 180-270 | 12 | 8 | 4 | 66.6667 | 149.734 | 182.995 | 182.995 | 149.734 | 182.995 | 182.995 |
| L | 2-5 | 1 | 1 | 0 | 100.000 | 2.5567 | 2.5567 | 2.5567 | 2.4050 | 2.4050 | 2.4050 |
| L | 5-10 | 1 | 1 | 0 | 100.000 | 5.5330 | 5.5330 | 5.5330 | 5.5330 | 5.5330 | 5.5330 |
| L | 10-20 | 1 | 1 | 0 | 100.000 | 10.0900 | 10.0900 | 10.0900 | 10.0900 | 10.0900 | 10.0900 |
| L | 20-45 | 1 | 1 | 0 | 100.000 | 15.3090 | 15.3090 | 15.3090 | 15.3090 | 15.3090 | 15.3090 |
| L | 180-270 | 8 | 2 | 6 | 25.0000 | 228.181 | 246.900 | 246.900 | 228.181 | 246.900 | 246.900 |
| L | 270-360 | 191 | 61 | 130 | 31.9372 | 348.302 | 356.918 | 359.570 | 348.302 | 356.918 | 359.570 |
| L | 360-540 | 8 | 5 | 3 | 62.5000 | 362.883 | 369.889 | 369.889 | 362.883 | 369.889 | 369.889 |

### Likely Short-Only Raw A-to-B Context

None.

### Largest Successful Short Deltas

| testId | confId | branch | successful | branch L2 | branch min | branch max | max axis | turn max | raw A->B L2 | raw A->B max | short/long gap | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 75 | 4 | S | yes | 217.705 | 0.128910 | 154.309 | Ax6 | 154.309 | 277.140 | 270.001 | n/a | 0.100000 | empty |
| 83 | 2 | S | yes | 212.273 | 0.267300 | 149.946 | Ax4 | 149.946 | 229.475 | 180.001 | n/a | 0.100000 | empty |
| 507 | 1 | S | yes | 210.258 | 0.970400 | 151.029 | Ax4 | 151.029 | 98.8075 | 45.0020 | 360.000 | 0.100000 | empty |
| 31 | 4 | S | yes | 207.121 | 0.280995 | 149.523 | Ax4 | 149.523 | 331.312 | 315.001 | 360.000 | 0.200000 | empty |
| 363 | 7 | S | yes | 201.227 | 0.043059 | 143.508 | Ax6 | 143.508 | 473.247 | 450.002 | n/a | 0.200000 | empty |
| 277 | 6 | S | yes | 194.271 | 2.4151 | 137.354 | Ax6 | 137.354 | 720.334 | 675.002 | n/a | 0.050000 | empty |
| 497 | 5 | S | yes | 188.732 | 0.122000 | 137.292 | Ax6 | 137.292 | 572.211 | 495.001 | 360.000 | 0.100000 | empty |
| 172 | 9 | S | yes | 180.868 | 0.338000 | 132.855 | Ax6 | 132.855 | 757.866 | 720.001 | n/a | 0.200000 | empty |

### Smallest Unsuccessful Short Deltas

| testId | confId | branch | successful | branch L2 | branch min | branch max | max axis | turn max | raw A->B L2 | raw A->B max | short/long gap | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18 | n/a | S | no | 9.8828 | 0.071000 | 8.1351 | Ax4 | 8.1351 | 107.759 | 90.0003 | 360.000 | 0.200000 | empty |
| 245 | n/a | S | no | 32.5229 | 1.9299 | 24.9754 | Ax6 | 24.9754 | 460.776 | 359.999 | 360.000 | 0.200000 | empty |
| 531 | n/a | S | no | 51.6322 | 0.132500 | 38.1350 | Ax6 | 38.1350 | 425.544 | 360.000 | n/a | 0.200000 | empty |
| 235 | n/a | S | no | 89.1265 | 0.084600 | 64.6000 | Ax6 | 64.6000 | 663.257 | 630.001 | n/a | 0.200000 | empty |
| 152 | n/a | S | no | 118.326 | 0.764930 | 86.4020 | Ax6 | 86.4020 | 606.743 | 585.000 | 360.000 | 0.050000 | empty |
| 346 | n/a | S | no | 142.337 | 1.5444 | 102.562 | Ax6 | 102.562 | 380.144 | 359.999 | 360.000 | 0.012500 | empty |
| 532 | n/a | S | no | 144.714 | 1.2392 | 106.109 | Ax4 | 106.109 | 304.796 | 225.001 | 360.000 | 0.100000 | empty |
| 453 | n/a | S | no | 146.508 | 0.335600 | 103.766 | Ax6 | 103.766 | 285.043 | 224.999 | n/a | 0.012500 | empty |

### Successful Long Cases Near 360 Deg

| testId | confId | branch | successful | branch L2 | branch min | branch max | max axis | turn max | raw A->B L2 | raw A->B max | short/long gap | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 90 | 4 | L | yes | 359.670 | 3.8484 | 359.089 | Ax6 | 359.089 | 160.354 | 90.0010 | 360.000 | 0.100000 | empty |
| 287 | 2 | L | yes | 359.187 | 0.712900 | 359.049 | Ax4 | 359.049 | 164.789 | 135.000 | 360.000 | 0.004395 | empty |
| 402 | 5 | L | yes | 361.449 | 0.262900 | 360.394 | Ax6 | 360.394 | 89.3179 | 51.3000 | 360.000 | 0.100000 | empty |
| 153 | 5 | L | yes | 357.249 | 1.0805 | 357.220 | Ax6 | 357.220 | 406.740 | 315.001 | 360.000 | 0.100000 | empty |
| 427 | 4 | L | yes | 357.146 | 2.8640 | 356.840 | Ax6 | 356.840 | 603.900 | 585.001 | 360.000 | 0.012500 | empty |
| 199 | 4 | L | yes | 357.048 | 1.9215 | 356.974 | Ax4 | 356.974 | 327.734 | 270.001 | 360.000 | 0.018750 | empty |
| 527 | 2 | L | yes | 356.932 | 0.408900 | 356.918 | Ax6 | 356.918 | 463.576 | 405.002 | 360.000 | 0.050000 | empty |
| 239 | 5 | L | yes | 364.127 | 0.594000 | 363.925 | Ax6 | 363.925 | 691.411 | 675.000 | 360.000 | 0.050000 | empty |

### Unsuccessful Long Cases Near 360 Deg

| testId | confId | branch | successful | branch L2 | branch min | branch max | max axis | turn max | raw A->B L2 | raw A->B max | short/long gap | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 56 | n/a | L | no | 359.645 | 1.0477 | 359.570 | Ax6 | 359.570 | 209.088 | 179.999 | 360.000 | 0.025000 | empty |
| 491 | n/a | L | no | 360.692 | 0.235100 | 360.501 | Ax6 | 360.501 | 184.210 | 134.999 | 360.000 | 0.006250 | empty |
| 463 | n/a | L | no | 358.777 | 2.2650 | 358.611 | Ax4 | 358.611 | 238.639 | 180.001 | 360.000 | 0.014356 | empty |
| 392 | n/a | L | no | 361.557 | 0.673600 | 361.414 | Ax6 | 361.414 | 259.943 | 180.000 | 360.000 | 0.003516 | empty |
| 81 | n/a | L | no | 362.043 | 0.295400 | 361.840 | Ax6 | 361.840 | 169.828 | 134.999 | 360.000 | 0.025000 | empty |
| 167 | n/a | L | no | 357.653 | 1.2264 | 357.549 | Ax4 | 357.549 | 189.080 | 134.999 | 360.000 | 0.012500 | empty |
| 496 | n/a | L | no | 357.241 | 0.258000 | 357.176 | Ax4 | 357.176 | 723.139 | 720.000 | 360.000 | 0.050000 | empty |
| 78 | n/a | L | no | 357.182 | 0.816100 | 356.957 | Ax6 | 356.957 | 536.783 | 405.002 | 360.000 | 0.001222 | empty |

## Branch Timing

`TimeLegacyS/L` is the fixed 1/1000 legacy lift timing. `TimeS/L` is the current adaptive implementation timing. `legacy/adaptive median` is the median speedup factor; values above 1 mean adaptive is faster.

- Timing columns not present in `tests_v20.csv`: TimeLegacyS, TimeLegacyL, TimeS, TimeL


## Aggregated Jump Summary

The same pooled max-jump statistic is reported separately for short and long branches, so successful and rejected branch boundaries do not hide each other.


### Short branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 0.824081 | 277 | 6 | S | Ax6 | 0.824081 | 8.2273 | 71.4908 |
| Successful | MaxWin | 8.2273 | 277 | 6 | S | Ax6 | 0.824081 | 8.2273 | 71.4908 |
| Successful | MaxWin2 | 71.4908 | 277 | 6 | S | Ax6 | 0.824081 | 8.2273 | 71.4908 |
| Unsuccessful | MaxAx | 19.4721 | 515 | n/a | S | Ax4 | 19.4721 | 120.805 | 173.878 |
| Unsuccessful | MaxWin | 120.805 | 515 | n/a | S | Ax4 | 19.4721 | 120.805 | 173.878 |
| Unsuccessful | MaxWin2 | 173.878 | 515 | n/a | S | Ax4 | 19.4721 | 120.805 | 173.878 |

### Long branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 11.9959 | 316 | 4 | L | Ax4 | 11.9959 | 93.7431 | 184.066 |
| Successful | MaxWin | 93.7431 | 316 | 4 | L | Ax4 | 11.9959 | 93.7431 | 184.066 |
| Successful | MaxWin2 | 184.066 | 316 | 4 | L | Ax4 | 11.9959 | 93.7431 | 184.066 |
| Unsuccessful | MaxAx | 85.6181 | 161 | n/a | L | Ax4 | 85.6181 | 171.274 | 196.227 |
| Unsuccessful | MaxWin | 171.274 | 161 | n/a | L | Ax4 | 85.6181 | 171.274 | 196.227 |
| Unsuccessful | MaxWin2 | 347.083 | 164 | n/a | L | Ax6 | 47.2030 | 156.437 | 347.083 |

## Legacy MaxWin Verification

- Verdict: PASS
- Limit: 240.000 deg
- Values over limit (successful branches only): 0

`Short/LongMaxWinAx[1/4/6]` is the largest legacy 1/1000-sampled joint jump across a 1/10 path window. Values above the limit mean the current coarse verification can miss a large rotation jump.

Limit evaluation is applied only to `successful` branches; `found not in success` rows are shown as context.

| sample | n | mean | median | p95 | max | over 240.000 | testId at max | branch | axis | column |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 1695 | 1.4746 | 0.088562 | 6.3872 | 93.7431 | 0 | 316 | L | Ax4 | LongMaxWinAx4 |
| found not in success | 465 | 17.5365 | 6.4562 | 83.5497 | 171.274 | n/a | 161 | L | Ax4 | LongMaxWinAx4 |

### MaxWin Limit Violations

None.

## Legacy MaxWin2 Verification

- Verdict: PASS
- Limit: 240.000 deg
- Values over limit (successful branches only): 0

`Short/LongMaxWin2Ax[1/4/6]` is the largest legacy 1/1000-sampled joint jump across a 1/10 path window. Values above the limit mean the current coarse verification can miss a large rotation jump.

Limit evaluation is applied only to `successful` branches; `found not in success` rows are shown as context.

| sample | n | mean | median | p95 | max | over 240.000 | testId at max | branch | axis | column |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 1695 | 8.0506 | 0.879852 | 57.2300 | 184.066 | 0 | 316 | L | Ax4 | LongMaxWin2Ax4 |
| found not in success | 465 | 58.1254 | 51.3617 | 160.333 | 347.083 | n/a | 164 | L | Ax6 | LongMaxWin2Ax6 |

### MaxWin2 Limit Violations

None.

## FinestStep Success Boundary

`successful` means the branch appears in `success.csv`. `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

| sample | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| S successful | 491 | 0.050000 | 0.198676 | 0.200000 | 0.200000 | 0.200000 |
| S found unsuccessful | 12 | 0.003125 | 0.086979 | 0.050000 | 0.200000 | 0.200000 |
| L successful | 74 | 0.003125 | 0.056309 | 0.050000 | 0.100000 | 0.100000 |
| L found unsuccessful | 143 | 0.000391 | 0.052393 | 0.050000 | 0.100000 | 0.200000 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 2
- CalcC/PathL mismatches: 2
- Worst valid delta: test 291, C vs CalcC, axis 1, 0.007700 deg

| testId | confId | comparison | max abs deg | axis | control branch |
| --- | --- | --- | --- | --- | --- |
| 76 | 2 | C vs PathL | n/a | n/a | none |
| 76 | 2 | CalcC vs PathL | n/a | n/a | none |
| 443 | 5 | C vs PathL | n/a | n/a | none |
| 443 | 5 | CalcC vs PathL | n/a | n/a | none |

## Branch Matching

- Control branch counts: S=491, L=74, none=2
- ControlMatchShort XOR ControlMatchLong violations: 15
- C vs selected Control target mismatches: S=0, L=0
- Legacy Matches counts: S=488, L=70, none=9
- MatchesShort XOR MatchesLong violations: 9
- Legacy/control branch disagreements: 11
- C vs selected Lift target mismatches: S=0, L=0

### Control XOR Violations

| testId | confId | ControlMatchShort | ControlMatchLong |
| --- | --- | --- | --- |
| 4 | 3 | True | True |
| 30 | 5 | True | True |
| 55 | 5 | True | True |
| 66 | 4 | True | True |
| 69 | 5 | True | True |
| 76 | 2 | False | False |
| 76 | 5 | True | True |
| 131 | 5 | True | True |
| 164 | 5 | True | True |
| 177 | 3 | True | True |
| 311 | 9 | True | True |
| 365 | 1 | True | True |
| 443 | 2 | True | True |
| 443 | 5 | False | False |
| 458 | 5 | True | True |

### Legacy XOR Violations

| testId | confId | MatchesShort | MatchesLong |
| --- | --- | --- | --- |
| 33 | 4 | False | False |
| 85 | 8 | False | False |
| 116 | 1 | False | False |
| 125 | 2 | False | False |
| 187 | 1 | False | False |
| 238 | 2 | False | False |
| 349 | 4 | False | False |
| 372 | 5 | False | False |
| 409 | 1 | False | False |

### Control Target Mismatches

None.

### Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 68 |
| L | none | 6 |
| S | S | 488 |
| S | none | 3 |
| none | L | 2 |

### Legacy Lift Target Mismatches

None.

## Control Jump Boundaries

`Control[Short/Long]MaxAx[1/4/6]` is treated as the largest adaptive-step jump normalized to 1/1000 sampling. `FinestStep at max` is the adaptive sampling step from the row where the maximum was found.

| sample | n | mean | median | p95 | max | FinestStep at max |
| --- | --- | --- | --- | --- | --- | --- |
| S ControlMaxAx1 successful | 491 | 0.004080 | 0.001742 | 0.011906 | 0.392999 | 0.100000 |
| S ControlMaxAx4 successful | 491 | 0.030526 | 0.012190 | 0.115708 | 0.780876 | 0.050000 |
| S ControlMaxAx6 successful | 491 | 0.030336 | 0.012425 | 0.113073 | 0.781252 | 0.050000 |
| S ControlMaxAx1 unsuccessful | 46 | 0.003132 | 0.001408 | 0.008268 | 0.059578 | 0.200000 |
| S ControlMaxAx4 unsuccessful | 46 | 1.0520 | 0.016011 | 4.6046 | 18.4282 | 0.003125 |
| S ControlMaxAx6 unsuccessful | 46 | 1.0539 | 0.019553 | 4.6092 | 18.4179 | 0.003125 |
| L ControlMaxAx1 successful | 74 | 0.038442 | 0.021341 | 0.097380 | 0.741642 | 0.025000 |
| L ControlMaxAx4 successful | 74 | 1.5775 | 0.741985 | 7.2001 | 11.2957 | 0.003125 |
| L ControlMaxAx6 successful | 74 | 1.5794 | 0.725388 | 7.0439 | 10.9808 | 0.003125 |
| L ControlMaxAx1 unsuccessful | 463 | 207.284 | 0.030204 | 1339.690 | 1449.510 | 0.000100 |
| L ControlMaxAx4 unsuccessful | 463 | 258.476 | 1.8144 | 1500.490 | 1796.760 | 0.000100 |
| L ControlMaxAx6 unsuccessful | 463 | 250.949 | 1.8606 | 1439.420 | 1790.600 | 0.000100 |

## Legacy 1/1000 MaxAx Boundary

`Short/LongMaxAx[1/4/6]` comes from the legacy fixed 1/1000 sampling. `successful` means the exact S/L branch appears in `success.csv`; `found unsuccessful` means `tests.csv` found the branch, but there is no matching successful control branch.

### Successful vs Unsuccessful

This pools all `Short/LongMaxAx1/4/6` values together across both S/L branches and axes 1/4/6, then splits only by success.

| sample | n | mean | median | p95 | max | testId at max | branch | axis at max | MaxAx1 | MaxAx4 | MaxAx6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 1695 | 0.160830 | 0.008881 | 0.639557 | 11.9959 | 316 | L | Ax4 | 0.024757 | 11.9959 | 11.6809 |
| found unsuccessful | 465 | 3.0928 | 0.657104 | 16.6834 | 85.6181 | 161 | L | Ax4 | 0.009193 | 85.6181 | 85.2788 |

### Max Examples

| outcome | testId | branch | MaxAx1 | MaxAx4 | MaxAx6 | max axis | row max | FinestStep | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| successful | 316 | L | 0.024757 | 11.9959 | 11.6809 | Ax4 | 11.9959 | 0.003125 | empty |
| successful | 434 | L | 0.028545 | 11.0434 | 10.7876 | Ax4 | 11.0434 | 0.006250 | empty |
| successful | 287 | L | 0.022423 | 8.6919 | 8.4885 | Ax4 | 8.6919 | 0.004395 | empty |
| successful | 525 | L | 0.033604 | 6.8241 | 6.6256 | Ax4 | 6.8241 | 0.006250 | empty |
| successful | 175 | L | 0.011242 | 4.7720 | 5.0789 | Ax6 | 5.0789 | 0.009375 | empty |
| successful | 427 | L | 0.014969 | 4.5541 | 4.7494 | Ax6 | 4.7494 | 0.012500 | empty |
| successful | 31 | L | 0.018732 | 4.5194 | 4.2582 | Ax4 | 4.5194 | 0.050000 | empty |
| successful | 184 | L | 0.015182 | 3.9456 | 3.7734 | Ax4 | 3.9456 | 0.012500 | empty |
| successful | 8 | L | 0.024288 | 3.7401 | 3.5335 | Ax4 | 3.7401 | 0.012500 | empty |
| successful | 451 | L | 0.011536 | 3.4204 | 3.7357 | Ax6 | 3.7357 | 0.012500 | empty |
| found unsuccessful | 161 | L | 0.009193 | 85.6181 | 85.2788 | Ax4 | 85.6181 | 0.000391 | empty |
| found unsuccessful | 346 | L | 0.016975 | 50.7844 | 50.9636 | Ax6 | 50.9636 | 0.003125 | empty |
| found unsuccessful | 164 | L | 0.887413 | 46.8546 | 47.2030 | Ax6 | 47.2030 | 0.200000 | empty |
| found unsuccessful | 431 | L | 0.008194 | 34.8368 | 34.5010 | Ax4 | 34.8368 | 0.001563 | empty |
| found unsuccessful | 152 | L | 0.018524 | 32.7478 | 33.0315 | Ax6 | 33.0315 | 0.003125 | empty |
| found unsuccessful | 78 | L | 0.023506 | 30.8242 | 31.0312 | Ax6 | 31.0312 | 0.001222 | empty |
| found unsuccessful | 140 | L | 0.035143 | 25.4349 | 25.2440 | Ax4 | 25.4349 | 0.001563 | empty |
| found unsuccessful | 375 | L | 0.014420 | 22.1131 | 21.7927 | Ax4 | 22.1131 | 0.001563 | empty |
| found unsuccessful | 245 | L | 0.034424 | 19.2015 | 19.5111 | Ax6 | 19.5111 | 0.012500 | empty |
| found unsuccessful | 515 | S | 0.002869 | 19.4721 | 19.4618 | Ax4 | 19.4721 | 0.003125 | empty |

## Legacy Jump Comparison

Correlations are computed only where the current Control and legacy Lift jointtargets match within tolerance.

### Legacy Jump Statistics

| sample | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| S legacy MaxAx1 | 500 | 0.004693 | 0.001720 | 0.011917 | 0.463399 |
| S legacy WinAx1 | 500 | 0.046397 | 0.017139 | 0.118774 | 4.4108 |
| S legacy Win2Ax1 | 500 | 0.425169 | 0.171001 | 1.1783 | 39.3017 |
| S legacy MaxAx4 | 500 | 0.142406 | 0.013075 | 0.244614 | 19.4721 |
| S legacy WinAx4 | 500 | 1.1670 | 0.130265 | 2.2758 | 120.805 |
| S legacy Win2Ax4 | 500 | 5.1166 | 1.2724 | 18.6439 | 173.878 |
| S legacy MaxAx6 | 500 | 0.141811 | 0.013626 | 0.238525 | 19.4618 |
| S legacy WinAx6 | 500 | 1.1615 | 0.135833 | 2.2149 | 120.702 |
| S legacy Win2Ax6 | 500 | 5.0884 | 1.3238 | 18.7213 | 172.849 |
| L legacy MaxAx1 | 207 | 0.042288 | 0.021898 | 0.092970 | 1.6513 |
| L legacy WinAx1 | 207 | 0.421832 | 0.218953 | 0.929462 | 16.3585 |
| L legacy Win2Ax1 | 207 | 3.5679 | 2.1599 | 9.0911 | 64.4863 |
| L legacy MaxAx4 | 207 | 3.3507 | 1.0437 | 12.0951 | 85.6181 |
| L legacy WinAx4 | 207 | 20.4586 | 9.7587 | 77.8997 | 171.274 |
| L legacy Win2Ax4 | 207 | 79.5065 | 71.1015 | 165.628 | 196.227 |
| L legacy MaxAx6 | 207 | 3.3534 | 0.988586 | 12.3145 | 85.2788 |
| L legacy WinAx6 | 207 | 20.4858 | 9.4962 | 80.4297 | 167.881 |
| L legacy Win2Ax6 | 207 | 79.3141 | 71.1763 | 160.416 | 186.425 |

### Control vs Legacy Correlation

| branch | axis | matching targets | Control/Max | Control/Win | Control/Win2 |
| --- | --- | --- | --- | --- | --- |
| S | 1 | 500 | 0.921238 | 0.930524 | 0.986379 |
| S | 4 | 500 | 0.998262 | 0.981381 | 0.798654 |
| S | 6 | 500 | 0.998315 | 0.981454 | 0.796122 |
| L | 1 | 207 | 0.999528 | 0.999488 | 0.919396 |
| L | 4 | 207 | 0.918346 | 0.746537 | 0.430313 |
| L | 6 | 207 | 0.917802 | 0.742504 | 0.396735 |

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 1394
- Groups with row count != 200: 11
- Groups with dangling unpaired row: 0
- Ratio pairs checked: 57197
- Ratio pair/order issues: 48167
- Mean PathDist: 0.484476
- Max PathDist: 136.099
- Mean Rotdist: 0.128379
- Max Rotdist: 179.977

### PathL Distance By Ratio Source

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| PathDist measured from PathRatio rows | 57197 | 0.069581 | 0.040243 | 0.245386 | 0.694410 |
| PathDist measured from RotRatio rows | 57197 | 0.899372 | 0.154352 | 0.366857 | 136.099 |
| Rotdist measured from PathRatio rows | 57197 | 0.137550 | 0.000000 | 0.468136 | 179.977 |
| Rotdist measured from RotRatio rows | 57197 | 0.119208 | 0.000000 | 0.111906 | 178.705 |

### PathL Sample Group Issues

| testId | confId | branch | rows | expected |
| --- | --- | --- | --- | --- |
| 4 | 3 | L | 88 | 200 |
| 30 | 5 | L | 32 | 200 |
| 55 | 5 | L | 96 | 200 |
| 66 | 4 | L | 98 | 200 |
| 69 | 5 | L | 98 | 200 |
| 131 | 5 | L | 98 | 200 |
| 164 | 5 | L | 92 | 200 |
| 177 | 3 | L | 98 | 200 |
| 311 | 9 | L | 98 | 200 |
| 365 | 1 | L | 98 | 200 |
| 458 | 5 | L | 98 | 200 |

### PathL Ratio Difference Statistics

| metric | n | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- |
| abs(RatioPath - ExpectedRatio) | 57197 | 0.007931 | 0.009280 | 0.009885 | 0.017407 |
| abs(RatioRot - ExpectedRatio) | 57197 | 0.015286 | 0.008397 | 0.009364 | 0.990000 |
| abs(RatioPath - RatioRot) | 57197 | 0.009395 | 0.000894 | 0.002490 | 0.999887 |

### Shortest PathLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-ExpectedRatio) n | abs(RatioPath-ExpectedRatio) min | abs(RatioPath-ExpectedRatio) mean | abs(RatioPath-ExpectedRatio) median | abs(RatioPath-ExpectedRatio) p95 | abs(RatioPath-ExpectedRatio) max | abs(RatioRot-ExpectedRatio) n | abs(RatioRot-ExpectedRatio) min | abs(RatioRot-ExpectedRatio) mean | abs(RatioRot-ExpectedRatio) median | abs(RatioRot-ExpectedRatio) p95 | abs(RatioRot-ExpectedRatio) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 116 | 2 | S | 15.2211 | 11.7731 | 100 | 0.008966 | 0.008984 | 0.008984 | 0.008994 | 0.009002 | 100 | 0.008980 | 0.008982 | 0.008982 | 0.008983 | 0.008983 |
| 116 | 1 | L | 15.2211 | 348.227 | 100 | 0.000000 | 0.007124 | 0.006894 | 0.015519 | 0.017407 | 100 | 0.000000 | 0.000001 | 0.000001 | 0.000001 | 0.000001 |
| 354 | 4 | S | 18.0008 | 12.0908 | 100 | 0.009333 | 0.009381 | 0.009380 | 0.009433 | 0.009447 | 100 | 0.008714 | 0.008717 | 0.008716 | 0.008727 | 0.008735 |
| 444 | 5 | S | 19.2297 | 11.8144 | 100 | 0.009741 | 0.009859 | 0.009858 | 0.009953 | 0.009969 | 100 | 0.008885 | 0.008894 | 0.008894 | 0.008902 | 0.008902 |
| 95 | 8 | S | 21.9336 | 11.1232 | 100 | 0.009623 | 0.009776 | 0.009771 | 0.009919 | 0.009932 | 100 | 0.009065 | 0.009068 | 0.009068 | 0.009070 | 0.009071 |
| 60 | 4 | S | 21.9337 | 11.1232 | 100 | 0.006274 | 0.006807 | 0.006604 | 0.008175 | 0.008181 | 100 | 0.007815 | 0.007934 | 0.007852 | 0.008373 | 0.008376 |
| 509 | 5 | S | 23.4940 | 9.1037 | 100 | 0.009377 | 0.009447 | 0.009450 | 0.009500 | 0.009511 | 100 | 0.009010 | 0.009032 | 0.009030 | 0.009057 | 0.009061 |
| 488 | 1 | S | 28.5782 | 12.9221 | 100 | 0.009658 | 0.009703 | 0.009704 | 0.009742 | 0.009749 | 100 | 0.008726 | 0.008729 | 0.008729 | 0.008731 | 0.008733 |
| 53 | 5 | S | 30.5712 | 6.6649 | 100 | 0.009114 | 0.009427 | 0.009652 | 0.009660 | 0.009663 | 100 | 0.008392 | 0.008677 | 0.008883 | 0.008902 | 0.008903 |
| 131 | 5 | L | 31.0892 | 2.5583 | 49 | 0.000499 | 0.008179 | 0.009559 | 0.009685 | 0.009740 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |

### Shortest RotLength Ratio Behavior

| testId | confId | branch | PathLength | RotLength | abs(RatioPath-ExpectedRatio) n | abs(RatioPath-ExpectedRatio) min | abs(RatioPath-ExpectedRatio) mean | abs(RatioPath-ExpectedRatio) median | abs(RatioPath-ExpectedRatio) p95 | abs(RatioPath-ExpectedRatio) max | abs(RatioRot-ExpectedRatio) n | abs(RatioRot-ExpectedRatio) min | abs(RatioRot-ExpectedRatio) mean | abs(RatioRot-ExpectedRatio) median | abs(RatioRot-ExpectedRatio) p95 | abs(RatioRot-ExpectedRatio) max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 55 | 5 | L | 31.1259 | 2.5427 | 48 | 0.002702 | 0.008792 | 0.009294 | 0.011816 | 0.013115 | 48 | 0.520000 | 0.755000 | 0.755000 | 0.970000 | 0.990000 |
| 55 | 5 | S | 31.1259 | 2.5427 | 100 | 0.008153 | 0.008856 | 0.009052 | 0.009202 | 0.009222 | 100 | 0.005862 | 0.006682 | 0.006908 | 0.007117 | 0.007124 |
| 131 | 5 | L | 31.0892 | 2.5583 | 49 | 0.000499 | 0.008179 | 0.009559 | 0.009685 | 0.009740 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 131 | 5 | S | 31.0892 | 2.5583 | 100 | 0.009554 | 0.009561 | 0.009562 | 0.009568 | 0.009571 | 100 | 0.008515 | 0.008529 | 0.008529 | 0.008539 | 0.008541 |
| 66 | 4 | L | 93.4164 | 2.5583 | 49 | 0.000466 | 0.008403 | 0.009809 | 0.009846 | 0.009848 | 49 | 0.009884 | 0.729998 | 0.740000 | 0.960000 | 0.980000 |
| 66 | 4 | S | 93.4164 | 2.5583 | 100 | 0.009686 | 0.009698 | 0.009698 | 0.009708 | 0.009710 | 100 | 0.007625 | 0.007665 | 0.007662 | 0.007696 | 0.008082 |
| 69 | 5 | L | 136.639 | 2.5583 | 49 | 0.000026 | 0.005248 | 0.007953 | 0.009279 | 0.009285 | 49 | 0.510000 | 0.750000 | 0.750000 | 0.970000 | 0.990000 |
| 69 | 5 | S | 136.639 | 2.5583 | 100 | 0.008725 | 0.008727 | 0.008727 | 0.008730 | 0.008731 | 100 | 0.009164 | 0.009192 | 0.009193 | 0.009209 | 0.009215 |
| 76 | 5 | L | 81.0969 | 2.5896 | 100 | 0.000430 | 0.007985 | 0.009277 | 0.009285 | 0.009288 | 100 | 0.000000 | 0.495000 | 0.495000 | 0.940000 | 0.990000 |
| 76 | 5 | S | 81.0969 | 2.5896 | 100 | 0.009278 | 0.009283 | 0.009283 | 0.009287 | 0.009289 | 100 | 0.007437 | 0.007525 | 0.007523 | 0.007606 | 0.007612 |

### PathL Ratio Issue Counts

| problem | count |
| --- | --- |
| RatioPath differs from sample | 47899 |
| RatioRot differs from sample | 47547 |
| pair ratios differ | 813 |
| RatioRot not increasing | 684 |
| RatioPath not increasing | 2 |
| RatioPath outside 0..1 | 0 |
| odd row is not PathRatio | 0 |
| RatioRot outside 0..1 | 0 |

### PathL Ratio Issue Examples

| problem | testId | confId | branch | PathLength | RotLength | pair | ExpectedRatio | previous RatioPath | RatioPath | RatioRot | odd row mode | even row mode | odd PathDist | even Rotdist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RatioPath not increasing | 451 | 5 | S | 121.670 | 8.6482 | 10 | 0.100000 | 0.090821 | 0.089323 | 0.093234 | PathRatio | RotRatio | 0.261351 | 0.000000 |
| RatioPath not increasing | 474 | 2 | S | 86.9392 | 7.2301 | 18 | 0.180000 | 0.170484 | 0.169653 | 0.173077 | PathRatio | RotRatio | 0.399044 | 0.000000 |

### PathL Anomaly Statistics

| condition | rows | % rows | PathDist median | PathDist p95 | PathDist max | Rotdist median | Rotdist p95 | Rotdist max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any anomaly | 1922 | 1.6802 | 0.216672 | 93.2830 | 136.099 | 2.7048 | 20.9994 | 179.977 |
| CfxOK != TRUE | 0 | 0.000000 | n/a | n/a | n/a | n/a | n/a | n/a |
| FoundBranch mismatch | 1394 | 1.2186 | 0.541842 | 99.6212 | 136.099 | 3.5379 | 30.2540 | 179.977 |
| PathDist > 1.0000 mm | 695 | 0.607549 | 62.3422 | 107.691 | 136.099 | 4.1682 | 32.2754 | 178.705 |
| Rotdist > 1.0000 deg | 1676 | 1.4651 | 0.257740 | 96.4003 | 136.099 | 3.1639 | 24.2620 | 179.977 |

### PathL Anomaly Reason Combinations

| conditions | rows | % rows |
| --- | --- | --- |
| FoundBranch mismatch + PathDist > 1.0000 mm + Rotdist > 1.0000 deg | 656 | 0.573457 |
| Rotdist > 1.0000 deg | 527 | 0.460688 |
| FoundBranch mismatch + Rotdist > 1.0000 deg | 492 | 0.430092 |
| FoundBranch mismatch | 208 | 0.181828 |
| FoundBranch mismatch + PathDist > 1.0000 mm | 38 | 0.033219 |
| PathDist > 1.0000 mm + Rotdist > 1.0000 deg | 1 | 0.000874 |

### Worst PathDist By Test

| testId | max PathDist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 69 | 136.099 | 136.639 | 2.5583 | 0.200000 |
| 270 | 117.951 | 118.702 | 6.3840 | 0.200000 |
| 443 | 114.564 | 114.941 | 3.0558 | 0.200000 |
| 164 | 111.395 | 111.784 | 3.0925 | 0.200000 |
| 458 | 109.912 | 111.004 | 2.9688 | 0.200000 |
| 177 | 107.136 | 107.298 | 3.4991 | 0.200000 |
| 4 | 92.6810 | 92.9810 | 3.4991 | 0.200000 |
| 66 | 92.3073 | 93.4164 | 2.5583 | 0.200000 |
| 311 | 88.8281 | 89.1340 | 2.9688 | 0.200000 |
| 76 | 80.8283 | 81.0969 | 2.5894 | 0.200000 |

### Worst Rotdist By Test

| testId | max Rotdist | PathLength | RotLength | FinestStep |
| --- | --- | --- | --- | --- |
| 76 | 179.977 | 81.0969 | 2.5896 | 0.200000 |
| 443 | 179.977 | 114.941 | 3.0561 | 0.200000 |
| 177 | 76.4697 | 107.298 | 3.4991 | 0.200000 |
| 365 | 69.9136 | 58.9587 | 3.1124 | 0.200000 |
| 30 | 67.7121 | 67.0113 | 12.0380 | 0.200000 |
| 311 | 67.3507 | 89.1340 | 2.9688 | 0.200000 |
| 458 | 67.3506 | 111.004 | 2.9688 | 0.200000 |
| 131 | 59.6167 | 31.0892 | 2.5583 | 0.200000 |
| 69 | 59.6165 | 136.639 | 2.5583 | 0.200000 |
| 66 | 59.6164 | 93.4164 | 2.5583 | 0.200000 |

## Suggested Next Investigations

- Treat joint target, XOR, and selected branch mismatches in `success.csv` as primary blockers.
- Use the unsuccessful branch jump statistics to visualize where the current adaptive checker starts rejecting branches.
- Use the legacy jump correlations to compare constant 1/1000 sampling against the adaptive implementation.
