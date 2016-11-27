# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import lib.Utils as U
import random


class Sp:

    def __init__(self, device):
        self.device = device

    def start_appium(self):
        """
        启动appium
        p:appium port
        bp:bootstrap port
        :return: 返回appium端口参数
        """

        aport = random.randint(4700, 4900)
        bpport = random.randint(4700, 4900)
        U.cmd("appium -p %s -bp %s -U %s" %
              (aport, bpport, self.device))  # 启动appium
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
