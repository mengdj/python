#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
from proc.util import AppProcData


class RTMP(AppProcData):
    """尝试rtmp协议解析"""
    _handshake = False

    def find(self, data):
        """校验数据并完成初始化，成功返回self，链式调用"""
        print(len(data))
        return None
