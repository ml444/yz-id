#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@desc: ...
"""
from yzid.core.populate import Populator


class SyncPopulator(Populator):
    """"""
    def populate(self, id_meta):
        super()._populate(id_meta)
