#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name
from pathlib import Path


def _is_linux():
    return Path.cwd().parts[0] == '/'


def red(in_str: str) -> str:
    return f'\033[31m{in_str}\033[0m' if _is_linux() else in_str


def green(in_str: str) -> str:
    return f'\033[32m{in_str}\033[0m' if _is_linux() else in_str


def blue(in_str: str) -> str:
    return f'\033[34m{in_str}\033[0m' if _is_linux() else in_str
