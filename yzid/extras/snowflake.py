#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@desc:
    【Snowflake】:
    | 版本 | 毫秒级时间 | 机器ID | 序列号 |
    | --- | --------- | ----- | ----- |
    | 63  | 62-22     | 21-12 | 11-0  |

    因为最高位是标识位，为1表示为负数，所以最高位不使用。
    41bit 保存时间戳，精确到毫秒。也就是说最大可使用的年限是69年。
    10bit 的机器位，能部属在1024台机器节点来生成ID。
    12bit 的序列号，一毫秒最大生成唯一ID的数量为4096个。
"""
from yzid.core.service import IdService


def get_snowflake_service(
        time_epoch: int,
        machine_code: int,
):
    return IdService(
        structure=[
            ("sequence", 12),
            ("machine", (10, machine_code)),
            ("duration", 41),
            ("version", (1, 0))
        ],
        time_epoch=time_epoch,
        time_unit=10**3,
        time_name="duration",
        sequence_name="sequence"
    )