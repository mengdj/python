#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"


class OnlyId(object):
    """四元祖存储唯一元素"""
    __src_ip = None
    __dst_ip = None
    __src_port = None
    __dst_port = None
    __ins = None

    def __init__(self):
        pass

    def __str__(self):
        return ("%d:%d:%d:%d %d|%d:%d:%d:%d %d" % (
            self.__src_ip[0], self.__src_ip[1], self.__src_ip[2], self.__src_ip[3], self.__src_port,
            self.__dst_ip[0], self.__dst_ip[1], self.__dst_ip[2], self.__dst_ip[3], self.__dst_port,
        ))

    def init(self, src_ip, dst_ip, src_port, dst_port):
        self.__src_ip = src_ip
        self.__dst_ip = dst_ip
        self.__src_port = src_port
        self.__dst_port = dst_port

    def get_only_id(self):
        return self.__str__()

    @staticmethod
    def build(src_ip, dst_ip, src_port, dst_port):
        if OnlyId.__ins is None:
            OnlyId.__ins = OnlyId()
        OnlyId.__ins.init(src_ip, dst_ip, src_port, dst_port)
        return OnlyId.__ins.get_only_id()

    @staticmethod
    def reversal(only_id):
        assert only_id != ""
        tmp = only_id.split("|")
        return ("%s|%s" % (tmp[1], tmp[0]))


class TCP_Build(object):
    """通过4元祖重组tcp数据"""
    __v_dict = {}
    __fn = None

    def bind(self, fn):
        self.__fn = fn

    def write(self, tcp):
        """将tcp包写入到二维链表中（保持数据从小到大）"""
        _vd = self.__v_dict
        _ip = tcp.upper
        only_id = OnlyId.build(_ip.src, _ip.dst, tcp.src, tcp.dst)
        # build_repeat_seq用于记录重复seq
        if hasattr(tcp, "build_repeat_seq") is False:
            setattr(tcp, "build_repeat_seq", 1)
        if only_id in _vd:
            _vd_items = _vd.get(only_id)
            """[1 3 5 7] 10 => [1 3 5 7 10]"""
            vi = 0
            find = False
            for v in _vd_items:
                if tcp.seq < v.seq:
                    # 小于插前面
                    _vd_items.insert(vi, tcp)
                    find = True
                    break
                elif tcp.seq == v.seq:
                    # 相等时插后面
                    v.build_repeat_seq += 1
                    _vd_items.insert(vi + v.build_repeat_seq, tcp)
                    find = True
                    break
                vi += 1
            if find is False:
                _vd_items.append(tcp)
            _vd[only_id] = _vd_items
        else:
            _vd[only_id] = []
            _vd[only_id].append(tcp)
        self.__v_dict = _vd

    def read(self):
        pass

    def show(self):
        """DEBUG"""
        dc = lc = 0
        for dk, dv in self.__v_dict.items():
            print(dk)
            dc += 1
            for lv in dv:
                print(lv)
                print(lv.build_repeat_seq)
                lc += 1
            print("")
        print("dc:%d lc:%d" % (dc, lc))
