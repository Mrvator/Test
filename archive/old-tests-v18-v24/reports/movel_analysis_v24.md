# ABB MoveL Analysis v24

## Header Resume

- Tests: 254
- Successful runs: 278
- PathLength min/max: 0.192316..1.5806 mm
- RotLength min/max: 25.1184..169.306 deg
- Highest FinestStep in all test data: 0.001000 (FinestStepS/L, n=508)
- Successful runs where C_rax differs from CalcC_rax by > 1.0000 deg on any axis: 0
- Successful runs where C_rax differs from PathL_rax by > 1.0000 deg on any axis: 0
- Successful runs where ControlMatchShort XOR ControlMatchLong is false: 0
- Successful runs where MatchesShort XOR MatchesLong is false: 8

## Legacy XOR Violations

| testId | confId | MatchesShort | MatchesLong |
| --- | --- | --- | --- |
| 23 | 2 | False | False |
| 25 | 5 | False | False |
| 35 | 5 | False | False |
| 54 | 5 | False | False |
| 56 | 5 | False | False |
| 59 | 8 | False | False |
| 208 | 8 | False | False |
| 248 | 5 | False | False |

## Control XOR Violations

None.

## Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 68 |
| L | none | 4 |
| S | S | 202 |
| S | none | 4 |

## Table 1 - Successful vs No Success Branch Counts

| outcome | Short | Long |
| --- | --- | --- |
| Successful | 206 | 72 |
| No success.csv record | 17 | 5 |

## Table 2 - Aggregated Jump Summary

Legacy max-jump statistics are reported only for successful branches where the corresponding `MatchesShort` or `MatchesLong` value is true.


### Short branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 4.2909 | 250 | 5 | S | Ax4 | 4.2909 | 41.0303 | 150.059 |
| Successful | MaxWin | 41.0303 | 250 | 5 | S | Ax4 | 4.2909 | 41.0303 | 150.059 |
| Successful | MaxWin2 | 150.059 | 250 | 5 | S | Ax4 | 4.2909 | 41.0303 | 150.059 |

### Long branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 4.8898 | 89 | 6 | L | Ax6 | 4.8898 | 23.0201 | 41.4453 |
| Successful | MaxWin | 36.4247 | 15 | 4 | L | Ax4 | 3.7620 | 36.4247 | 151.183 |
| Successful | MaxWin2 | 151.183 | 15 | 4 | L | Ax4 | 3.7620 | 36.4247 | 151.183 |

## Table 3 - Minimum FinestStep

| outcome | Short | Long |
| --- | --- | --- |
| Successful | 0.001000 | 0.001000 |
| No success.csv record | 0.001000 | 0.000500 |

## Successful MaxAx < MaxWin < MaxWin2 Violations


### Short

- Violations: 0

None.

### Long

- Violations: 0

None.

## XY Graphs

- Legacy MaxAx: `reports/movel_xy_maxax_v24.svg`
- Legacy MaxWin2: `reports/movel_xy_maxwin2_v24.svg`

Each SVG has two panels: Successful Short and Successful Long. A branch is included only when the corresponding `MatchesShort` or `MatchesLong` value is true. Long panels plot `360 - RotLength`.

## PathL Ratio Analysis

- PathL pairing check: OK, 278 testId/confId groups, 2 rows per group, 0 row count issues, 0 pair issues.

### Ratio Precision

| metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| PathRatio error | 278 | 0.326198 | 0.918338 | 0.981345 | 0.990000 | 0.990000 |
| RotRatio error | 278 | 0.989999 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |

### Distance Precision

| metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| PathDist from PathRatio rows | 278 | 0.008359 | 0.216843 | 0.220832 | 0.398695 | 0.530304 |
| PathDist from RotRatio rows | 278 | 0.000000 | 0.000098 | 0.000074 | 0.000280 | 0.000863 |
| RotDist from PathRatio rows | 278 | 0.000000 | 9.0620 | 0.949321 | 47.3175 | 125.021 |
| RotDist from RotRatio rows | 278 | 0.000000 | 0.008795 | 0.000000 | 0.055953 | 0.055953 |

### PathLength Bucket Precision

