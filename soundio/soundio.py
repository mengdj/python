#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__ = "1.0.3"
__author__ = "mengdj@outlook.com"
import os
from ctypes import *
from enum import Enum, unique

"""
cross-platform audio input and output for real-time & consumer software
http://libsound.io
"""

"""
def method_find(act=""):
    def _wrap(func):
        def _param(*args, **kwargs):
            return func(*args,*kwargs)
        return _param
    return _wrap
"""


@unique
class SoundIoChannelId(Enum):
    SoundIoChannelIdInvalid = 0
    SoundIoChannelIdFrontLeft = 1
    SoundIoChannelIdFrontRight = 2
    SoundIoChannelIdFrontCenter = 3
    SoundIoChannelIdLfe = 4
    SoundIoChannelIdBackLeft = 5
    SoundIoChannelIdBackRight = 6
    SoundIoChannelIdFrontLeftCenter = 7
    SoundIoChannelIdFrontRightCenter = 8
    SoundIoChannelIdBackCenter = 9
    SoundIoChannelIdSideLeft = 10
    SoundIoChannelIdSideRight = 11
    SoundIoChannelIdTopCenter = 12
    SoundIoChannelIdTopFrontLeft = 13
    SoundIoChannelIdTopFrontCenter = 14
    SoundIoChannelIdTopFrontRight = 15
    SoundIoChannelIdTopBackLeft = 16
    SoundIoChannelIdTopBackCenter = 17
    SoundIoChannelIdTopBackRight = 18

    SoundIoChannelIdBackLeftCenter = 19
    SoundIoChannelIdBackRightCenter = 20
    SoundIoChannelIdFrontLeftWide = 21
    SoundIoChannelIdFrontRightWide = 22
    SoundIoChannelIdFrontLeftHigh = 23
    SoundIoChannelIdFrontCenterHigh = 24
    SoundIoChannelIdFrontRightHigh = 25
    SoundIoChannelIdTopFrontLeftCenter = 26
    SoundIoChannelIdTopFrontRightCenter = 27
    SoundIoChannelIdTopSideLeft = 28
    SoundIoChannelIdTopSideRight = 29
    SoundIoChannelIdLeftLfe = 30
    SoundIoChannelIdRightLfe = 31
    SoundIoChannelIdLfe2 = 32
    SoundIoChannelIdBottomCenter = 33
    SoundIoChannelIdBottomLeftCenter = 34
    SoundIoChannelIdBottomRightCenter = 35

    SoundIoChannelIdMsMid = 36
    SoundIoChannelIdMsSide = 37

    SoundIoChannelIdAmbisonicW = 38
    SoundIoChannelIdAmbisonicX = 39
    SoundIoChannelIdAmbisonicY = 40
    SoundIoChannelIdAmbisonicZ = 41

    SoundIoChannelIdXyX = 42
    SoundIoChannelIdXyY = 43

    SoundIoChannelIdHeadphonesLeft = 44
    SoundIoChannelIdHeadphonesRight = 45
    SoundIoChannelIdClickTrack = 46
    SoundIoChannelIdForeignLanguage = 47
    SoundIoChannelIdHearingImpaired = 48
    SoundIoChannelIdNarration = 49
    SoundIoChannelIdHaptic = 50
    SoundIoChannelIdDialogCentricMix = 51
    SoundIoChannelIdAux = 52
    SoundIoChannelIdAux0 = 53
    SoundIoChannelIdAux1 = 54
    SoundIoChannelIdAux2 = 55
    SoundIoChannelIdAux3 = 56
    SoundIoChannelIdAux4 = 57
    SoundIoChannelIdAux5 = 58
    SoundIoChannelIdAux6 = 59
    SoundIoChannelIdAux7 = 60
    SoundIoChannelIdAux8 = 70
    SoundIoChannelIdAux9 = 71
    SoundIoChannelIdAux10 = 72
    SoundIoChannelIdAux11 = 73
    SoundIoChannelIdAux12 = 74
    SoundIoChannelIdAux13 = 75
    SoundIoChannelIdAux14 = 76
    SoundIoChannelIdAux15 = 77


@unique
class SoundIoError(Enum):
    SoundIoErrorNone = 0
    SoundIoErrorNoMem = 1
    SoundIoErrorInitAudioBackend = 2
    SoundIoErrorSystemResources = 3
    SoundIoErrorOpeningDevice = 4
    SoundIoErrorNoSuchDevice = 5
    SoundIoErrorInvalid = 6
    SoundIoErrorBackendUnavailable = 7
    SoundIoErrorStreaming = 8
    SoundIoErrorIncompatibleDevice = 9
    SoundIoErrorNoSuchClient = 10
    SoundIoErrorIncompatibleBackend = 11
    SoundIoErrorBackendDisconnected = 12
    SoundIoErrorInterrupted = 13
    SoundIoErrorUnderflow = 14
    SoundIoErrorEncodingString = 15


