#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
import unittest

from proc.tcp_build import TCP_Build

import pcap


def callback_tcp():
    pass


class PacketTest(unittest.TestCase):
    def test_parse(self):
        p = pcap.Pcap()
        it = p.parse("data/1.pcap")
        tb=TCP_Build()
        for i in it:
            mac = i.data
            ip = mac.data
            if ip is not None:
                ti = ip.data
                if ti is not None:
                    """
                    print(mac)
                    print(i.head)
                    print(ip)
                    """
                    if ti.__class__.__name__ == "TCP":
                        tb.write(ti)
                    elif ti.__class__.__name__ == "UDP":
                        pass
                    #print(ti)
        tb.show()

if __name__ == "__main__":
    unittest.main()
