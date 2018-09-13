#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from proc.util import AppProcData, BytesBuffer

RTMP_VERSION = 0x03


class RTMP(AppProcData):
    """尝试rtmp协议解析"""
    __buff = None
    __handshake = False

    def __init__(self):
        if RTMP.__buff is None:
            RTMP.__buff = BytesBuffer()

    def find(self, ins):
        """校验数据并完成初始化，成功返回self，链式调用"""
        size = len(ins)
        if size > 0:
            if ins.data[0]==0x03:
                self.__handshake=True
        return None
