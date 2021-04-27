#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
"""
@auth: cml
@desc: ...
"""
from threading import RLock
from yzid.core.populate import Populator


class LockPopulator(Populator):
    """"""
    lock = RLock()

    def populate(self, id_meta):
        self.lock.acquire()
        try:
            super()._populate(id_meta)
        except Exception as e:
            pass
        finally:
            self.lock.release()

