#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
import unittest
from yzid.extras.anonymous import get_id_service


time_epoch = 1610351662
expect_id = 6927002444522061825


class TestSonyflake(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.idsvc = get_id_service(time_epoch=time_epoch, machine_code=1)

    def test_generate_id(self):
        _id = self.idsvc.generate_id()
        self.assertIsInstance(_id, int)
        self.assertGreaterEqual(len(str(_id)), 17)
        print(_id)

    def test_explain_id(self):
        id_dict = self.idsvc.explain_id(expect_id)
        self.assertIsInstance(id_dict, dict)
        self.assertEqual(id_dict, {'machine': 1, 'sequence': 0, 'duration': 8822807, 'method': 2, 'type': 1, 'version': 0})

    def test_make_id(self):
        data = {'sequence': 0, 'timestamp': 8822807 + time_epoch}
        id1 = self.idsvc.make_id(**data)
        self.assertEqual(id1, expect_id)

    def test_translate_time(self):
        timestamp = self.idsvc.translate_time(8822807)
        self.assertEqual(timestamp, 1619174469)


if __name__ == '__main__':
    unittest.main()




