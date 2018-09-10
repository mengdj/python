#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "mengdj@outlook.com"
import struct
import traceback
from enum import Enum, unique

"""flv文件解析，元数据解析采用amf0格式"""


@unique
class TagType(Enum):
    """标签类型"""
    FLV_TAG_AUDIO = 0x08
    FLV_TAG_VIDEO = 0x09
    FLV_TAG_SCRIPT = 0x12


@unique
class Amf0DataType(Enum):
    """脚本中的变量类型（本程序支持的元数据类型）"""
    FLV_AMF0_NUMBER = 0x00
    FLV_AMF0_BOOLEAN = 0x01
    FLV_AMF0_STRING = 0x02
    FLV_AMF0_OBJECT = 0X03
    FLV_AMF0_NULL = 0x05
    FLV_AMF0_ARRAY = 0x08
    FLV_AMF0_END_OF_OBJECT = 0x09
    FLV_AMF0_STRICT_ARRAY = 0X0a
    FLV_AMF0_DATE = 0X0b
    FLV_AMF0_LONG_STRING = 0X0c


class UnSupportFileFormat(Exception):
    pass


class UnSupportAmfValFormat(Exception):
    pass


class Tag(object):
    """flv文件头"""
    previousTagsSize = 0
    type = 0
    length = 0
    timestamp = 0
    exTimestamp = 0
    streamsId = 0
    # 原始数据
    data = []

    def parse(self):
        """请子类实现此方法来解析原始数据"""
        pass

    def __str__(self):
        """like tostring"""
        return "%s previousTagsSize:%d type:%d length:%d timestamp:%d exTimestamp:%d streamsId:%d" % (
            self.__class__, self.previousTagsSize, self.type, self.length, self.timestamp, self.exTimestamp,
            self.streamsId)

    def getBytes(self):
        """获取原始字节数据"""
        return self.data


# end of class Tag

class AudioTag(Tag):
    """音频tag"""
    format = None
    samplerate = None
    bits = 0
    sc = 0
    __flag = None
    __data = []

    def parse(self):
        data = super().getBytes()
        if len(data) != 0:
            self.__flag = data[0]
            self.__data = data[1:]
            # 前面4位为音频格式
            self.format = self.__flag >> 4
            # 5 6位是采样率 0000 0011&0010 1011= 0000 0011=3
            self.samplerate = (0x03 & self.__flag >> 2)
            # 7 位是采样长度 0 8bit 1 16bits
            self.bits = (self.__flag >> 1 & 0x01)
            # 单声道还是双声道 0单声道 1立体声
            self.sc = (self.__flag & 0x01)
        return self

    def getBytes(self):
        """获取字节数据"""
        return self.__data


# end of class AudioTag
class VideoTag(Tag):
    """视频tag"""
    frameType = None
    codec = None
    __flag = None
    __data = []

    def parse(self):
        """解析视频tag信息"""
        data = super().getBytes()
        if len(data) != 0:
            self.__flag = data[0]
            self.__data = data[1:]
            # 前4位为帧类型
            self.frameType = (self.__flag >> 4)
            # 后4位位编码类型（发现python左偏移貌似有些问题,不会自动补位，所以不能用左偏移）
            self.codec = (self.__flag & 0x0f)
        return self

    def getBytes(self):
        """获取字节数据"""
        return self.__data


