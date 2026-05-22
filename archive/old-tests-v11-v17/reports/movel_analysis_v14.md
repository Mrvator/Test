# ABB MoveL Analysis v14

## Summary

- Tests: 14
- Tests with success rows: 6
- Success rows: 9
- Tests missing success rows: 8
- PathL diagnostic rows: 1800
- PathL groups by test/conf/branch: 9
- Joint tolerance: 0.01 deg
- Path distance warning: 1.0 mm
- Rotation distance warning: 1.0 deg

## Success Coverage

| missing testId |
| --- |
| 2 |
| 3 |
| 4 |
| 7 |
| 8 |
| 9 |
| 12 |
| 14 |

## Joint Target Consistency

- C/CalcC mismatches: 0
- C/PathL mismatches: 1
- CalcC/PathL mismatches: 1
- Worst valid delta: test 11, C vs CalcC, axis 1, 0.001700 deg

| testId | confId | comparison | max abs deg | axis | control branch |
| --- | --- | --- | --- | --- | --- |
| 6 | 3 | C vs PathL | n/a | n/a | none |
| 6 | 3 | CalcC vs PathL | n/a | n/a | none |

## Branch Matching

- Control branch counts: S=6, L=2, none=1
- Legacy/control flag differences: 2
- Selected control target mismatches: 0

### Legacy vs Control Differences

| testId | confId | MatchesShort | MatchesLong | ControlMatchShort | ControlMatchLong |
| --- | --- | --- | --- | --- | --- |
| 6 | 2 | True | False | True | True |
| 6 | 3 | False | True | False | False |

### Control Target Mismatches

None.

## PathL Diagnostics

- Rows with CfxOK != TRUE: 0
- Rows with FoundBranch mismatch: 200
- Mean PathDist: 50.6759
- Max PathDist: 1821.040
- Mean Rotdist: 10.4086
- Max Rotdist: 179.973

### PathL Anomalies

| testId | confId | branch | found | CfxOK | PathDist | Rotdist |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 2 | L | S | TRUE | 0.237230 | 3.5883 |
| 6 | 2 | L | S | TRUE | 1821.040 | 34.7562 |
| 6 | 2 | L | S | TRUE | 0.227008 | 7.1892 |
| 6 | 2 | L | S | TRUE | 1802.640 | 38.0414 |
| 6 | 2 | L | S | TRUE | 0.278364 | 10.7805 |
| 6 | 2 | L | S | TRUE | 1784.280 | 41.3274 |
| 6 | 2 | L | S | TRUE | 0.266434 | 14.3827 |
| 6 | 2 | L | S | TRUE | 1765.880 | 44.6126 |
| 6 | 2 | L | S | TRUE | 0.255718 | 17.9845 |
| 6 | 2 | L | S | TRUE | 1747.480 | 47.8978 |
| 6 | 2 | L | S | TRUE | 0.240124 | 21.5860 |
| 6 | 2 | L | S | TRUE | 1729.070 | 51.1828 |
| 6 | 2 | L | S | TRUE | 0.225381 | 25.1876 |
| 6 | 2 | L | S | TRUE | 1710.670 | 54.4679 |
| 6 | 2 | L | S | TRUE | 0.212959 | 28.7893 |
| 6 | 2 | L | S | TRUE | 1692.270 | 57.7530 |
| 6 | 2 | L | S | TRUE | 0.200133 | 32.3910 |
| 6 | 2 | L | S | TRUE | 1673.870 | 61.0382 |
| 6 | 2 | L | S | TRUE | 0.215895 | 35.9878 |
| 6 | 2 | L | S | TRUE | 1655.490 | 64.3237 |
| 6 | 2 | L | S | TRUE | 0.199861 | 39.5900 |
| 6 | 2 | L | S | TRUE | 1637.090 | 67.6088 |
| 6 | 2 | L | S | TRUE | 0.189337 | 43.1908 |
| 6 | 2 | L | S | TRUE | 1618.690 | 70.8940 |
| 6 | 2 | L | S | TRUE | 0.161107 | 46.7934 |
| 6 | 2 | L | S | TRUE | 1600.280 | 74.1790 |
| 6 | 2 | L | S | TRUE | 0.194866 | 50.3891 |
| 6 | 2 | L | S | TRUE | 1581.900 | 77.4647 |
| 6 | 2 | L | S | TRUE | 0.167347 | 53.9917 |
| 6 | 2 | L | S | TRUE | 1563.500 | 80.7497 |
| 6 | 2 | L | S | TRUE | 0.148006 | 57.5939 |
| 6 | 2 | L | S | TRUE | 1545.100 | 84.0349 |
| 6 | 2 | L | S | TRUE | 0.180060 | 61.1890 |
| 6 | 2 | L | S | TRUE | 1526.710 | 87.3204 |
| 6 | 2 | L | S | TRUE | 0.159408 | 64.7914 |
| 6 | 2 | L | S | TRUE | 1508.310 | 90.6055 |
| 6 | 2 | L | S | TRUE | 0.142692 | 68.3933 |
| 6 | 2 | L | S | TRUE | 1489.920 | 93.8908 |
| 6 | 2 | L | S | TRUE | 0.177130 | 71.9875 |
| 6 | 2 | L | S | TRUE | 1471.530 | 97.1763 |
... 160 more omitted by report limit.

### Worst PathDist By Test

| testId | max PathDist |
| --- | --- |
| 6 | 1821.040 |
| 11 | 0.541499 |
| 1 | 0.517893 |
| 13 | 0.487414 |
| 10 | 0.442825 |
| 5 | 0.442606 |

### Worst Rotdist By Test

| testId | max Rotdist |
| --- | --- |
| 6 | 179.973 |
| 11 | 0.181308 |
| 1 | 0.104678 |
| 5 | 0.055953 |
| 10 | 0.055953 |
| 13 | 0.055953 |

## Suggested Next Investigations

- Inspect missing success rows first; these are failed or unrecorded MoveL executions.
- For joint mismatches, compare the reported axis against RAPID configuration changes and quaternion branch choice.
- For PathL anomalies, inspect the same `testId/confId/branch` in the raw PathL rows and verify branch interpolation state.
