import flv
import unittest


class TestFlv(unittest.TestCase):
    """python单元测试"""

    def test_load(self):
        fl = flv.Flv()
        ret = fl.load("20180510-155845.flv")
        print("共找到%d个tag" % ret)


if __name__ == "__main__":
    """代替命令行下的 python3 -m unittest flv_test.py"""
    unittest.main()