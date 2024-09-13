#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name
from pathlib import Path
from typing import Any
import pandas as pd

from util.terminal_color import green
from util.timer import timer


def mkdir(path: Path):
    # 親ディレクトリが存在しない場合
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    # ファイルが指定されている場合（is_file()は存在しているファイルにしか反応しない）
    elif path.suffix != '':
        pass
    # ディレクトリが指定されている場合
    elif not path.exists():
        print(f'mkdir {green(path.as_posix())}')
        path.mkdir()

    return path


@timer('pd_read_csv')
def pd_read_csv(
    read_path: Path, index_col: Any = None, encode: str = 'cp932', exp='.csv', comp: str = ''
):
    read_path = read_path.with_suffix(exp)
    print(f'load pandas data: {green(read_path.as_posix())}')
    compression = comp if comp else None
    return pd.read_csv(read_path, index_col=index_col, encoding=encode, compression=compression)


@timer('pd_read_hdf')
def pd_read_hdf(read_path: Path, index_col: Any = None, encode: str = 'cp932', exp='.hd5'):
    read_path = read_path.with_suffix(exp)
    print(f'load pandas data: {green(read_path.as_posix())}')
    return pd.read_hdf(read_path, key='data', index_col=index_col, encoding=encode)


@timer('pd_read_pqt')
def pd_read_pqt(read_path: Path, exp='.parquet'):
    read_path = read_path.with_suffix(exp)
    print(f'load pandas data: {green(read_path.as_posix())}')
    return pd.read_parquet(read_path)


@timer('pd_read_orc')
def pd_read_orc(read_path: Path, exp='.orc'):
    read_path = read_path.with_suffix(exp)
    print(f'load pandas data: {green(read_path.as_posix())}')
    return pd.read_orc(read_path)


@timer('pd_write_csv')
def pd_write_csv(df: pd.DataFrame, path: Path, exp='.csv', comp: str = ''):
    path = path.with_suffix(exp)
    compression = comp if comp else None
    df.to_csv(path, compression=compression)


@timer('pd_write_hdf')
def pd_write_hdf(df: pd.DataFrame, path: Path, exp='.hd5'):
    path = path.with_suffix(exp)
    df.astype(str).to_hdf(path, key='data', mode='w', complib=None, index=False)


@timer('pd_write_pqt')
def pd_write_pqt(df: pd.DataFrame, path: Path, comp: str = '', exp='.parquet'):
    path = path.with_suffix(exp)
    compression = comp if comp else None
    df.to_parquet(path, compression=compression, index=False)


@timer('pd_write_orc')
def pd_write_orc(df: pd.DataFrame, path: Path, exp='.orc'):
    path = path.with_suffix(exp)
    df.astype({'name': 'object'}).reset_index().to_orc(path, index=False)
