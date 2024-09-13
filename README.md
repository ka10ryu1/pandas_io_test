# pandas_io_test

pandas の CSV、Parquet、ORC などの形式の読み書き速度とファイルサイズを検証する

## 概要

- pandas で DataFrame を出力する際に使用する形式は CSV が一般的である
- しかし、CSV は大規模データになるとパフォーマンスが低下する
- Parquet を利用することで、大規模データでも高速かつコンパクトにデータの入出力が可能になる
- Parquet をはじめとした多くの形式は DataFrame の型も格納できるので便利

## インストール

```bash
python3 -m venv ENV --prompt IO
source ./ENV/bin/activate
pip install -r requirements.txt
```

## 実行手順

```bash
./main.py
```

## 結果

### `./main.py`

50万行だと、Parquetが優秀である

```bash
### write [ms]
        hdf  orc   csv  pqt
count    10   10    10   10
mean   1426  358  1863  188
std      61   37   147   14
min    1331  313  1734  171
25%    1392  322  1767  180
50%    1413  354  1776  186
75%    1472  386  1925  195
max    1533  417  2125  216

### read [ms]
       hdf  orc  csv  pqt
count   10   10   10   10
mean   337  103  652  101
std     45   16   35   19
min    287   90  607   82
25%    302   93  622   93
50%    330   97  652   95
75%    359  107  674  104
max    421  141  703  146
```

### `./main.py -l 100`

100 行程度ならサイズ、読み書き速度ともに CSV が強い

```bash
### write [ms]
       hdf  orc  csv  pqt
count   10   10   10   10
mean    11    4    1    2
std     16    3    0    1
min      5    3    1    1
25%      6    3    1    1
50%      6    3    1    1
75%      7    3    1    2
max     55   13    2    3

### read [ms]
       hdf  orc  csv  pqt
count   10   10   10   10
mean     5    2    2    3
std      1    2    0    2
min      4    1    1    2
25%      4    1    1    2
50%      5    1    1    2
75%      5    2    2    2
max      8    7    2    9
```


### 使用するデータ

| timestamp        | name    | id     | x         | y         | hash1            | hash2 |
| ---------------- | ------- | ------ | --------- | --------- | ---------------- | ----- |
| 2000/1/1 0:00:00 | Charlie | 100474 | 0.366934  | -0.909413 | raUjPi4gCUXX0007 | 365   |
| 2000/1/1 0:01:00 | Alice   | 100024 | -0.672441 | 0.002724  | 1pPsXYf3iRsQ66ze | 854   |
| 2000/1/1 0:02:00 | Bob     | 100329 | -0.899501 | -0.816123 | OB08E209i3lihQBD | 8     |
| 2000/1/1 0:03:00 | Charlie | 100192 | 0.076412  | -0.448875 | MYYaJ2xYDD9Hhhi7 | 571   |
| 2000/1/1 0:04:00 | Alice   | 99899  | -0.615352 | -0.248992 | Dye6A6mMlMTgdQOE | 132   |
| ...              | ...     | ...    | ...       | ...       | ...              |       |
| 2000/1/1 1:35:00 | Charlie | 99834  | 0.586145  | -0.840511 | dbLJPnyDVMDLJYSs | 494   |
| 2000/1/1 1:36:00 | Alice   | 100386 | 0.565667  | 0.454848  | FupIcqzCzscBdt11 | 487   |
| 2000/1/1 1:37:00 | Alice   | 99746  | 0.037006  | 0.220266  | 0uSWRbsaT2GKryQx | 171   |
| 2000/1/1 1:38:00 | Charlie | 100217 | -0.529304 | 0.078742  | tDTsqbwv3IdnF8R6 | 165   |
| 2000/1/1 1:39:00 | Alice   | 99962  | -0.106775 | 0.070502  | 19fdOejCwwRK06qO | 22    |

Parquetのデータは `./view_pqt hoge.pqt` で閲覧可能
