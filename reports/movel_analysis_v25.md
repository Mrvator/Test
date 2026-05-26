# ABB MoveL Analysis v25

## Header Resume

- Tests: 250
- Successful runs: 248
- PathLength min/max: 0.219385..1.5596 mm
- RotLength min/max: 2.1926..15.2704 deg
- Highest FinestStep in all test data: 0.001000 (FinestStepS/L, n=500)
- Successful runs where C_rax differs from CalcC_rax by > 1.0000 deg on any axis: 0
- Successful runs where C_rax differs from PathL_rax by > 1.0000 deg on any axis: 0
- Successful runs where ControlMatchShort XOR ControlMatchLong is false: 0
- Successful runs where MatchesShort XOR MatchesLong is false: 10

## Legacy XOR Violations

| testId | confId | MatchesShort | MatchesLong |
| --- | --- | --- | --- |
| 32 | 4 | False | False |
| 36 | 5 | False | False |
| 46 | 5 | False | False |
| 126 | 4 | False | False |
| 151 | 5 | False | False |
| 160 | 8 | False | False |
| 162 | 5 | False | False |
| 176 | 1 | False | False |
| 188 | 1 | False | False |
| 220 | 7 | False | False |

## Control XOR Violations

None.

## Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 20 |
| L | none | 4 |
| S | S | 218 |
| S | none | 6 |

## Table 1 - Successful vs No Success Branch Counts

| outcome | Short | Long |
| --- | --- | --- |
| Successful | 224 | 24 |
| No success.csv record | 6 | 2 |

## Table 2 - Aggregated Jump Summary

Legacy max-jump statistics are reported only for successful branches where the corresponding `MatchesShort` or `MatchesLong` value is true.


### Short branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 0.397247 | 45 | 4 | S | Ax6 | 0.397247 | 3.9705 | 38.2299 |
| Successful | MaxWin | 3.9705 | 45 | 4 | S | Ax6 | 0.397247 | 3.9705 | 38.2299 |
| Successful | MaxWin2 | 38.2299 | 45 | 4 | S | Ax6 | 0.397247 | 3.9705 | 38.2299 |

### Long branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 5.9612 | 217 | 4 | L | Ax4 | 5.9612 | 55.2947 | 169.358 |
| Successful | MaxWin | 55.2947 | 217 | 4 | L | Ax4 | 5.9612 | 55.2947 | 169.358 |
| Successful | MaxWin2 | 169.358 | 217 | 4 | L | Ax4 | 5.9612 | 55.2947 | 169.358 |

## Table 3 - Minimum FinestStep

| outcome | Short | Long |
| --- | --- | --- |
| Successful | 0.001000 | 0.001000 |
| No success.csv record | 0.001000 | 0.001000 |

## Successful MaxAx < MaxWin < MaxWin2 Violations


### Short

- Violations: 0

None.

### Long

- Violations: 0

None.

## XY Graphs

- Legacy MaxAx: `reports/movel_xy_maxax_v25.svg`
- Legacy MaxWin2: `reports/movel_xy_maxwin2_v25.svg`

Each SVG has two panels: Successful Short and Successful Long. A branch is included only when the corresponding `MatchesShort` or `MatchesLong` value is true. Long panels plot `360 - RotLength`.

## PathL Ratio Analysis

- PathL pairing check: OK, 248 testId/confId groups, 200 rows per group, 0 row count issues, 0 pair issues.

### Ratio Precision

| metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| PathRatio error | 24800 | 0.000000 | 0.025072 | 0.011432 | 0.097883 | 0.520000 |
| RotRatio error | 24800 | 0.000000 | 0.013090 | 0.009991 | 0.010056 | 0.990000 |

### Distance Precision

| metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| PathDist from PathRatio rows | 24800 | 0.000000 | 0.034044 | 0.012792 | 0.181367 | 0.680475 |
| PathDist from RotRatio rows | 24800 | 0.000278 | 0.046817 | 0.016705 | 0.244945 | 1.5456 |
| RotDist from PathRatio rows | 24800 | 0.000000 | 3.8483 | 0.079129 | 25.6639 | 178.301 |
| RotDist from RotRatio rows | 24800 | 0.000000 | 0.052939 | 0.000000 | 0.039565 | 15.2707 |

### PathLength Bucket Precision

