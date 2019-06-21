#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "mengdj@outlook.com"

from io import StringIO
from io import BytesIO
from queue import Queue

"""
"""
class IOPool(object):
    def __init__(self, max_size=5, type=1):
        """
        :param max_size:        最大数量
        :param type:            类型 1：字符串缓冲区 2：字节缓冲区
        """
        self.queue = Queue()
        self.max_size = max_size
        self.type = type

    def get(self):
        """
        获取缓冲区
        :return:
        """
        if self.queue.qsize() < self.max_size or self.queue.empty():
            if self.type == 1:
                self.queue.put(StringIO())
            elif self.type == 2:
                self.queue.put(BytesIO())
        ins = self.queue.get()
        ins.seek(0, 0)
        ins.truncate()
        return ins

    def release(self, ins):
        """
        释放缓冲区对象
        :param ins:
        :return:
        """
        self.queue.put(ins)

    def __del__(self):
        while self.queue.empty() is False:
            self.queue.get().close()