@unique
class SoundIoFormat(Enum):
    SoundIoFormatInvalid = 0
    SoundIoFormatS8 = 1
    SoundIoFormatU8 = 2
    SoundIoFormatS16LE = 3
    SoundIoFormatS16BE = 4
    SoundIoFormatU16LE = 5
    SoundIoFormatU16BE = 6
    SoundIoFormatS24LE = 7
    SoundIoFormatS24BE = 8
    SoundIoFormatU24LE = 9
    SoundIoFormatU24BE = 10
    SoundIoFormatS32LE = 11
    SoundIoFormatS32BE = 12
    SoundIoFormatU32LE = 13
    SoundIoFormatU32BE = 14
    SoundIoFormatFloat32LE = 15
    SoundIoFormatFloat32BE = 16
    SoundIoFormatFloat64LE = 17
    SoundIoFormatFloat64BE = 18


class SoundIoSampleRateRangeStructure(Structure):
    _fields_ = [
        ("min", c_int),
        ("max", c_int)
    ]


class SoundIoStructure(Structure):
    # 结构体无法传入自己,所以采用后面的形式,全局来初始化对象
    pass


SoundIoStructure._fields_ = [
    ("userdata", c_void_p),
    ("on_devices_change", CFUNCTYPE(None, POINTER(SoundIoStructure))),
    ("on_backend_disconnect", CFUNCTYPE(None, c_void_p, c_int)),
    ("on_events_signal", CFUNCTYPE(None, c_void_p)),
    ("current_backend", c_int),
    ("app_name", c_char_p),
    ("emit_rtprio_warning", CFUNCTYPE(None)),
    ("jack_info_callback", CFUNCTYPE(None, c_char_p)),
    ("jack_error_callback", CFUNCTYPE(None, c_char_p))
]

SOUNDIO_MAX_CHANNELS = 24


class SoundIoChannelLayoutStructure(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("channel_count", c_int),
        ("channels", c_int * SOUNDIO_MAX_CHANNELS)
    ]


class SoundIoDeviceStrcuture(Structure):
    """设备信息"""
    _fields_ = [
        ("soundio", POINTER(SoundIoStructure)),
        ("id", c_char_p),
        ("name", c_char_p),
        ("aim", c_int),
        ("layouts", POINTER(SoundIoChannelLayoutStructure)),
        ("layout_count", c_int),
        ("current_layout", SoundIoChannelLayoutStructure),
        ("formats", POINTER(c_int)),
        ("format_count", c_int),
        ("current_format", c_int),
        ("sample_rates", POINTER(SoundIoSampleRateRangeStructure)),
        ("sample_rate_count", c_int),
        ("sample_rate_current", c_int),
        ("software_latency_min", c_double),
        ("software_latency_max", c_double),
        ("software_latency_current", c_double),
        ("is_raw", c_bool),
        ("ref_count", c_int),
        ("probe_error", c_int),
    ]


class SoundIoOutStreamStructure(Structure):
    """输出流结构体(内含有指针函数，用到了自己，python无法在结构体中传递自己，从上往下执行，因此写在下面)"""
    pass


# 类变量赋值，防止写在里面报错
SoundIoOutStreamStructure._fields_ = [
    ("devices", POINTER(SoundIoDeviceStrcuture)),
    ("format", c_int),
    ("sample_rate", c_int),
    ("layout", SoundIoChannelLayoutStructure),
    ("software_latency", c_double),
    ("userdata", c_void_p),
    ("write_callback", CFUNCTYPE(None, POINTER(SoundIoOutStreamStructure), c_int, c_int)),
    ("underflow_callback", CFUNCTYPE(None, POINTER(SoundIoOutStreamStructure))),
    ("error_callback", CFUNCTYPE(None, POINTER(SoundIoOutStreamStructure), c_int)),
    ("name", c_char_p),
    ("non_terminal_hint", c_bool),
    ("bytes_per_frame", c_int),
    ("bytes_per_sample", c_int),
    ("layout_error", c_int),
]


class SoundIoChannelAreaStructure(Structure):
    _fields_ = [
        ("ptr", c_char_p),
        ("step", c_int)
    ]