| bucket | metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <1 | PathRatio error | 143 | 0.326198 | 0.893143 | 0.958327 | 0.990000 | 0.990000 |
| <1 | RotRatio error | 143 | 0.989999 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |
| <1 | PathDist from PathRatio rows | 143 | 0.008359 | 0.218179 | 0.220680 | 0.398695 | 0.530304 |
| <1 | PathDist from RotRatio rows | 143 | 0.000000 | 0.000100 | 0.000078 | 0.000273 | 0.000518 |
| <1 | RotDist from PathRatio rows | 143 | 0.000000 | 11.8676 | 2.5836 | 53.5597 | 125.021 |
| <1 | RotDist from RotRatio rows | 143 | 0.000000 | 0.009494 | 0.000000 | 0.055953 | 0.055953 |
| <10 | PathRatio error | 135 | 0.722452 | 0.945026 | 0.990000 | 0.990000 | 0.990000 |
| <10 | RotRatio error | 135 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |
| <10 | PathDist from PathRatio rows | 135 | 0.016445 | 0.215427 | 0.220984 | 0.389405 | 0.448291 |
| <10 | PathDist from RotRatio rows | 135 | 0.000000 | 0.000095 | 0.000071 | 0.000280 | 0.000863 |
| <10 | RotDist from PathRatio rows | 135 | 0.000000 | 6.0901 | 0.055953 | 26.4638 | 67.2538 |
| <10 | RotDist from RotRatio rows | 135 | 0.000000 | 0.008055 | 0.000000 | 0.039565 | 0.055953 |
| <100 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <100 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <100 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <100 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <100 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <100 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=100 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| >=100 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| >=100 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=100 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=100 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=100 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |

### RotLength Bucket Precision

| bucket | metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <1 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <1 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <1 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <1 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <1 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <1 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <10 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <10 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <10 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <10 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <10 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <10 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <90 | PathRatio error | 102 | 0.326198 | 0.911194 | 0.976938 | 0.990000 | 0.990000 |
| <90 | RotRatio error | 102 | 0.989999 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |
| <90 | PathDist from PathRatio rows | 102 | 0.018300 | 0.231291 | 0.224266 | 0.439862 | 0.515804 |
| <90 | PathDist from RotRatio rows | 102 | 0.000000 | 0.000098 | 0.000066 | 0.000345 | 0.000518 |
| <90 | RotDist from PathRatio rows | 102 | 0.000000 | 5.1553 | 0.965126 | 21.8816 | 47.5364 |
| <90 | RotDist from RotRatio rows | 102 | 0.000000 | 0.009631 | 0.000000 | 0.039565 | 0.055953 |
| <180 | PathRatio error | 104 | 0.439774 | 0.925754 | 0.990000 | 0.990000 | 0.990000 |
| <180 | RotRatio error | 104 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |
| <180 | PathDist from PathRatio rows | 104 | 0.008359 | 0.219835 | 0.229768 | 0.357546 | 0.505652 |
| <180 | PathDist from RotRatio rows | 104 | 0.000000 | 0.000099 | 0.000076 | 0.000280 | 0.000863 |
| <180 | RotDist from PathRatio rows | 104 | 0.000000 | 6.8452 | 0.055953 | 27.6509 | 65.8948 |
| <180 | RotDist from RotRatio rows | 104 | 0.000000 | 0.006940 | 0.000000 | 0.039565 | 0.055953 |
| <270 | PathRatio error | 46 | 0.443034 | 0.910415 | 0.973047 | 0.990000 | 0.990000 |
| <270 | RotRatio error | 46 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |
| <270 | PathDist from PathRatio rows | 46 | 0.028127 | 0.208183 | 0.196783 | 0.359628 | 0.530304 |
| <270 | PathDist from RotRatio rows | 46 | 0.000000 | 0.000081 | 0.000066 | 0.000273 | 0.000320 |
| <270 | RotDist from PathRatio rows | 46 | 0.000000 | 18.4079 | 4.4029 | 77.8063 | 125.021 |
| <270 | RotDist from RotRatio rows | 46 | 0.000000 | 0.010382 | 0.000000 | 0.055953 | 0.055953 |
| <350 | PathRatio error | 26 | 0.686211 | 0.930724 | 0.988387 | 0.990000 | 0.990000 |
| <350 | RotRatio error | 26 | 0.990000 | 0.990000 | 0.990000 | 0.990000 | 0.990000 |
| <350 | PathDist from PathRatio rows | 26 | 0.026255 | 0.163514 | 0.140068 | 0.349167 | 0.361921 |
| <350 | PathDist from RotRatio rows | 26 | 0.000000 | 0.000119 | 0.000085 | 0.000273 | 0.000518 |
| <350 | RotDist from PathRatio rows | 26 | 0.000000 | 16.7202 | 0.529216 | 75.8908 | 83.5869 |
| <350 | RotDist from RotRatio rows | 26 | 0.000000 | 0.010130 | 0.000000 | 0.055953 | 0.055953 |
| <359 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <359 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <359 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <359 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <359 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <359 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
