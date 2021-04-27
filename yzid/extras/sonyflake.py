#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@desc:
    【Sonyflake】：
    | 版本 | 10毫秒级时间 | 序列号 | 机器ID |
    | 63  | 62-24       | 23-16 | 15-0  |

    39 bits for time in units of 10 msec
     8 bits for a sequence number
    16 bits for a machine id
    因为最高位是标识位，为1表示为负数，所以最高位不使用。

"""
from yzid.core.service import IdService


def get_sonyflake_service(
        time_epoch: int,
        machine_code: int,
):
    return IdService(
        structure=[
            ("machine", (16, machine_code)),
            ("sequence", 8),
            ("duration", 39),
            ("version", (1, 0))
        ],
        time_epoch=time_epoch,
        time_unit=10**2,
        time_name="duration",
        sequence_name="sequence"
    )


