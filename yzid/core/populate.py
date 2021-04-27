#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
from .base import PopulatorBase
from .meta import IdMeta


class Populator(PopulatorBase):
    def __init__(self, time_name, sequence_name: str, time_unit: int, epoch: int):
        """"""
        self.td_name = time_name
        self.seq_name = sequence_name
        if time_unit <= 0 or time_unit > 10**6:
            raise ValueError(f"0<{time_unit}<=10**6")
        self.time_unit = time_unit
        self.epoch = epoch

    def populate(self, im: IdMeta):
        return self._populate(im)

    def _populate(self, im: IdMeta):
        """
        查看当前时间是否已经到了下一个时间单位了，
        如果到了，则将序号清零。
        如果还在上一个时间单位，就对序列号进行累加。
        如果累加后越界了，就需要等待下一时间单位再产生唯一ID

        :param im:
        :return:
        """
        timeduration = generate_time(self.time_unit, self.epoch)
        validate_timestamp(self.last_td, timeduration)
        if timeduration == self.last_td:
            self.sequence += 1
            self.sequence &= im.get_mask(self.seq_name)
            if self.sequence == 0:
                self.last_td = till_next_time(
                    self.last_td, self.time_unit, self.epoch)
        else:
            self.last_td = timeduration
            self.sequence = 0

        im.set_attr(self.seq_name, self.sequence)
        im.set_attr(self.td_name, self.last_td)


import time


def generate_time(timeunit: int, epoch: int):
    """
    EPOCH 以微秒为单位
    根据传入的时间单位，计算time_duration

    :param timeunit: 10**6(微秒)
    :return:
    """

    return int(time.time()*timeunit - epoch)
    # return int((time.time()*1e6 - epoch) / (1e6/timeunit))


def validate_timestamp(last_timestamp, timestamp):
    if timestamp < last_timestamp:
        raise ValueError(
            "Clock moved backwards.  "
            "Refusing to generate id for %d second/milisecond.",
            (last_timestamp-timestamp)
        )


def till_next_time(last_timestamp, timeunit: int, epoch: int):
    timestamp = generate_time(timeunit, epoch)
    while timestamp <= last_timestamp:
        timestamp = generate_time(timeunit, epoch)
    return timestamp
