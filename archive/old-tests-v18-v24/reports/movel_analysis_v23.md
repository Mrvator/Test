# ABB MoveL Analysis v23

## Header Resume

- Tests: 545
- Successful runs: 577
- PathLength min/max: n/a..n/a mm
- RotLength min/max: n/a..n/a deg
- Highest FinestStep in all test data: 0.001000 (FinestStepS/L, n=1090)
- Successful runs where C_rax differs from CalcC_rax by > 1.0000 deg on any axis: 0
- Successful runs where C_rax differs from PathL_rax by > 1.0000 deg on any axis: 0
- Successful runs where ControlMatchShort XOR ControlMatchLong is false: 0
- Successful runs where MatchesShort XOR MatchesLong is false: 23

## Legacy XOR Violations

| testId | confId | MatchesShort | MatchesLong |
| --- | --- | --- | --- |
| 7 | 1 | False | False |
| 47 | 5 | False | False |
| 64 | 6 | False | False |
| 95 | 2 | False | False |
| 121 | 4 | False | False |
| 121 | 5 | True | True |
| 133 | 7 | False | False |
| 172 | 5 | False | False |
| 199 | 4 | False | False |
| 206 | 7 | False | False |
| 215 | 2 | False | False |
| 215 | 5 | False | False |
| 273 | 8 | False | False |
| 375 | 1 | False | False |
| 375 | 2 | False | False |
| 377 | 6 | False | False |
| 392 | 5 | False | False |
| 402 | 4 | False | False |
| 411 | 6 | False | False |
| 414 | 2 | False | False |
| 444 | 5 | False | False |
| 486 | 8 | False | False |
| 510 | 4 | False | False |

## Control XOR Violations

None.

## Legacy vs Control Branch Comparison

| control | legacy | rows |
| --- | --- | --- |
| L | L | 78 |
| L | none | 7 |
| S | S | 477 |
| S | none | 15 |

## Table 1 - Successful vs No Success Branch Counts

| outcome | Short | Long |
| --- | --- | --- |
| Successful | 492 | 85 |
| No success.csv record | 4 | 1 |

## Table 2 - Aggregated Jump Summary

Legacy max-jump statistics are reported only for successful branches where the corresponding `MatchesShort` or `MatchesLong` value is true.


### Short branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 0.184486 | 522 | 1 | S | Ax1 | 0.184486 | 1.8430 | 18.2747 |
| Successful | MaxWin | 1.8430 | 522 | 1 | S | Ax1 | 0.184486 | 1.8430 | 18.2747 |
| Successful | MaxWin2 | 18.2747 | 522 | 1 | S | Ax1 | 0.184486 | 1.8430 | 18.2747 |

### Long branches

| outcome | metric | value | testId | confId | branch | axis | row MaxAx | row MaxWin | row MaxWin2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Successful | MaxAx | 168.504 | 121 | 5 | L | Ax4 | 168.504 | 118.340 | 112.584 |
| Successful | MaxWin | 335.246 | 244 | 2 | L | Ax6 | 156.574 | 335.246 | 357.488 |
| Successful | MaxWin2 | 357.488 | 244 | 2 | L | Ax6 | 156.574 | 335.246 | 357.488 |

## Table 3 - Minimum FinestStep

| outcome | Short | Long |
| --- | --- | --- |
| Successful | 0.001000 | 0.000125 |
| No success.csv record | 0.001000 | 0.001000 |

## Successful MaxAx < MaxWin < MaxWin2 Violations


### Short

- Violations: 0

None.

### Long

- Violations: 126

