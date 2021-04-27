#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
import abc
from .meta import IdMeta


class IdServiceBase(metaclass=abc.ABCMeta):
    """
    ID生成器的接口抽象基类
    """
    @abc.abstractmethod
    def generate_id(self):
        pass

    @abc.abstractmethod
    def explain_id(self, id_int: int):
        pass

    @abc.abstractmethod
    def make_id(self, sequence: int, time_stamp: int):
        pass

    @abc.abstractmethod
    def translate_time(self, time_duration: int):
        """"""


class PopulatorBase(metaclass=abc.ABCMeta):
    """
    填充器，对自增的sequence进行相关操作
    """
    last_td = -1
    sequence = 0

    @abc.abstractmethod
    def populate(self, im: IdMeta):
        """填充操作"""

    @classmethod
    def reset(cls):
        cls.sequence = 0
        cls.last_td = -1


class ConvertorBase(metaclass=abc.ABCMeta):
    """
    ID的长整型合成与拆解成实例的转换接口基类
    """
    @abc.abstractmethod
    def generate(self, im: IdMeta) -> int:
        """把ID实例转换为一个长整型的ID"""
        pass

    @abc.abstractmethod
    def explain(self, long_id: int, im: IdMeta) -> dict:
        """拆解长整型的ID"""
        pass