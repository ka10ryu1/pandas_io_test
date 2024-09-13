#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name
import argparse
from pandas import set_option, get_option
from pathlib import Path


from file_io import pd_read_pqt

print(1, get_option('display.max_rows'))
set_option('display.max_rows', 500)
print(2, get_option('display.max_rows'))


def df_len(df):
    return len(df.index)


def command():
    parser = argparse.ArgumentParser(description='PQT形式のファイルを可視化する')
    parser.add_argument(
        'pqt',
        type=Path,
        nargs='+',
        metavar='PATH',
        help='PQTファイルのパス',
    )
    parser.add_argument(
        '-s',
        '--save_dir',
        type=Path,
        default='out',
        metavar='PATH',
        help='解析結果の保存ディレクトリ',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='printfデバッグを実行するフラグ',
    )
    return parser.parse_args()


def main(args):
    for path in args.pqt:
        df = pd_read_pqt(path)[1]
        if df_len(df) >= 1000:
            print(df[:500])
        elif df_len(df) >= 200:
            print(df[:200])
        else:
            print(df)

    return 0


if __name__ == '__main__':
    exit(main(command()))