class SoundIoInStreamStrcuture(Structure):
    """输入流"""
    pass


SoundIoInStreamStrcuture._fields_ = [
    ("device", POINTER(SoundIoDeviceStrcuture)),
    ("format", c_int),
    ("sample_rate", c_int),
    ("layout", SoundIoChannelLayoutStructure),
    ("software_latency", c_double),
    ("userdata", c_void_p),
    ("read_callback", CFUNCTYPE(None, POINTER(SoundIoInStreamStrcuture), c_int, c_int)),
    ("overflow_callback", CFUNCTYPE(None, POINTER(SoundIoInStreamStrcuture))),
    ("error_callback", CFUNCTYPE(None, POINTER(SoundIoInStreamStrcuture), c_int)),
    ("name", c_char_p),
    ("non_terminal_hint", c_bool),
    ("bytes_per_frame", c_int),
    ("bytes_per_sample", c_int),
    ("layout_error", c_int),
]


class SoundIoRingBufferStruct(Structure):
    pass


class SoundIo(object):
    __lib = ""
    __soundio = None

    def __init__(self, lib=""):
        """
        :param lib: 动态库文件名称,windows为dll,linux为so,需要正确填入路径
        """
        if lib == "":
            os_name = os.name
            if os_name == "nt":
                lib = "libsoundio.dll"
            elif os_name == "posix":
                lib = "/usr/local/lib/libsoundio.so"
        assert lib != "", "lib can't null"
        self.__lib = cdll.LoadLibrary(lib)

    def __enter__(self):
        """实现with"""
        return self.soundio_create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """实现with"""
        self.soundio_destroy(self.__soundio)

    def soundio_version_string(self):
        """获取版本字符串"""
        _soundio_version_string = self.__lib.soundio_version_string
        _soundio_version_string.argtypes = None
        _soundio_version_string.restype = c_char_p
        return bytes.decode(_soundio_version_string())

    def soundio_version_major(self):
        _soundio_version_major = self.__lib.soundio_version_major
        _soundio_version_major.argtypes = None
        _soundio_version_major.restype = c_int
        return _soundio_version_major()

    def soundio_version_minor(self):
        _soundio_version_minor = self.__lib.soundio_version_minor
        _soundio_version_minor.argtypes = None
        _soundio_version_minor.restype = c_int
        return _soundio_version_minor()

    def soundio_version_patch(self):
        _soundio_version_patch = self.__lib.soundio_version_patch
        _soundio_version_patch.argtypes = None
        _soundio_version_patch.restype = c_int
        return _soundio_version_patch()

    def soundio_create(self):
        """
        创建1个后端，可通过此函数创建多个后端
        :return:
        """
        _soundio_create = self.__lib.soundio_create
        _soundio_create.argtypes = None
        _soundio_create.restype = POINTER(SoundIoStructure)
        self.__soundio = _soundio_create();
        return self.__soundio

    def soundio_destroy(self, sis):
        if sis is not None:
            _soundio_destroy = self.__lib.soundio_destroy
            _soundio_destroy.argtypes = [POINTER(SoundIoStructure)]
            _soundio_destroy.restype = None
            _soundio_destroy(sis)
            return True
        return False

    def soundio_connect(self, sis):
        _soundio_connect = self.__lib.soundio_connect
        _soundio_connect.argtypes = [POINTER(SoundIoStructure)]
        _soundio_connect.restype = c_int
        return _soundio_connect(sis)

    def soundio_connect_backend(self, sis, backend):
        _soundio_connect_backend = self.__lib.soundio_connect_backend
        _soundio_connect_backend.argtypes = [POINTER(SoundIoStructure), c_int]
        _soundio_connect_backend.restype = c_int
        return _soundio_connect_backend(sis, backend)

    def soundio_disconnect(self, sis):
        _soundio_disconnect = self.__lib.soundio_disconnect
        _soundio_disconnect.argtypes = [POINTER(SoundIoStructure)]
        _soundio_disconnect.restype = None
        return _soundio_disconnect(sis)

    def soundio_strerror(self, err):
        """错误代码转换为描述信息"""
        _soundio_strerror = self.__lib.soundio_strerror
        _soundio_strerror.argtypes = [c_int]
        _soundio_strerror.restype = c_char_p
        return bytes.decode(_soundio_strerror(err))

    def soundio_backend_name(self, backend):
        _soundio_backend_name = self.__lib.soundio_backend_name
        _soundio_backend_name.argtypes = [c_int]
        _soundio_backend_name.restype = c_char_p
        return bytes.decode(_soundio_backend_name(backend))

    def soundio_backend_count(self, sis):
        _soundio_backend_count = self.__lib.soundio_backend_count
        _soundio_backend_count.argtypes = [POINTER(SoundIoStructure)]
        _soundio_backend_count.restype = c_int
        return _soundio_backend_count(sis)

    def soundio_get_backend(self, sis, index):
        _soundio_get_backend = self.__lib.soundio_get_backend
        _soundio_get_backend.argtypes = [POINTER(SoundIoStructure)]
        _soundio_get_backend.restype = c_int
        return _soundio_get_backend(sis, index)

    def soundio_have_backend(self, backend):
        _soundio_have_backend = self.__lib.soundio_get_backend
        _soundio_have_backend.argtypes = [c_int]
        _soundio_have_backend.restype = c_bool
        return _soundio_have_backend(backend)

    def soundio_flush_events(self, sis):
        """
        自动更新所有链接的设备,调用时将触发回调 on_devices_change,on_backend_disconnect
        在调用
            soundio_input_device_count soundio_output_device_count
            soundio_get_input_device soundio_get_output_device
            soundio_default_input_device_index soundio_default_output_device_index
        前必须调用(相同线程)
        :param sis:
        :return:
        """
        _soundio_flush_events = self.__lib.soundio_flush_events
        _soundio_flush_events.argtypes = [POINTER(SoundIoStructure)]
        _soundio_flush_events.restype = None
        return _soundio_flush_events(sis)

    def soundio_wait_events(self, sis):
        _soundio_wait_events = self.__lib.soundio_wait_events
        _soundio_wait_events.argtypes = [POINTER(SoundIoStructure)]
        _soundio_wait_events.restype = None
        return _soundio_wait_events(sis)

    def soundio_wakeup(self, sis):
        """停止堵塞"""
        _soundio_wakeup = self.__lib.soundio_wakeup
        _soundio_wakeup.argtypes = [POINTER(SoundIoStructure)]
        _soundio_wakeup.restype = None
        return _soundio_wakeup(sis)

    def soundio_force_device_scan(self, sis):
        _soundio_force_device_scan = self.__lib.soundio_force_device_scan
        _soundio_force_device_scan.argtypes = [POINTER(SoundIoStructure)]
        _soundio_force_device_scan.restype = None
        return _soundio_force_device_scan(sis)

    def soundio_channel_layout_equal(self, scla, sclb):
        _soundio_channel_layout_equal = self.__lib.soundio_channel_layout_equal
        _soundio_channel_layout_equal.argtypes = [POINTER(SoundIoChannelLayoutStructure),
                                                  POINTER(SoundIoChannelLayoutStructure)]
        _soundio_channel_layout_equal.restype = c_bool
        return _soundio_channel_layout_equal(scla, sclb)

    def soundio_get_channel_name(self, cid):
        _soundio_get_channel_name = self.__lib.soundio_get_channel_name
        _soundio_get_channel_name.argtypes = [c_int]
        _soundio_get_channel_name.restype = c_char_p
        return bytes.decode(_soundio_get_channel_name(cid))

    def soundio_parse_channel_id(self, name):
        _soundio_parse_channel_id = self.__lib.soundio_parse_channel_id
        _soundio_parse_channel_id.argtypes = [c_char_p, c_int]
        _soundio_parse_channel_id.restype = c_int
        return bytes.decode(_soundio_parse_channel_id(name, len(name)))

    def soundio_channel_layout_builtin_count(self):
        _soundio_channel_layout_builtin_count = self.__lib.soundio_channel_layout_builtin_count
        _soundio_channel_layout_builtin_count.argtypes = None
        _soundio_channel_layout_builtin_count.restype = c_int
        return _soundio_channel_layout_builtin_count();

    def soundio_channel_layout_get_builtin(self, index):
        _soundio_channel_layout_get_builtin = self.__lib.soundio_channel_layout_get_builtin
        _soundio_channel_layout_get_builtin.argtypes = [c_int]
        _soundio_channel_layout_get_builtin.restype = POINTER(SoundIoChannelLayoutStructure)
        return _soundio_channel_layout_get_builtin(index)

    def soundio_channel_layout_get_default(self, channel_count):
        _soundio_channel_layout_get_default = self.__lib.soundio_channel_layout_get_default
        _soundio_channel_layout_get_default.argtypes = [c_int]
        _soundio_channel_layout_get_default.restype = POINTER(SoundIoChannelLayoutStructure)
        return _soundio_channel_layout_get_default(channel_count)

    def soundio_channel_layout_find_channel(self, layout, channel):
        _soundio_channel_layout_find_channel = self.__lib.soundio_channel_layout_find_channel
        _soundio_channel_layout_find_channel.argtypes = [POINTER(SoundIoChannelLayoutStructure), c_int]
        _soundio_channel_layout_find_channel.restype = c_int
        return _soundio_channel_layout_find_channel(layout, channel)

    def soundio_channel_layout_detect_builtin(self, layout):
        _soundio_channel_layout_detect_builtin = self.__lib.soundio_channel_layout_detect_builtin
        _soundio_channel_layout_detect_builtin.argtypes = [POINTER(SoundIoChannelLayoutStructure)]
        _soundio_channel_layout_detect_builtin.restype = c_bool
        return _soundio_channel_layout_detect_builtin(layout)

    def soundio_best_matching_channel_layout(self, preferred_layouts, preferred_layout_count, available_layouts,
                                             available_layout_count):
        _soundio_best_matching_channel_layout = self.__lib.soundio_best_matching_channel_layout
        _soundio_best_matching_channel_layout.argtypes = [POINTER(SoundIoChannelLayoutStructure), c_int,
                                                          POINTER(SoundIoChannelLayoutStructure), c_int]
        _soundio_best_matching_channel_layout.restype = POINTER(SoundIoChannelLayoutStructure)
        return _soundio_best_matching_channel_layout(preferred_layouts, preferred_layout_count, available_layouts,
                                                     available_layout_count)

    def soundio_sort_channel_layouts(self, layouts, layout_count):
        _soundio_sort_channel_layouts = self.__lib.soundio_sort_channel_layouts
        _soundio_sort_channel_layouts.argtypes = [POINTER(SoundIoChannelLayoutStructure)]
        _soundio_sort_channel_layouts.restype = None
        return _soundio_sort_channel_layouts(layouts, layout_count)

    def soundio_get_bytes_per_sample(self, format):
        _soundio_get_bytes_per_sample = self.__lib.soundio_get_bytes_per_sample
        _soundio_get_bytes_per_sample.argtypes = [c_int]
        _soundio_get_bytes_per_sample.restype = c_int
        return _soundio_get_bytes_per_sample(format)

    def soundio_format_string(self, format):
        _soundio_format_string = self.__lib.soundio_format_string
        _soundio_format_string.argtypes = [c_int]
        _soundio_format_string.restype = c_char_p
        return bytes.decode(_soundio_format_string(format))

    def soundio_input_device_count(self, soundio):
        """获取输入设备数"""
        _soundio_input_device_count = self.__lib.soundio_input_device_count
        _soundio_input_device_count.argtypes = [POINTER(SoundIoStructure)]
        _soundio_input_device_count.restype = c_int
        return _soundio_input_device_count(soundio)

    def soundio_output_device_count(self, soundio):
        """获取输出设备数"""
        _soundio_output_device_count = self.__lib.soundio_output_device_count
        _soundio_output_device_count.argtypes = [POINTER(SoundIoStructure)]
        _soundio_output_device_count.restype = c_int
        return _soundio_output_device_count(soundio)

    def soundio_get_input_device(self, soundio, index):
        """获取指定输入设备"""
        _soundio_get_input_device = self.__lib.soundio_get_input_device
        _soundio_get_input_device.argtypes = [POINTER(SoundIoStructure), c_int]
        _soundio_get_input_device.restype = POINTER(SoundIoDeviceStrcuture)
        ret = _soundio_get_input_device(soundio, index)
        return ret

    def soundio_get_output_device(self, soundio, index):
        """
        获取指定输出设备
        :param soundio:
        :param index:
        :return:
        """
        _soundio_get_output_device = self.__lib.soundio_get_output_device
        _soundio_get_output_device.argtypes = [POINTER(SoundIoStructure), c_int]
        _soundio_get_output_device.restype = POINTER(SoundIoDeviceStrcuture)
        return _soundio_get_output_device(soundio, index)

    def soundio_default_input_device_index(self, soundio):
        """
        获取默认输入设备索引
        :param soundio:soundio_create返回
        :return int: 如果返回-1,则需要调用 soundio_flush_events
        """
        _soundio_default_input_device_index = self.__lib.soundio_default_input_device_index
        _soundio_default_input_device_index.argtypes = [POINTER(SoundIoStructure)]
        _soundio_default_input_device_index.restype = c_int
        return _soundio_default_input_device_index(soundio)

    def soundio_default_output_device_index(self, soundio):
        """
        获取默认输出设备索引
        :param soundio:soundio_create返回
        :return:如果返回-1,则需要调用 soundio_flush_events
        """
        _soundio_default_output_device_index = self.__lib.soundio_default_output_device_index
        _soundio_default_output_device_index.argtypes = [POINTER(SoundIoStructure)]
        _soundio_default_output_device_index.restype = c_int
        return _soundio_default_output_device_index(soundio)

    def soundio_device_ref(self, device):
        """给设备引用数+1"""
        _soundio_device_ref = self.__lib.soundio_device_ref
        _soundio_device_ref.argtypes = [POINTER(SoundIoDeviceStrcuture)]
        _soundio_device_ref.restype = None
        return _soundio_device_ref(device)

    def soundio_device_unref(self, device):
        """给设备引用数-1"""
        _soundio_device_unref = self.__lib.soundio_device_unref
        _soundio_device_unref.argtypes = [POINTER(SoundIoDeviceStrcuture)]
        _soundio_device_unref.restype = None
        return _soundio_device_unref(device)

    def soundio_device_equal(self, da, db):
        """判断两个设备是否一样,是否是同一设备"""
        _soundio_device_equal = self.__lib.soundio_device_equal
        _soundio_device_equal.argtypes = [POINTER(SoundIoDeviceStrcuture), POINTER(SoundIoDeviceStrcuture)]
        _soundio_device_equal.restype = c_bool
        return _soundio_device_equal(da, db)

    def soundio_device_sort_channel_layouts(self, device):
        """布局排序"""
        _soundio_device_sort_channel_layouts = self.__lib.soundio_device_sort_channel_layouts
        _soundio_device_sort_channel_layouts.argtypes = [POINTER(SoundIoDeviceStrcuture)]
        _soundio_device_sort_channel_layouts.restype = None
        return _soundio_device_sort_channel_layouts(device)

    def soundio_device_supports_format(self, device, format):
        """验证设备是否支持所传格式"""
        _soundio_device_supports_format = self.__lib.soundio_device_supports_format
        _soundio_device_supports_format.argtypes = [POINTER(SoundIoDeviceStrcuture), c_int]
        _soundio_device_supports_format.restype = c_bool
        return _soundio_device_supports_format(device, format)

    def soundio_device_supports_layout(self, device, layout):
        """验证函数"""
        _soundio_device_supports_layout = self.__lib.soundio_device_supports_layout
        _soundio_device_supports_layout.argtypes = [POINTER(SoundIoDeviceStrcuture),
                                                    POINTER(SoundIoChannelLayoutStructure)]
        _soundio_device_supports_layout.restype = c_bool
        return _soundio_device_supports_layout(device, layout)

    def soundio_device_supports_sample_rate(self, device, sample_rate):
        """设备是否支持采样率"""
        _soundio_device_supports_sample_rate = self.__lib.soundio_device_supports_sample_rate
        _soundio_device_supports_sample_rate.argtypes = [POINTER(SoundIoDeviceStrcuture), c_int]
        _soundio_device_supports_sample_rate.restype = c_bool
        return _soundio_device_supports_sample_rate(device, sample_rate)

    def soundio_device_nearest_sample_rate(self, device, sample_rate):
        """获取一个设备支持的与所传参数最接近的采样率"""
        _soundio_device_nearest_sample_rate = self.__lib.soundio_device_nearest_sample_rate
        _soundio_device_nearest_sample_rate.argtypes = [POINTER(SoundIoDeviceStrcuture), c_int]
        _soundio_device_nearest_sample_rate.restype = c_int
        return _soundio_device_nearest_sample_rate(device, sample_rate)

    def soundio_outstream_create(self, device):
        """创建输出流"""
        _soundio_outstream_create = self.__lib.soundio_outstream_create
        _soundio_outstream_create.argtypes = [POINTER(SoundIoDeviceStrcuture)]
        _soundio_outstream_create.restype = POINTER(SoundIoOutStreamStructure)
        return _soundio_outstream_create(device)

    def soundio_outstream_destroy(self, outstream):
        """销毁输出流"""
        _soundio_outstream_destroy = self.__lib.soundio_outstream_destroy
        _soundio_outstream_destroy.argtypes = [POINTER(SoundIoOutStreamStructure)]
        _soundio_outstream_destroy.restype = None
        return _soundio_outstream_destroy(outstream)

    def soundio_outstream_open(self, outstream):
        """打开输出流"""
        _soundio_outstream_open = self.__lib.soundio_outstream_open
        _soundio_outstream_open.argtypes = [POINTER(SoundIoOutStreamStructure)]
        _soundio_outstream_open.restype = c_int
        return _soundio_outstream_open(outstream)

    def soundio_outstream_start(self, outstream):
        _soundio_outstream_start = self.__lib.soundio_outstream_start
        _soundio_outstream_start.argtypes = [POINTER(SoundIoOutStreamStructure)]
        _soundio_outstream_start.restype = c_int
        return _soundio_outstream_start(outstream)

    def soundio_outstream_begin_write(self, outstream, areas, frame_count):
        _soundio_outstream_begin_write = self.__lib.soundio_outstream_begin_write
        # 二级指针
        _soundio_outstream_begin_write.argtypes = [POINTER(SoundIoOutStreamStructure),
                                                   POINTER(POINTER(SoundIoChannelAreaStructure)), POINTER(c_int)]
        _soundio_outstream_begin_write.restype = c_int
        return _soundio_outstream_begin_write(outstream, areas, frame_count)

    def soundio_outstream_end_write(self, outstream):
        _soundio_outstream_end_write = self.__lib.soundio_outstream_end_write
        _soundio_outstream_end_write.argtypes = [POINTER(SoundIoOutStreamStructure)]
        _soundio_outstream_end_write.restype = c_int
        return _soundio_outstream_end_write(outstream)

    def soundio_outstream_clear_buffer(self, outstream):
        _soundio_outstream_clear_buffer = self.__lib.soundio_outstream_clear_buffer
        _soundio_outstream_clear_buffer.argtypes = [POINTER(SoundIoOutStreamStructure)]
        _soundio_outstream_clear_buffer.restype = c_int
        return _soundio_outstream_clear_buffer(outstream)

    def soundio_outstream_pause(self, outstream, pause):
        _soundio_outstream_pause = self.__lib.soundio_outstream_pause
        _soundio_outstream_pause.argtypes = [POINTER(SoundIoOutStreamStructure), c_bool]
        _soundio_outstream_pause.restype = c_int
        return _soundio_outstream_pause(outstream, pause)

    def soundio_outstream_get_latency(self, outstream, out_latency):
        _soundio_outstream_get_latency = self.__lib.soundio_outstream_get_latency
        _soundio_outstream_get_latency.argtypes = [POINTER(SoundIoOutStreamStructure), POINTER(POINTER(c_double))]
        _soundio_outstream_get_latency.restype = c_int
        return _soundio_outstream_get_latency(outstream, out_latency)

    def soundio_instream_create(self, device):
        """创建输入流"""
        _soundio_instream_create = self.__lib.soundio_instream_create
        _soundio_instream_create.argtypes = [POINTER(SoundIoDeviceStrcuture)]
        _soundio_instream_create.restype = POINTER(SoundIoInStreamStrcuture)
        return _soundio_instream_create(device)

    def soundio_instream_destroy(self, instream):
        _soundio_instream_destroy = self.__lib.soundio_instream_destroy
        _soundio_instream_destroy.argtypes = [POINTER(SoundIoInStreamStrcuture)]
        _soundio_instream_destroy.restype = None
        return _soundio_instream_destroy(instream)

    def soundio_instream_open(self, instream):
        _soundio_instream_open = self.__lib.soundio_instream_open
        _soundio_instream_open.argtypes = [POINTER(SoundIoInStreamStrcuture)]
        _soundio_instream_open.restype = c_int
        return _soundio_instream_open(instream)

    def soundio_instream_start(self, instream):
        _soundio_instream_start = self.__lib.soundio_instream_start
        _soundio_instream_start.argtypes = [POINTER(SoundIoInStreamStrcuture)]
        _soundio_instream_start.restype = c_int
        return _soundio_instream_start(instream)

    def soundio_instream_begin_read(self, instream, areas, frame_count):
        _soundio_instream_begin_read = self.__lib.soundio_instream_begin_read
        _soundio_instream_begin_read.argtypes = [POINTER(SoundIoInStreamStrcuture),
                                                 POINTER(POINTER(SoundIoChannelAreaStructure)), POINTER(c_int)]
        _soundio_instream_begin_read.restype = c_int
        return _soundio_instream_begin_read(instream, areas, frame_count)

    def soundio_instream_end_read(self, instream):
        _soundio_instream_end_read = self.__lib.soundio_instream_end_read
        _soundio_instream_end_read.argtypes = [POINTER(SoundIoInStreamStrcuture)]
        _soundio_instream_end_read.restype = c_int
        return _soundio_instream_end_read(instream)

    def soundio_instream_pause(self, instream, pause):
        _soundio_instream_pause = self.__lib.soundio_instream_pause
        _soundio_instream_pause.argtypes = [POINTER(SoundIoInStreamStrcuture), c_bool]
        _soundio_instream_pause.restype = c_int
        return _soundio_instream_pause(instream, pause)

    def soundio_instream_get_latency(self, instream, out_latency):
        _soundio_instream_get_latency = self.__lib.soundio_instream_get_latency
        _soundio_instream_get_latency.argtypes = [POINTER(SoundIoInStreamStrcuture), POINTER(c_double)]
        _soundio_instream_get_latency.restype = c_int
        return _soundio_instream_get_latency(instream, out_latency)

    def soundio_ring_buffer_create(self, soundio, requested_capacity):
        """环形缓冲区(创建)"""
        _soundio_ring_buffer_create = self.__lib.soundio_ring_buffer_create
        _soundio_ring_buffer_create.argtypes = [POINTER(SoundIoStructure), c_int]
        _soundio_ring_buffer_create.restype = POINTER(SoundIoRingBufferStruct)
        return _soundio_ring_buffer_create(soundio, requested_capacity)

    def soundio_ring_buffer_destroy(self, ring_buffer):
        """环形缓冲区(销毁)"""
        _soundio_ring_buffer_destroy = self.__lib.soundio_ring_buffer_destroy
        _soundio_ring_buffer_destroy.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_destroy.restype = None
        return _soundio_ring_buffer_destroy(ring_buffer)

    def soundio_ring_buffer_capacity(self, ring_buffer):
        """环形缓冲区容量)"""
        _soundio_ring_buffer_capacity = self.__lib.soundio_ring_buffer_capacity
        _soundio_ring_buffer_capacity.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_capacity.restype = c_int
        return _soundio_ring_buffer_capacity(ring_buffer)

    def soundio_ring_buffer_write_ptr(self, ring_buffer):
        _soundio_ring_buffer_write_ptr = self.__lib.soundio_ring_buffer_write_ptr
        _soundio_ring_buffer_write_ptr.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_write_ptr.restype = c_char_p
        return _soundio_ring_buffer_write_ptr(ring_buffer)

    def soundio_ring_buffer_advance_write_ptr(self, ring_buffer, count):
        _soundio_ring_buffer_write_ptr = self.__lib.soundio_ring_buffer_write_ptr
        _soundio_ring_buffer_write_ptr.argtypes = [POINTER(SoundIoRingBufferStruct), count]
        _soundio_ring_buffer_write_ptr.restype = None
        return _soundio_ring_buffer_write_ptr(ring_buffer, count)

    def soundio_ring_buffer_read_ptr(self, ring_buffer):
        _soundio_ring_buffer_read_ptr = self.__lib.soundio_ring_buffer_read_ptr
        _soundio_ring_buffer_read_ptr.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_read_ptr.restype = c_char_p
        return _soundio_ring_buffer_read_ptr(ring_buffer)

    def soundio_ring_buffer_advance_read_ptr(self, ring_buffer, count):
        _soundio_ring_buffer_advance_read_ptr = self.__lib.soundio_ring_buffer_advance_read_ptr
        _soundio_ring_buffer_advance_read_ptr.argtypes = [POINTER(SoundIoRingBufferStruct), count]
        _soundio_ring_buffer_advance_read_ptr.restype = None
        return _soundio_ring_buffer_advance_read_ptr(ring_buffer, count)

    def soundio_ring_buffer_fill_count(self, ring_buffer):
        _soundio_ring_buffer_fill_count = self.__lib.soundio_ring_buffer_fill_count
        _soundio_ring_buffer_fill_count.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_fill_count.restype = c_int
        return _soundio_ring_buffer_fill_count(ring_buffer)

    def soundio_ring_buffer_free_count(self, ring_buffer):
        _soundio_ring_buffer_free_count = self.__lib.soundio_ring_buffer_free_count
        _soundio_ring_buffer_free_count.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_free_count.restype = c_int
        return _soundio_ring_buffer_free_count(ring_buffer)

    def soundio_ring_buffer_clear(self, ring_buffer):
        _soundio_ring_buffer_clear = self.__lib.soundio_ring_buffer_clear
        _soundio_ring_buffer_clear.argtypes = [POINTER(SoundIoRingBufferStruct)]
        _soundio_ring_buffer_clear.restype = None
        return _soundio_ring_buffer_clear(ring_buffer)

    def callback_ptr(self, restype, *argtypes, **kw):
        """构建回调函数,需要对 *argtypes, **kw 拆包"""
        return CFUNCTYPE(restype, *argtypes, **kw)