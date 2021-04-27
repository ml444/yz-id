#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
from .base import ConvertorBase
from .meta import IdMeta


class Convertor(ConvertorBase):
    # def __init__(self, id_meta: IdMeta):
    #     self.im = id_meta

    def generate(self, im: IdMeta) -> int:
        """"""
        result = 0
        for name in im.names:
            result |= im.get_attr(name) << im.get_start_pos(name)
        return result

    def explain(self, long_id: int, im: IdMeta) -> dict:
        for name in im.names:
            im.set_attr(
                name,
                (long_id >> im.get_start_pos(name)) & im.get_mask(name)
            )
        return im.id2dict()