| testId | branch | axis | MaxAx | MaxWin | MaxWin2 | bOK | stErr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | L | Ax1 | 2.1086 | 5.0987 | 4.2744 | True | empty |
| 10 | L | Ax1 | 2.2692 | 7.1112 | 6.9890 | True | empty |
| 10 | L | Ax6 | 13.6519 | 45.6671 | 42.4380 | True | empty |
| 14 | L | Ax1 | 3.2803 | 8.1712 | 7.3117 | True | empty |
| 14 | L | Ax4 | 26.9213 | 63.7465 | 49.7910 | True | empty |
| 15 | L | Ax1 | 1.3719 | 4.2193 | 2.6547 | True | empty |
| 22 | L | Ax1 | 3.8998 | 11.1529 | 7.1354 | True | empty |
| 22 | L | Ax4 | 27.6153 | 116.645 | 104.074 | True | empty |
| 24 | L | Ax1 | 7.8434 | 7.2687 | 6.9971 | True | empty |
| 24 | L | Ax6 | 15.8460 | 15.6808 | 15.1012 | True | empty |
| 30 | L | Ax1 | 2.0830 | 6.8239 | 5.4614 | True | empty |
| 30 | L | Ax6 | 30.2124 | 118.686 | 117.972 | True | empty |
| 32 | L | Ax1 | 3.5984 | 7.2315 | 5.5656 | True | empty |
| 32 | L | Ax6 | 41.0704 | 99.2480 | 93.6928 | True | empty |
| 35 | L | Ax1 | 1.9089 | 3.8908 | 2.8844 | True | empty |
| 35 | L | Ax4 | 32.6323 | 64.9337 | 47.4775 | True | empty |
| 45 | L | Ax1 | 2.2903 | 3.0173 | 2.9587 | True | empty |
| 45 | L | Ax4 | 45.1095 | 65.4204 | 64.2749 | True | empty |
| 49 | L | Ax1 | 4.3506 | 12.0045 | 10.5632 | True | empty |
| 54 | L | Ax1 | 3.3495 | 6.6105 | 5.4439 | True | empty |
| 54 | L | Ax4 | 42.8419 | 143.462 | 126.954 | True | empty |
| 57 | L | Ax1 | 1.0686 | 2.1882 | 1.9089 | True | empty |
| 57 | L | Ax4 | 30.2907 | 71.7000 | 69.3458 | True | empty |
| 66 | L | Ax1 | 5.2534 | 17.3976 | 14.9112 | True | empty |
| 66 | L | Ax6 | 29.7513 | 124.884 | 116.765 | True | empty |
| 70 | L | Ax1 | 0.276989 | 0.806385 | 0.776890 | True | empty |
| 70 | L | Ax4 | 8.8422 | 15.7863 | 13.1630 | True | empty |
| 80 | L | Ax1 | 1.9697 | 7.7198 | 6.6558 | True | empty |
| 96 | L | Ax1 | 4.8488 | 10.2824 | 8.8324 | True | empty |
| 96 | L | Ax6 | 30.2883 | 84.2818 | 83.7437 | True | empty |
| 97 | L | Ax1 | 1.2953 | 3.5157 | 3.3174 | True | empty |
| 100 | L | Ax1 | 1.8865 | 5.2316 | 5.1402 | True | empty |
| 100 | L | Ax6 | 30.1761 | 85.2099 | 61.8236 | True | empty |
| 104 | L | Ax1 | 3.3967 | 10.1026 | 7.6760 | True | empty |
| 109 | L | Ax1 | 1.9193 | 4.7854 | 3.6630 | True | empty |
| 109 | L | Ax4 | 24.2104 | 73.6491 | 43.5023 | True | empty |
| 121 | L | Ax1 | 1.8526 | 2.3786 | 2.3003 | True | empty |
| 121 | L | Ax4 | 168.504 | 118.340 | 112.584 | True | empty |
| 121 | L | Ax6 | 100.130 | 75.3789 | 71.4040 | True | empty |
| 124 | L | Ax1 | 2.7974 | 7.6585 | 7.0638 | True | empty |
| 132 | L | Ax1 | 2.5438 | 4.1071 | 3.7168 | True | empty |
| 132 | L | Ax4 | 36.9876 | 94.9430 | 83.7993 | True | empty |
| 146 | L | Ax1 | 1.7031 | 5.0799 | 4.9828 | True | empty |
| 146 | L | Ax4 | 32.3260 | 136.728 | 133.241 | True | empty |
| 147 | L | Ax1 | 2.0479 | 5.6287 | 5.2324 | True | empty |
| 153 | L | Ax1 | 5.0042 | 15.6383 | 14.6435 | True | empty |
| 153 | L | Ax6 | 19.5207 | 62.8838 | 52.6787 | True | empty |
| 158 | L | Ax1 | 3.0888 | 4.0977 | 3.2721 | True | empty |
| 158 | L | Ax4 | 36.5984 | 81.9663 | 51.1765 | True | empty |
| 159 | L | Ax1 | 3.9089 | 11.6206 | 11.0892 | True | empty |
| 159 | L | Ax6 | 58.7647 | 104.280 | 99.4231 | True | empty |
| 162 | L | Ax1 | 4.5498 | 8.0006 | 6.8716 | True | empty |
| 162 | L | Ax4 | 61.7711 | 132.422 | 131.423 | True | empty |
| 163 | L | Ax1 | 1.3505 | 2.9789 | 2.2052 | True | empty |
| 163 | L | Ax4 | 31.3638 | 101.776 | 95.3461 | True | empty |
| 169 | L | Ax1 | 2.9217 | 7.7399 | 6.9667 | True | empty |
| 169 | L | Ax6 | 41.1734 | 115.280 | 112.625 | True | empty |
| 170 | L | Ax1 | 2.4283 | 7.4322 | 5.4651 | True | empty |
| 170 | L | Ax6 | 33.0588 | 109.664 | 99.8228 | True | empty |
| 182 | L | Ax1 | 2.0470 | 5.9493 | 5.4902 | True | empty |
| 182 | L | Ax6 | 29.6879 | 100.441 | 100.237 | True | empty |
| 203 | L | Ax1 | 2.7670 | 9.1039 | 9.0985 | True | empty |
| 203 | L | Ax4 | 51.4684 | 119.191 | 118.184 | True | empty |
| 208 | L | Ax6 | 27.9157 | 73.0535 | 68.6447 | True | empty |
| 210 | L | Ax6 | 11.8504 | 56.1487 | 38.0165 | True | empty |
| 216 | L | Ax1 | 0.942960 | 2.9581 | 2.8716 | True | empty |
| 216 | L | Ax4 | 53.5949 | 72.9441 | 64.0837 | True | empty |
| 217 | L | Ax1 | 0.375214 | 0.853271 | 0.801559 | True | empty |
| 217 | L | Ax4 | 19.8289 | 56.6283 | 56.3234 | True | empty |
| 223 | L | Ax1 | 0.859001 | 1.4577 | 1.1809 | True | empty |
| 223 | L | Ax4 | 7.1757 | 14.7083 | 13.4286 | True | empty |
| 225 | L | Ax1 | 5.7946 | 11.1575 | 10.1459 | True | empty |
| 225 | L | Ax4 | 52.5459 | 90.2508 | 87.1509 | True | empty |
| 230 | L | Ax1 | 2.3736 | 7.1748 | 6.5166 | True | empty |
| 231 | L | Ax1 | 2.8004 | 6.2932 | 5.5475 | True | empty |
| 231 | L | Ax4 | 49.7401 | 110.268 | 103.626 | True | empty |
| 244 | L | Ax1 | 2.5554 | 2.8169 | 2.5779 | True | empty |
| 244 | L | Ax4 | 124.928 | 115.963 | 112.217 | True | empty |
| 268 | L | Ax1 | 1.5838 | 3.4273 | 3.1774 | True | empty |
| 277 | L | Ax1 | 1.4190 | 3.3668 | 2.7394 | True | empty |
| 277 | L | Ax4 | 25.1002 | 64.3870 | 49.5894 | True | empty |
| 293 | L | Ax1 | 2.0456 | 2.8764 | 2.2372 | True | empty |
| 293 | L | Ax4 | 91.2424 | 144.309 | 143.046 | True | empty |
| 302 | L | Ax1 | 3.9035 | 11.2181 | 10.1265 | True | empty |
| 309 | L | Ax6 | 10.9961 | 22.4189 | 21.9055 | True | empty |
| 314 | L | Ax1 | 15.6044 | 48.6852 | 44.4139 | True | empty |
| 315 | L | Ax1 | 1.9759 | 5.8098 | 4.5395 | True | empty |
| 315 | L | Ax4 | 27.7189 | 90.1157 | 81.7037 | True | empty |
| 326 | L | Ax1 | 2.6434 | 6.3360 | 4.4021 | True | empty |
| 329 | L | Ax1 | 1.9211 | 2.9690 | 2.4220 | True | empty |
| 329 | L | Ax4 | 30.9047 | 105.667 | 73.0400 | True | empty |
| 336 | L | Ax1 | 2.0892 | 3.0295 | 2.8433 | True | empty |
| 336 | L | Ax4 | 60.7628 | 129.669 | 120.141 | True | empty |
| 355 | L | Ax1 | 2.0128 | 6.6495 | 5.2600 | True | empty |
| 355 | L | Ax6 | 25.9258 | 74.7653 | 71.8796 | True | empty |
| 359 | L | Ax1 | 1.9786 | 3.7479 | 2.8470 | True | empty |
| 359 | L | Ax4 | 26.4647 | 101.412 | 96.8762 | True | empty |
| 361 | L | Ax1 | 4.1726 | 6.6778 | 6.2558 | True | empty |
| 361 | L | Ax6 | 51.5681 | 94.5725 | 84.6391 | True | empty |
| 364 | L | Ax1 | 0.509071 | 0.914223 | 0.699471 | True | empty |
| 364 | L | Ax4 | 6.3797 | 12.5464 | 9.0775 | True | empty |
| 368 | L | Ax1 | 1.6248 | 4.7415 | 4.2836 | True | empty |
| 391 | L | Ax1 | 1.3603 | 3.8278 | 3.5782 | True | empty |
| 391 | L | Ax4 | 16.0532 | 40.8093 | 33.5530 | True | empty |
| 395 | L | Ax1 | 2.2231 | 8.4215 | 5.9718 | True | empty |
| 404 | L | Ax1 | 2.0589 | 7.3577 | 6.5353 | True | empty |
| 410 | L | Ax1 | 2.9069 | 4.1206 | 3.9320 | True | empty |
| 410 | L | Ax4 | 45.0624 | 105.717 | 101.418 | True | empty |
| 439 | L | Ax1 | 1.4188 | 4.1639 | 3.5754 | True | empty |
| 441 | L | Ax1 | 2.6790 | 7.5152 | 6.7674 | True | empty |
| 454 | L | Ax1 | 2.7025 | 7.3850 | 5.7811 | True | empty |
| 454 | L | Ax4 | 31.7643 | 131.761 | 131.450 | True | empty |
| 487 | L | Ax1 | 0.991909 | 2.8094 | 2.6130 | True | empty |
| 487 | L | Ax4 | 40.9496 | 132.713 | 93.2417 | True | empty |
| 489 | L | Ax6 | 23.3861 | 114.908 | 84.7826 | True | empty |
| 491 | L | Ax1 | 7.4403 | 22.1102 | 20.3239 | True | empty |
| 498 | L | Ax1 | 1.8619 | 6.2427 | 4.8429 | True | empty |
| 503 | L | Ax1 | 1.7567 | 3.2554 | 2.6272 | True | empty |
| 505 | L | Ax1 | 2.2025 | 2.4662 | 2.1810 | True | empty |
| 505 | L | Ax4 | 41.4690 | 101.736 | 77.9828 | True | empty |
| 511 | L | Ax1 | 3.4417 | 6.3154 | 4.7709 | True | empty |
| 511 | L | Ax4 | 39.3268 | 110.120 | 76.6190 | True | empty |
| 513 | L | Ax6 | 30.3631 | 98.3193 | 57.8537 | True | empty |
| 518 | L | Ax1 | 3.4760 | 9.0586 | 8.2663 | True | empty |
| 527 | L | Ax6 | 13.1429 | 45.1291 | 35.8198 | True | empty |
| 536 | L | Ax6 | 16.7749 | 45.3856 | 38.4155 | True | empty |

## XY Graphs

- Legacy MaxAx: `reports/movel_xy_maxax_v23.svg`
- Legacy MaxWin2: `reports/movel_xy_maxwin2_v23.svg`

Each SVG has two panels: Successful Short and Successful Long. A branch is included only when the corresponding `MatchesShort` or `MatchesLong` value is true. Long panels plot `360 - RotLength`.

## PathL Ratio Analysis

- PathL pairing check: OK, 0 testId/confId groups, row counts no groups, 0 row count issues, 0 pair issues.

### Ratio Precision

| metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |

### Distance Precision

| metric | n | min | mean | median | p95 | max |
| --- | --- | --- | --- | --- | --- | --- |
| PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |

### PathLength Bucket Precision

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
| <90 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <90 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <90 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <90 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <90 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <90 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
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
| <350 | PathRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <350 | RotRatio error | 0 | n/a | n/a | n/a | n/a | n/a |
| <350 | PathDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <350 | PathDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <350 | RotDist from PathRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
| <350 | RotDist from RotRatio rows | 0 | n/a | n/a | n/a | n/a | n/a |
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
