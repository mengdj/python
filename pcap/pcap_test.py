#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
import unittest

from pcap.proc.pcap import Pcap
from pcap.proc.rtmp import RTMP


def callback_rtmp(ins, msg, fr):
    print(msg)


class PcapTest(unittest.TestCase):
    """测试"""

    def test_load(self):
        _pcap = Pcap()
        _gen = _pcap.parse("/home/mengdj/work/git/python/pcap/data/1.pcap")
        for _packet in _gen:
            _mac = _packet.data
            _net = _mac.data
            _trans = _net.data
            if _trans.__class__.__name__ == "TCP":
                # 打印tcp的选项数据
                # print(_trans.option)
                _app = _trans.data
                if _app is not None:
                    if RTMP.find(_trans, callback_rtmp):
                        # 依次打印网络层、传输层头部
                        print(_mac)
                        print(_net)
                        print(_trans)


if __name__ == "__main__":
    unittest.main()
