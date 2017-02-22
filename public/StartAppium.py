# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import lib.Utils as U
import random
import platform


class Sp:
    def __init__(self, device):
        self.device = device

    def __start_driver(self, aport, bpport):
        """
        清理logcat与appium所有进程
        :return:
        """
        if platform.system() == 'Windows':
            # 在win10启动appium有bug,暂时处理方案
            import subprocess
            subprocess.Popen("appium -p %s -bp %s -U %s" %
                             (aport, bpport, self.device), shell=True)

        else:
            appium = U.cmd("appium -p %s -bp %s -U %s" %
                           (aport, bpport, self.device))  # 启动appium
            while True:
                appium_line = appium.stdout.readline().strip()
                U.Logging.debug(appium_line)
                U.sleep(1)
                if 'listener started' in appium_line or 'Error: listen' in appium_line:
                    break

    def start_appium(self):
        """
        启动appium
        p:appium port
        bp:bootstrap port
        :return: 返回appium端口参数
        """

        aport = random.randint(4700, 4900)
        bpport = random.randint(4700, 4900)
        self.__start_driver(aport, bpport)

        U.Logging.debug(
            'start appium :p %s bp %s device:%s' %
            (aport, bpport, self.device))
        U.sleep(10)
        return aport

    def main(self):
        """

        :return: 启动appium
        """
        return self.start_appium()


if __name__ == '__main__':
    s = Sp('0530dc6a')
    s.main()
