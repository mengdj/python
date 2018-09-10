#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
import unittest
import pcap
from proc.rtmp import RTMP
from proc.tcp import TCP


class PacketTest(unittest.TestCase):
    def test_parse(self):
        p = pcap.Pcap()
        ret = p.parse("data/1.pcap")
        print("共加载%d个数据包" % ret)
        if ret > 0:
            for i in p.packets:
                mac = i.data
                # print(i.head)
                # print("目标mac=%s 源mac=%s" % (mac.dst, mac.src))
                ip = mac.data
                if ip is not None:
                    ti = ip.data
                    if ti is not None:
                        print(mac)
                        print(i.head)
                        print(ip)
                        if ti.__class__.__name__ == "TCP":
                            rp = ti.find(RTMP())
                        elif ti.__class__.__name__ == "UDP":
                            pass
                        print(ti)
                print("")

            print()

if __name__ == "__main__":
    unittest.main()
