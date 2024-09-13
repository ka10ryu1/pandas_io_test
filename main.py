#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name
import argparse
from pathlib import Path

import random
import string
import numpy as np
import pandas as pd

from collections import defaultdict

from file_io import mkdir
from file_io import pd_read_csv, pd_read_hdf, pd_read_orc, pd_read_pqt
from file_io import pd_write_csv, pd_write_hdf, pd_write_orc, pd_write_pqt
from util.terminal_color import red


def command():
    parser = argparse.ArgumentParser(description='pandasのDataFrame検証')
    parser.add_argument(
        '-t',
        '--astype',
        default='all_obj',
        metavar='TYPE',
        choices=('all_obj', 'default', 'use_16_32', 'use_16_32_cat'),
        help='データ型の種類 [default:%(default)s]',
    )
    parser.add_argument(
        '-c',
        '--comp',
        default='',
        metavar='COMP',
        choices=('gzip', 'snappy'),
        help='圧縮の種類 [default:未圧縮]',
    )
    parser.add_argument(
        '-n',
        '--num',
        type=int,
        default=10,
        metavar='INT',
        help='試行回数 [default:%(default)s]',
    )
    parser.add_argument(
        '-l',
        '--lines',
        type=int,
        default=500000,
        metavar='INT',
        help='DataFrameの行数（最大10,517,761行） [default:%(default)s]',
    )
    parser.add_argument(
        '--out',
        type=Path,
        default='out',
        metavar='PATH',
        help='データの保存ディレクトリ [default:%(default)s]',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='printfデバッグを実行するフラグ',
    )
    return parser.parse_args()


def dataframe_info(df: pd.DataFrame):
    return pd.concat(
        [
            df.dtypes,
            df.memory_usage(deep=True),
            df.max(numeric_only=True),
            df.min(numeric_only=True),
            df.iloc[0],
        ],
        axis=1,
        ignore_index=True,
    ).rename(
        columns={0: 'dtypes', 1: 'memory', 2: 'max', 3: 'min', 4: 'first'},
    )


def str_num_hash(num, hash_len=16):
    return [
        ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(hash_len)])
        for _ in range(num)
    ]


def num_hash(num, hash_len=3):
    return [
        int(''.join([random.choice(string.digits) for _ in range(hash_len)])) for _ in range(num)
    ]


def make_time_series(num, start='2000-01-01', end='2019-12-31', freq='min', seed=None):
    index = pd.date_range(start=start, end=end, freq=freq, name='timestamp')[:num]
    n = len(index)
    state = np.random.RandomState(seed)
    columns = {
        'name': state.choice(['Alice', 'Bob', 'Charlie'], size=n),
        'id': state.poisson(100000, size=n),
        'x': state.rand(n) * 2 - 1,
        'y': state.rand(n) * 2 - 1,
        'hash1': str_num_hash(n),
        'hash2': num_hash(n),
    }
    df = pd.DataFrame(columns, index=index, columns=columns, dtype='object')
    if df.index[-1] == end:
        df = df.iloc[:-1]

    return df


def write_all(df, path, comp):
    rslt = {}
    if not comp:
        rslt['hdf'] = pd_write_hdf(df, path)[0]
        rslt['orc'] = pd_write_orc(df, path)[0]

    if not comp or comp == 'gzip':
        rslt['csv'] = pd_write_csv(df, path, comp=comp)[0]

    rslt['pqt'] = pd_write_pqt(df, path, comp=comp)[0]
    return rslt


def read_all(path, comp):
    rslt = {}
    if not comp:
        rslt['hdf'] = pd_read_hdf(path)[0]
        rslt['orc'] = pd_read_orc(path)[0]

    if not comp or comp == 'gzip':
        rslt['csv'] = pd_read_csv(path, comp=comp)[0]

    rslt['pqt'] = pd_read_pqt(path)[0]
    return rslt


def dict_merge(input_dict_list):
    result = defaultdict(list)
    for d in input_dict_list:
        for key, value in d.items():
            result[key].append(value)

    return pd.DataFrame(dict(result)).fillna(0)


def loop_num(df, path, num, comp):
    write_list = []
    read_list = []
    for i in range(num):
        print(red(f'\n### {i:2}/{num}回目'))
        write_list.append(write_all(df, path, comp))
        read_list.append(read_all(path, comp))

    print(red('\n### write [ms]'))
    print(dict_merge(write_list).describe().round().astype(int))
    print(red('\n### read [ms]'))
    print(dict_merge(read_list).describe().round().astype(int))


def main(args):
    print(args)
    mkdir(args.out)
    df = make_time_series(args.lines)
    print(df)

    if args.astype == 'default':
        print('### default')
        df = df.astype(
            {
                'id': np.int64,
                'x': np.float64,
                'y': np.float64,
                'hash2': np.int64,
            }
        )
    elif args.astype == 'use_16_32':
        print('### use 16/32 bit')
        df = df.astype(
            {
                'id': np.int32,
                'x': np.float32,
                'y': np.float32,
                'hash2': np.int16,
            }
        )
    elif args.astype == 'use_16_32_cat':
        print('### use category')
        df = df.astype(
            {
                'id': np.int32,
                'x': np.float32,
                'y': np.float32,
                'hash2': np.int16,
                'name': 'category',
            }
        )
    else:
        print('### all object')

    print(dataframe_info(df))
    comp = f'_{args.comp}' if args.comp else ''
    loop_num(df, args.out / f'{args.astype}_{args.lines}{comp}.csv', args.num, args.comp)
    return 0


if __name__ == '__main__':
    exit(main(command()))
