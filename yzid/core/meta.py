#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
from typing import List, Tuple


class IdMeta:
    pos_name_format = "{}_pos"
    bit_name_format = "{}_bit"

    def __init__(self, structure: List[Tuple[str, int]]):
        """
        :param structure: 64bit的整型数据的组成分布列表，从低0位开始至最高的63位
            [
                ("machine",     10),
                ("sequence",    20),
                ("timestamp",   30),
                ("method",      (2, 2)),
                ("type",        (1, 1)),
                ("version",     (1, 0)),
            ]
            | 版本 | 类型 | 生成方式 | 秒级时间 | 序列号 | 机器号 |
            | 63   | 62  | 60-61   | 59-30   | 29-10 | 0-9   |

        """
        self._processing_structure(structure)

    def _processing_structure(self, structure):
        self.names = []
        p = 0
        for k, v in structure:
            self.names.append(k)
            setattr(self, self.pos_name_format.format(k), p)

            if isinstance(v, tuple):
                if len(v) != 2:
                    raise ValueError(f"len({v}) != 2")
                p += v[0]
                setattr(self, self.bit_name_format.format(k), v[0])
                setattr(self, k, v[1])
            elif isinstance(v, int):
                p += v
                setattr(self, self.bit_name_format.format(k), v)
                setattr(self, k, 0)
            else:
                raise ValueError("The value does not meet the requirements.")

        if p != 64:
            raise ValueError("The composition of the data does not meet the "
                             "requirement that the total is equal to 64.")

    def _validate_name(self, name: str) -> bool:
        return hasattr(self, self.bit_name_format.format(name))

    def _validate_bit(self, value) -> bool:
        if not isinstance(value, int):
            return False
        return True

    def get_bit(self, name: str) -> int:
        return getattr(self, self.bit_name_format.format(name))

    def set_bit(self, name: str, value: int):
        self._validate_name(name)
        self._validate_bit(value)
        return setattr(self, self.bit_name_format.format(name), value)

    def get_mask(self, name):
        return -1 ^ -1 << self.get_bit(name)

    def get_start_pos(self, name):
        return getattr(self, self.pos_name_format.format(name))
    
    def get_attr(self, name):
        return getattr(self, name)

    def set_attr(self, name, value):
        return setattr(self, name, value)

    def id2dict(self):
        return {k: self.get_attr(k) for k in self.names}