# end of class VideoTag
class ScriptTag(Tag):
    """
        脚本数据也称元数据metadata，解析起来稍微有点麻烦
        amf0可以查看:
        https://wwwimages2.adobe.com/content/dam/acom/en/devnet/pdf/amf0-file-format-specification.pdf
    """
    numVal = 0
    strVal, lStrVal = "", ""
    objVal = []
    arrVal = {}
    boolVal = False
    nullVal, dateVal = None, None

    def parse(self):
        """解析脚本元meta数据"""
        data = super().getBytes()
        size = len(data)
        while size > 0:
            type = data[0]
            data, size = data[1:], size - 1
            if type == Amf0DataType.FLV_AMF0_NUMBER:
                data, size, self.numVal = self.__parse_number(data, size)
            elif type == Amf0DataType.FLV_AMF0_BOOLEAN:
                data, size, self.boolVal = self.__parse_boolean(data, size)
            elif type == Amf0DataType.FLV_AMF0_STRING:
                data, size, self.strVal = self.__parse_string(data, size)
            elif type == Amf0DataType.FLV_AMF0_NULL:
                data, size, self.nullVal = self.__parse_null(data, size)
            elif type == Amf0DataType.FLV_AMF0_OBJECT:
                data, size, self.objVal = self.__parse_object(data, size)
            elif type == Amf0DataType.FLV_AMF0_DATE:
                data, size, self.dateVal = self.__parse_date(data, size)
            elif type == Amf0DataType.FLV_AMF0_ARRAY:
                data, size, self.arrVal = self.__parse_array(data, size)
            elif type == Amf0DataType.FLV_AMF0_STRICT_ARRAY:
                data, size, self.arrVal = self.__parse_strict_array(data, size)
            elif type == Amf0DataType.FLV_AMF0_LONG_STRING:
                data, size, self.lStrVal = self.__parse_long_string(data, size)
            else:
                raise UnSupportAmfValFormat(type)
        # end of while
        assert size == 0
        return self

    def __parse_number(self, data, size):
        # 利用struct来处理double
        ret = struct.unpack('>d', data[:8])[0]
        return data[8:], size - 8, ret

    def __parse_boolean(self, data, size):
        """解析boolean值"""
        ret = False
        if int(data[0]) != 0:
            ret = True
        return data[1:], size - 1, ret

    def __parse_null(self, data, size):
        """解析null值"""
        return data[1:], size - 1, None

    def __parse_string(self, data, size):
        """解析string值(2字节的长度+N字符串)"""
        offset = bytes2int(data[:2])
        offset += 2
        ret = bytes.decode(data[2:offset])
        return data[offset:], size - offset, str(ret)

    def __parse_long_string(self, data, size):
        """解析string值(4字节的长度+N字符串)"""
        offset = bytes2int(data[:4])
        offset += 4
        ret = bytes.decode(data[4:offset])
        return data[offset:], size - offset, str(ret)

    def __parse_date(self, data, size):
        """解析data值(2字节的时区+8字节的时间戳),返回一个dict"""
        zone = struct.unpack('>d', data[0:2])[0]
        time = struct.unpack('>d', data[2:10])[0]
        return data[10:], size - 10, {"zone": zone, "time": time}

    def __parse_array(self, data, size):
        """ecma解析,实际是map数据"""
        arrLen = bytes2int(data[:4])
        arrVal = None
        data, size, arrVal = self.__parse_object(data[4:], size - 4)
        return data, size, {"len": arrLen, "val": arrVal}

    def __parse_strict_array(self, data, size):
        """strict解析array,strict数组是没有key的"""
        alen = bytes2int(data[:4])
        ret = []
        tmp = None
        data, size = data[4:], size - 4
        while size > 0:
            size -= 1
            if data[0] == Amf0DataType.FLV_AMF0_END_OF_OBJECT:
                data = data[1:]
                break
            elif data[0] == Amf0DataType.FLV_AMF0_NUMBER:
                data, size, tmp = self.__parse_number(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_BOOLEAN:
                data, size, tmp = self.__parse_boolean(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_STRING:
                data, size, tmp = self.__parse_string(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_NULL:
                data, size, tmp = self.__parse_null(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_OBJECT:
                data, size, tmp = self.__parse_object(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_DATE:
                data, size, tmp = self.__parse_date(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_ARRAY:
                data, size, tmp = self.__parse_array(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_STRICT_ARRAY:
                data, size, tmp = self.__parse_strict_array(data[1:], size)
                ret.append(tmp)
            elif data[0] == Amf0DataType.FLV_AMF0_LONG_STRING:
                data, size, tmp = self.__parse_long_string(data[1:], size)
                ret.append(tmp)
        return data, size, ret

    def __parse_object(self, data, size):
        """解析object信息，object由一组[key+value],其中value可以是object来嵌套使用"""
        ret = dict()
        while size > 0:
            if data[0] == Amf0DataType.FLV_AMF0_END_OF_OBJECT:
                data = data[1:]
                size -= 1
                break
            # 获取key的长度
            keyLen = bytes2int(data[:2])
            keyLen += 2
            keyVal = bytes.decode(data[2:keyLen])
            data, size = data[keyLen:], size - keyLen - 1
            # 判断object-value类型
            if data[0] == Amf0DataType.FLV_AMF0_NUMBER:
                data, size, ret[keyVal] = self.__parse_number(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_BOOLEAN:
                data, size, ret[keyVal] = self.__parse_boolean(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_STRING:
                data, size, ret[keyVal] = self.__parse_string(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_NULL:
                data, size, ret[keyVal] = self.__parse_null(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_OBJECT:
                data, size, ret[keyVal] = self.__parse_object(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_DATE:
                data, size, ret[keyVal] = self.__parse_date(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_ARRAY:
                data, size, ret[keyVal] = self.__parse_array(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_STRICT_ARRAY:
                data, size, ret[keyVal] = self.__parse_strict_array(data[1:], size)
            elif data[0] == Amf0DataType.FLV_AMF0_LONG_STRING:
                data, size, ret[keyVal] = self.__parse_long_string(data[1:], size)
        return data, size, ret


class OtherTag(Tag):
    """其他标签不予处理"""

    def parse(self):
        """获取字节数据,这部分暂不处理"""
        return self


def bytes2int(data):
    """字节转换为int"""
    return int.from_bytes(data, byteorder="big")


# flv文件头
class Head(object):
    signature = None
    version = None
    flag = None
    length = 0

    def __init__(self, data):
        """初始化flv文件头信息,一般占用9个字节"""
        self.signature = (data[0:3])
        self.signature = bytes.decode(self.signature)
        if self.signature != "FLV":
            raise UnSupportFileFormat("文件格式不被支持")
        self.version = data[3]
        self.flag = data[4]
        self.length = bytes2int(data[5:9])

    def has_audio(self):
        """是否有音频"""
        return self.flag & 1

    def has_video(self):
        """是否有视频"""
        return self.flag >> 2

    def len(self):
        """对于大于9个字节可能是拓展或其他"""
        return self.length


# flv文件体
class Flv(object):
    head = None
    tags = []
    previousTagSize = 0
    # 内部缓冲区
    __buffer = None

    # 加载flv文件
    def load(self, filePath, buffSize=2048):
        ret = 0
        assert filePath != ""
        try:
            with open(filePath, 'rb') as io:
                preTag = None
                while 1:
                    if self.__buffer is not None:
                        # 当缓冲区达到指定buffer时不再读取文件，先处理缓冲区
                        buffLen = len(self.__buffer)
                        if buffLen >= buffSize:
                            ctx = self.__buffer
                        else:
                            ctx = io.read(buffSize)
                            if len(ctx) != 0:
                                ctx = self.__buffer + ctx
                                # print("使用文件IO(%d)" % len(ctx))
                            else:
                                ctx = self.__buffer
                                # print("缓冲区剩余数据处理%d" % len(ctx))
                        self.__buffer = None
                    else:
                        ctx = io.read(buffSize)
                    size = len(ctx)
                    if size > 0:
                        # 处理文件头
                        if self.head is None:
                            if size >= 9:
                                self.head = Head(ctx)
                                ctx = ctx[self.head.len():]
                                size -= self.head.len()
                            else:
                                self.__buffer = ctx
                        # 处理标签数据(最后一个循环会遗留4个字节为最后一个tag的大小)
                        if size >= 4:
                            # 最后那一个previousTagsSize为4字节
                            self.previousTagSize = bytes2int(ctx[0:4])
                            if size >= 15:
                                if preTag is None:
                                    previousTagType = ctx[4]
                                    if previousTagType == TagType.FLV_TAG_AUDIO:
                                        preTag = AudioTag()
                                    elif previousTagType == TagType.FLV_TAG_VIDEO:
                                        preTag = VideoTag()
                                    elif previousTagType == TagType.FLV_TAG_SCRIPT:
                                        preTag = ScriptTag()
                                    else:
                                        preTag = OtherTag()
                                    # 处理基本信息，最后才处理数据
                                    preTag.previousTagsSize = self.previousTagSize
                                    preTag.type = previousTagType
                                    preTag.length = bytes2int(ctx[5:8])
                                    preTag.timestamp = bytes2int(ctx[8:11])
                                    preTag.exTimestamp = bytes2int(ctx[11:12])
                                    preTag.streamsId = bytes2int(ctx[12:15])
                                    size -= 15
                                    ctx = ctx[15:]
                                    if size > 0:
                                        if size >= preTag.length:
                                            preTag.data = ctx[:preTag.length]
                                            self.__buffer = ctx[preTag.length:]
                                            size -= preTag.length
                                            self.tags.append(preTag.parse())
                                            ret += 1
                                            preTag = None
                                        else:
                                            preTag.data = ctx[:size]
                                            self.__buffer = None
                                    else:
                                        self.__buffer = None
                                else:
                                    # 补充剩下的数据
                                    calcSize = preTag.length - len(preTag.data)
                                    if size >= calcSize:
                                        preTag.data = preTag.data + ctx[:calcSize]
                                        size -= calcSize
                                        if size > 0:
                                            self.__buffer = ctx[calcSize:]
                                        else:
                                            self.__buffer = None
                                        self.tags.append(preTag.parse())
                                        ret += 1
                                        preTag = None
                                    else:
                                        preTag.data = preTag.data + ctx[:calcSize]
                                        self.__buffer = None
                        else:
                            self.__buffer = ctx
                    else:
                        break
                # end while
        except Exception as e:
            print("Exception:\n%s\n" % traceback.format_exc())
        return ret

# end of class Flv