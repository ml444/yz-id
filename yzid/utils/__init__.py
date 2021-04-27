#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-12-2
@desc: ...
"""


def check_platform_64bit():
    import platform
    b, _ = platform.architecture()
    return True if b == '64bit' else False

    # import sys
    # return True if sys.maxsize > 2**32 else False