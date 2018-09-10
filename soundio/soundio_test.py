import unittest
import soundio
from ctypes import *


def on_devices_change_callback(sis):
    """设备发生改变时的回调"""
    print("\r\n当前:%s backend:%d" % (bytes.decode(sis.contents.app_name), sis.contents.current_backend))
    pass


class SoundIoTest(unittest.TestCase):
    def test_devices(self):
        """获取设备列表"""
        s = soundio.SoundIo()
        with s as sis:
            sis.contents.on_devices_change = s.callback_ptr(None, POINTER(soundio.SoundIoStructure))(
                on_devices_change_callback)
            if soundio.SoundIoError.SoundIoErrorNone.value == s.soundio_connect(sis):
                s.soundio_flush_events(sis)
                ic = s.soundio_input_device_count(sis);
                oc = s.soundio_output_device_count(sis);
                ici, oci = 0, 0
                while ici < ic:
                    ids = s.soundio_get_input_device(sis, ici)
                    ici += 1
                    print("输入(%d):%s" % (ici, bytes.decode(ids.contents.name)))

                print("");
                while oci < oc:
                    ods = s.soundio_get_output_device(sis, oci)
                    oci += 1
                    print("输出(%d):%s" % (oci, bytes.decode(ods.contents.name)))
            s.soundio_disconnect(sis)


if __name__ == "__main__":
    unittest.main()