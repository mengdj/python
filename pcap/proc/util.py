#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from io import BytesIO


class ProcData(object):
    def __init__(self):
        pass

    @property
    def data(self):
        """返回上层数据，未处理分片"""
        pass

    @property
    def raw_data(self):
        """返回上层数据，已处理完分片，源数据"""
        pass

    def find(self, data):
        """适配实现的应用层协议"""
        pass


class AppProcData(object):
    def __init__(self):
        pass

    def find(self, data):
        """校验数据并完成初始化，成功返回self，链式调用"""
        pass


class BytesOrder(object):
    """大小端排序工具类"""
    order = "big"

    @staticmethod
    def bytes2int(data, ord=""):
        if ord == "":
            ord = BytesOrder.order
        return int.from_bytes(data, ord)


class BytesBuffer(BytesIO):
    """封装BytesIO,增加重置"""
    __length = 0
    __count = 0

    def __len__(self):
        """获取长度，使用切片而不复制数据,同时增加计算缓存"""
        if self.__length == 0:
            self.__length = len(self.getbuffer())
        return self.__length

    def clear(self):
        """清理缓存区然后重置索引,seek必须调用"""
        self.truncate(0)
        self.seek(0)
        self.__length = 0
        self.__count = 0

    def write(self, *args, **kwargs):
        self.__length = 0
        self.__count += 1
        return super().write(*args, **kwargs)

    def writelines(self, *args, **kwargs):
        self.__length = 0
        self.__count += 1
        return super().writelines(*args, **kwargs)

    def count(self):
        return self.__count