| bucket | metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <1 | PathRatio error | 13300 | 0.000000 | 0.030227 | 0.011119 | 0.132788 | 0.520000 |
| <1 | RotRatio error | 13300 | 0.000000 | 0.013128 | 0.009993 | 0.010062 | 0.990000 |
| <1 | PathDist from PathRatio rows | 13300 | 0.000000 | 0.037904 | 0.012935 | 0.205174 | 0.680475 |
| <1 | PathDist from RotRatio rows | 13300 | 0.000278 | 0.050722 | 0.017450 | 0.273462 | 0.991484 |
| <1 | RotDist from PathRatio rows | 13300 | 0.000000 | 4.8055 | 0.096913 | 36.9669 | 178.301 |
| <1 | RotDist from RotRatio rows | 13300 | 0.000000 | 0.055514 | 0.000000 | 0.039565 | 15.2707 |
| <10 | PathRatio error | 11500 | 0.000000 | 0.019109 | 0.011593 | 0.063055 | 0.390000 |
| <10 | RotRatio error | 11500 | 0.000001 | 0.013047 | 0.009989 | 0.010051 | 0.990000 |
| <10 | PathDist from PathRatio rows | 11500 | 0.000722 | 0.029580 | 0.012519 | 0.154182 | 0.477518 |
| <10 | PathDist from RotRatio rows | 11500 | 0.000984 | 0.042301 | 0.015695 | 0.207548 | 1.5456 |
| <10 | RotDist from PathRatio rows | 11500 | 0.000000 | 2.7413 | 0.068528 | 19.0606 | 135.875 |
| <10 | RotDist from RotRatio rows | 11500 | 0.000000 | 0.049962 | 0.000000 | 0.055953 | 15.2450 |
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
| <10 | PathRatio error | 11700 | 0.000000 | 0.014021 | 0.010000 | 0.027348 | 0.492707 |
| <10 | RotRatio error | 11700 | 0.000001 | 0.014983 | 0.009998 | 0.010068 | 0.990000 |
| <10 | PathDist from PathRatio rows | 11700 | 0.000000 | 0.012391 | 0.008523 | 0.031967 | 0.194441 |
| <10 | PathDist from RotRatio rows | 11700 | 0.000278 | 0.021053 | 0.011637 | 0.045903 | 1.5456 |
| <10 | RotDist from PathRatio rows | 11700 | 0.000000 | 0.081106 | 0.039565 | 0.197823 | 4.6852 |
| <10 | RotDist from RotRatio rows | 11700 | 0.000000 | 0.044922 | 0.000000 | 0.039565 | 9.9010 |
| <90 | PathRatio error | 10700 | 0.000000 | 0.017950 | 0.011456 | 0.071001 | 0.141939 |
| <90 | RotRatio error | 10700 | 0.000000 | 0.013943 | 0.009994 | 0.010041 | 0.990000 |
| <90 | PathDist from PathRatio rows | 10700 | 0.000722 | 0.022168 | 0.014307 | 0.065021 | 0.290587 |
| <90 | PathDist from RotRatio rows | 10700 | 0.000984 | 0.031718 | 0.020656 | 0.084267 | 1.4797 |
| <90 | RotDist from PathRatio rows | 10700 | 0.000000 | 0.181892 | 0.111906 | 0.704430 | 1.4666 |
| <90 | RotDist from RotRatio rows | 10700 | 0.000000 | 0.065591 | 0.000000 | 0.039565 | 15.2707 |
| <180 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <180 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <180 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <180 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <180 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <180 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <270 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <270 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <270 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <270 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <270 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <270 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <350 | PathRatio error | 1900 | 0.000000 | 0.122124 | 0.091326 | 0.330000 | 0.520000 |
| <350 | RotRatio error | 1900 | 0.000000 | 0.000058 | 0.000055 | 0.000110 | 0.000156 |
| <350 | PathDist from PathRatio rows | 1900 | 0.003221 | 0.197066 | 0.184654 | 0.396347 | 0.680475 |
| <350 | PathDist from RotRatio rows | 1900 | 0.014856 | 0.248459 | 0.236871 | 0.453515 | 0.690732 |
| <350 | RotDist from PathRatio rows | 1900 | 0.000000 | 42.4869 | 31.7182 | 115.239 | 178.301 |
| <350 | RotDist from RotRatio rows | 1900 | 0.000000 | 0.036626 | 0.000000 | 0.148037 | 0.209357 |
| <359 | PathRatio error | 500 | 0.000000 | 0.067270 | 0.038475 | 0.250000 | 0.325736 |
| <359 | RotRatio error | 500 | 0.000008 | 0.000067 | 0.000068 | 0.000114 | 0.000152 |
| <359 | PathDist from PathRatio rows | 500 | 0.001535 | 0.175390 | 0.170812 | 0.323633 | 0.458571 |
| <359 | PathDist from RotRatio rows | 500 | 0.012440 | 0.206550 | 0.211450 | 0.374656 | 0.463128 |
| <359 | RotDist from PathRatio rows | 500 | 0.000000 | 23.6356 | 13.5944 | 87.4831 | 114.046 |
| <359 | RotDist from RotRatio rows | 500 | 0.000000 | 0.031781 | 0.000000 | 0.137056 | 0.148037 |
| >=359 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| >=359 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
