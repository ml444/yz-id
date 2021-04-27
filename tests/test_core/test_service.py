#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
import unittest
from yzid.core.service import IdService

compose_list = [
    ("version", 1),
    ("type", 1),
    ("method", 2),
    ("duration", 30),
    ("sequence", 20),
    ("machine", 10)
]
time_epoch = 1610351662
mode_type = 1


class TestService(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.idsvc = IdService(
            structure=compose_list,
            time_epoch=time_epoch,
            time_unit=1 if mode_type == 1 else 10 ** 3,  # 秒级和毫秒级的选择
            time_name="duration",
            sequence_name="sequence"
        )

    def test_validate_epoch(self):

        epoch0 = 1610351662.123
        with self.assertRaises(ValueError) as e:
            self.idsvc._validate_epoch(epoch0, time_unit=1)
        self.assertEqual(e.exception.args[0],
                         "The param of <class 'float'> need int type.")

        epoch0 = 610351662
        with self.assertRaises(ValueError) as e:
            self.idsvc._validate_epoch(epoch0, time_unit=1)
        self.assertEqual(e.exception.args[0],
                         f"The length of the {epoch0} is wrong.")

        epoch0 = 1610351662
        with self.assertRaises(ValueError) as e:
            self.idsvc._validate_epoch(epoch0, time_unit=123)
        self.assertEqual(e.exception.args[0],
                         "The value of this parameter is less than zero "
                         "or not 10 to the power of N")

        epoch = 1610351662
        result = self.idsvc._validate_epoch(epoch, time_unit=1)
        self.assertEqual(result, epoch)

        epoch = 1610351662
        result = self.idsvc._validate_epoch(epoch, time_unit=10)
        self.assertEqual(result, epoch*10)

        epoch = 1610351662
        result = self.idsvc._validate_epoch(epoch, time_unit=100)
        self.assertEqual(result, epoch * 100)

        epoch = 1610351662
        result = self.idsvc._validate_epoch(epoch, time_unit=1000)
        self.assertEqual(result, epoch * 1000)

        epoch1 = 1610351662001
        result = self.idsvc._validate_epoch(epoch1, time_unit=1000)
        self.assertEqual(result, epoch1)

        epoch1 = 1610351662001
        result = self.idsvc._validate_epoch(epoch1, time_unit=100)
        self.assertEqual(result, int(epoch1/10))

        epoch1 = 1610351662001
        result = self.idsvc._validate_epoch(epoch1, time_unit=1)
        self.assertEqual(result, int(epoch1 / 1000))



