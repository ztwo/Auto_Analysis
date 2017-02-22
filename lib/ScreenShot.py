# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""

import os
import Utils as U
import adbUtils
import random


class minicap():
    def __init__(self, device):
        self.adb = adbUtils.ADB(device)
        ini = U.ConfigIni()
        self.minicap_path = ini.get_ini(
            'minicap', 'minicap_path').format(
            self.adb.get_cpu_version())
        self.minitouch_path = ini.get_ini(
            'minicap', 'minitouch_path').format(
            self.adb.get_cpu_version())
        self.minicapSO_path = ini.get_ini(
            'minicap', 'minicapSO_path').format(
            self.adb.get_sdk_version(), self.adb.get_cpu_version())

    def push_minicap(self):
        U.Logging.info('push_Cpu_minicap:' + self.minicap_path)
        self.adb.adb('push %s /data/local/tmp' % self.minicap_path)

    def push_minicaptouch(self):
        U.Logging.info('push_touch_minitouch:' + self.minitouch_path)
        self.adb.shell('chmod 777 /data/local/tmp/minitouch')

    def push_minicapSO(self):
        U.Logging.info('push_sdk_minicap.so:' + self.minicapSO_path)
        self.adb.adb('push %s /data/local/tmp' % self.minicapSO_path)
        self.adb.shell('chmod 777 /data/local/tmp/minicap')

    def check_minicap(self):
        width = None
        height = None
        for i in self.adb.shell(
                "'LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -i'").stdout.readlines():
            if 'secure' in i and 'true' in i:
                U.Logging.info('push_minicap_sdk:success')
            elif 'width' in i:
                width = i.strip().split(':')[1].strip().split(',')[0]
            elif 'height' in i:
                height = i.strip().split(':')[1].strip().split(',')[0]

        if width is not None:
            return width, height
        return width, height

    def phone_screen(self, width_height):
        """
        截图
        :param width_height: 宽高
        :param filename: 存储的文件名
        :return:
        """

        U.Logging.info('phone_screen:%s' % width_height)
        filename = str(random.randint(1,1000))
        self.adb.shell(
            "'LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}/0 -s > /data/local/tmp/{}.png'".format(
                width_height, filename))
        U.Logging.info('phone_screen:success')
        return filename

    def pull_screen(self, filename, computer_path):
        self.adb.pull(
            '/data/local/tmp/{}.png'.format(filename),
            computer_path)

    def main(self,computer_path):
        if os.path.exists(self.minicapSO_path):
            width, height = self.check_minicap()
            width_height = '{}x{}@{}x{}'.format(width, height, width, height)
            # U.Logging.info('main:filename:%s' % filename)

            if 'None' not in width_height:
                U.Logging.info('main:exist minicap')
                filename = self.phone_screen(width_height)
                U.sleep(0.3)
                self.pull_screen(filename, computer_path)
            else:
                U.Logging.info('main:does not exist minicap')
                self.push_minicap()
                self.push_minicaptouch()
                self.push_minicapSO()
                U.sleep(0.3)
                width, height = self.check_minicap()
                width_height = '{}x{}@{}x{}'.format(
                    width, height, width, height)
                filename = self.phone_screen(width_height)
                U.sleep(0.3)
                self.pull_screen(filename, computer_path)
            self.adb.rm_minicap_jpg(filename)
        else:
            U.Logging.warn('not minicap found ,check the directory')
            self.adb.screen_shot(computer_path)


if __name__ == '__main__':
    a = minicap('BX903JC3WS')
    a.main('/Users/joko/Documents/Auto_Analysis/result/2016-11-30_14_00_1521/img/2.png')
