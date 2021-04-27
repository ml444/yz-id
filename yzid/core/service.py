#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
from math import log10
from copy import deepcopy
from typing import List, Tuple

from .base import *
from .meta import IdMeta
from .convert import Convertor
from .populate import Populator


class IdService(IdServiceBase):
    def __init__(
            self,
            structure: List[Tuple[str, int]],
            time_epoch: int,
            time_unit: int,     # 10**3 millisecond | 10**6 Microsecond
            time_name: str,
            sequence_name: str,
            populator: PopulatorBase = None,
            convertor: ConvertorBase = None,
    ):
        self._id_meta = IdMeta(structure)
        self.time_unit = self._processing_timeunit(time_unit)
        self.time_epoch = self._processing_timestamp(time_epoch)
        self.time_name = time_name
        self.sequence_name = sequence_name
        self._converter = convertor if convertor else self._get_convertor()
        self._populator = populator if populator else self._get_populator()

    def generate_id(self) -> int:
        """生成64位长整型ID"""
        self._populator.populate(self._id_meta)
        return self._converter.generate(self._id_meta)

    def explain_id(self, long_id: int) -> dict:
        """解析长整型ID为Id的实例"""
        return self._converter.explain(long_id, self._id_meta)

    def make_id(
            self, sequence: int, timestamp: int,
    ) -> int:
        """
        手动合成ID，慎用！
        限制手动合成的ID只能为过去的时间，防止未来时间的ID重复

        :param sequence:
        :param timestamp:
        :return:
        """
        time_duration = self._timestamp2duration(timestamp)
        _im = deepcopy(self._id_meta)
        _im.set_attr(self.sequence_name, sequence)
        _im.set_attr(self.time_name, time_duration)

        long_id = self._converter.generate(_im)
        return long_id

    def translate_time(self, time_duration: int) -> int:
        """
        从时间间隔中计算出时间戳
        :param time_duration:
        :param format: "%Y-%m-%d %H:%M:%S"
        :return:
        """
        return time_duration + self.time_epoch

    def _get_populator(self) -> PopulatorBase:
        # TODO 插件模式
        return Populator(
            self.time_name, self.sequence_name,
            self.time_unit, self.time_epoch
        )

    def _get_convertor(self) -> ConvertorBase:
        # TODO 插件模式
        return Convertor()

    def _timestamp2duration(self, timestamp: int) -> int:
        """
        将时间戳转为时间间隔数值
        根据self.time_unit确定时间单位

        :param timestamp:
        :return:
        """

        _ts = self._processing_timestamp(timestamp)
        value = _ts - self.time_epoch
        if value < 0:
            raise ValueError('Timestamp is out of calculation range.')
        return int(value)

    def _processing_timeunit(self, time_unit: int):
        if time_unit < 0 or log10(time_unit) % 1 != 0:
            raise ValueError("The value of this parameter is less than zero "
                             "or not 10 to the power of N")
        return time_unit

    def _processing_timestamp(self, ts: int) -> int:
        """根据时间单位处理时间戳"""
        # 验证时间是否标准
        if not isinstance(ts, (int, float)):
            raise ValueError(
                f"The param of {type(ts)} need int or float type.")
        _ts_len = len(str(int(ts)))
        if _ts_len < 10:
            raise ValueError(f"The length of the {ts} is wrong.")

        n = _ts_len - 10
        return int(ts * (self.time_unit / 10 ** n))