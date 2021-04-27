#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
import unittest
from yzid.extras.snowflake import get_snowflake_service

time_epoch = 1610351662 * 1000


class TestSnowflake(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.expect_id = 37700447359729664
        cls.idsvc = get_snowflake_service(time_epoch=time_epoch, machine_code=1)

    def test_generate_id(self):
        _id = self.idsvc.generate_id()
        self.assertIsInstance(_id, int)
        self.assertGreaterEqual(len(str(_id)), 17)
        print(_id)

    def test_explain_id(self):
        id_dict = self.idsvc.explain_id(self.expect_id)
        print(id_dict)
        self.assertIsInstance(id_dict, dict)
        self.assertEqual(id_dict, {'sequence': 0, 'machine': 0, 'duration': 8988487091, 'version': 0})

    def test_make_id(self):
        data = {'sequence': 0, 'timestamp': 8988487091 + time_epoch}
        id1 = self.idsvc.make_id(**data)
        print(id1)
        self.assertEqual(id1, self.expect_id)

    def test_translate_time(self):
        timestamp = self.idsvc.translate_time(8988487091)
        self.assertEqual(timestamp, 1619340149091)

