#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
import copy
import struct
import sys
from io import BytesIO

"""兼容性处理"""
try:
    from itertools import izip

    compat_izip = izip
except ImportError:
    compat_izip = zip

if sys.version_info < (3,):
    def iteritems(d, **kw):
        return d.iteritems(**kw)
else:
    def iteritems(d, **kw):
        return iter(d.items(**kw))


class _Meta(type):
    """struct元类，定制new"""

    def __new__(cls, clsname, clsbases, clsdict):
        t = type.__new__(cls, clsname, clsbases, clsdict)
        st = getattr(t, '__hdr__', None)
        if st is not None:
            # 限制导出
            clsdict['__slots__'] = [x[0] for x in st] + ['data']
            t = type.__new__(cls, clsname, clsbases, clsdict)
            # 变量
            t.__hdr_fields__ = [x[0] for x in st]
            # 格式（默认用了大端排序）
            t.__hdr_fmt__ = getattr(t, '__byte_order__', '>') + ''.join([x[1] for x in st])
            # 结构体
            t.__hdr_len__ = struct.calcsize(t.__hdr_fmt__)
            # 默认值
            t.__hdr_defaults__ = dict(compat_izip(
                t.__hdr_fields__, [x[2] for x in st]))
        return t


class _CData(_Meta("Temp", (object,), {})):
    def __init__(self, *args, **kwargs):
        self.data = b''
        if args:
            try:
                self.unpack(args[0])
            except struct.error:
                if len(args[0]) < self.__hdr_len__:
                    raise Exception
                raise Exception('invalid %s: %r' %
                                (self.__class__.__name__, args[0]))
        else:
            # 子类属性赋值
            for k in self.__hdr_fields__:
                setattr(self, k, copy.copy(self.__hdr_defaults__[k]))
            # 转换成迭代器
            for k, v in iteritems(kwargs):
                setattr(self, k, v)

    def __len__(self):
        return self.__hdr_len__ + len(self.data)

    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except AttributeError:
            raise KeyError

    def __repr__(self):
        l = []
        for field_name, _, _ in getattr(self, '__hdr__', []):
            field_value = getattr(self, field_name)
            if field_value != self.__hdr_defaults__[field_name]:
                if field_name[0] != '_':
                    l.append('%s=%r' % (field_name, field_value))  # (1)
                else:
                    for prop_name in field_name.split('_'):  # (2)
                        if isinstance(getattr(self.__class__, prop_name, None), property):
                            l.append('%s=%r' % (prop_name, getattr(self, prop_name)))
        l.extend(
            ['%s=%r' % (attr_name, attr_value)
             for attr_name, attr_value in iteritems(self.__dict__)
             if attr_name[0] != '_'  # exclude _private attributes
             and attr_name != self.data.__class__.__name__.lower()])  # exclude fields like ip.udp
        if self.data:
            l.append('data=%r' % self.data)
        return '%s(%s)' % (self.__class__.__name__, ', '.join(l))

    def __str__(self):
        return str(self.__bytes__())

    def __bytes__(self):
        return self.pack_hdr() + bytes(self.data)

    def pack_hdr(self):
        """Return packed header string."""
        try:
            return struct.pack(self.__hdr_fmt__,
                               *[getattr(self, k) for k in self.__hdr_fields__])
        except struct.error:
            vals = []
            for k in self.__hdr_fields__:
                v = getattr(self, k)
                if isinstance(v, tuple):
                    vals.extend(v)
                else:
                    vals.append(v)
            try:
                return struct.pack(self.__hdr_fmt__, *vals)
            except struct.error as e:
                raise Exception(str(e))

    def pack(self):
        """Return packed header + self.data string."""
        return bytes(self)

    def unpack(self, buf):
        for k, v in compat_izip(self.__hdr_fields__,
                                struct.unpack(self.__hdr_fmt__, buf[:self.__hdr_len__])):
            setattr(self, k, v)
        self.data = buf[self.__hdr_len__:]


class ProcData(object):
    __upper = 0

    def __init__(self, upper=None):
        self.__upper = upper

    @property
    def data(self):
        """返回上层数据，未处理分片"""
        pass

    @property
    def upper(self):
        return self.__upper


class AppProcData(object):
    """此接口由应用层来实现"""

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
    # 写入长度缓存
    __length = 0
    # 统计写入次数
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
        return super(BytesBuffer, self).write(*args, **kwargs)

    def writelines(self, *args, **kwargs):
        self.__length = 0
        self.__count += 1
        return super(BytesBuffer, self).writelines(*args, **kwargs)

    def count(self):
        return self.__count
