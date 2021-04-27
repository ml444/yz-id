#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@desc:
    ID类型分为最大峰值和最小粒度
    【最大峰值】：
    | 版本 | 类型 | 生成方式 | 秒级时间 | 序列号 | 机器ID |
    | 63   | 62  | 60-61  | 59-30   | 29-10 | 0-9   |

    【最小粒度】：
    | 版本 | 类型 | 生成方式 | 秒级时间 | 序列号 | 机器ID |
    | 63   | 62  | 60-61  | 59-20   | 19-10 | 0-9   |


"""
from enum import Enum

from yzid.core.service import IdService


class IdType(Enum):
    MAX_PEAK = 1            # 最大峰值
    MIN_GRANULARITY = 0     # 最小颗粒度


def get_id_service(
        time_epoch: int,
        machine_code: int,
        generate_method: int = 2,
        mode_type: int = 1,
        version: int = 0,

        populator_type: str = 'sync'
):
    """

    :param time_epoch:      时间起点
    :param machine_code:    机器序号
    :param generate_method:      (嵌入式，restful，中心分发）
    :param mode_type:       (最大峰值，最小粒度)
    :param version:
    :param populator_type:
    :return:
    """
    _type = {
        "max_peak": [
            ("machine",     (10, machine_code)),
            ("sequence",    20),
            ("duration",    30),
            ("method",      (2, generate_method)),
            ("type",        (1, 1)),
            ("version",     (1, version)),
        ],
        "min_granularity": [
            ("machine",     (10, machine_code)),
            ("sequence",    10),
            ("duration",    40),
            ("method",      (2, generate_method)),
            ("type",        (1, 0)),
            ("version",     (1, version)),
        ]
    }
    structure = _type.get("max_peak") if mode_type == 1 else _type.get("min_granularity")

    return IdService(
        structure=structure,
        time_epoch=time_epoch,
        time_unit=1 if mode_type == 1 else 10**3,  # 秒级和毫秒级的选择
        time_name="duration",
        sequence_name="sequence"
    )

