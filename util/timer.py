#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from time import perf_counter
from datetime import datetime as dt


def get_time(fmt='%y%m%d-%H%M%S'):
    return dt.now().strftime(fmt)


def get_now():
    return perf_counter()


def timer(pattern=None):
    def _timer(func):
        def _wrapper(*args, **kwargs):
            st = perf_counter()
            out = func(*args, **kwargs)
            msg = '>> Total time; '
            if (now := perf_counter() - st) < 1:
                msg += f'{now * 1000:7.3f}; ms'
            elif now < 180:
                msg += f'{now:7.3f}; s'
            elif now < 180 * 60:
                msg += f'{now / 60:6.2f}; min ({int(now)} s)'
            else:
                msg += f'{now / 3600:6.2f}; h ({int(now)} s)'

            msg += f' [{pattern}]'
            print(msg)
            return now * 1000, out

        return _wrapper

    return _timer
