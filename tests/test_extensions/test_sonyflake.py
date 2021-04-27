#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
import unittest
from yzid.extras.sonyflake import get_sonyflake_service


time_epoch = 1610351662*100
expect_id = 15073483440521217


class TestSonyflake(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.idsvc = get_sonyflake_service(time_epoch=time_epoch, machine_code=1)

    def test_generate_id(self):
        _id = self.idsvc.generate_id()
        self.assertIsInstance(_id, int)
        self.assertGreaterEqual(len(str(_id)), 17)
        print(_id)

    def test_explain_id(self):
        id_dict = self.idsvc.explain_id(expect_id)
        self.assertIsInstance(id_dict, dict)
        self.assertEqual(id_dict, {'machine': 1, 'sequence': 0, 'duration': 898449626, 'version': 0})

    def test_make_id(self):
        data = {'sequence': 0, 'timestamp': 898449626 + time_epoch}
        id1 = self.idsvc.make_id(**data)
        self.assertEqual(id1, expect_id)

    def test_translate_time(self):
        timestamp = self.idsvc.translate_time(898449626)
        self.assertEqual(timestamp, 161933615826)


if __name__ == '__main__':
    unittest.main()
