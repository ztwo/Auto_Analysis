# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import lib.adbUtils


class Al:
    def __init__(self, device):
        self.device = device

    def _get_android_log(self, log_path):
        """

        :return:清理当前设备缓存log,并且记录当前设备log
        """

        adb = lib.adbUtils.ADB(self.device)
        adb.c_logcat()
        adb.logcat(log_path)

    def main(self, log_path):
        """

        :return: 开启记录log
        """
        return self._get_android_log(log_path)


if __name__ == '__main__':
    a = Al('0530dc6a')
