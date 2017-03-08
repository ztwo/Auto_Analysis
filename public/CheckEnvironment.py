# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/12/6 下午6:31
"""
import lib.Utils as U
import public.GetDevice


def check_environment():
    appium = U.cmd("appium -v").stdout.readline().strip()
    if '1.' not in appium:
        U.Logging.error('appium not in computer')
        exit()
    else:
        U.Logging.info('appium version {}'.format(appium))
    if not public.GetDevice.get_device():
        U.Logging.error('the computer is not connected to any devices')
        exit()

if __name__ == '__main__':
    check_environment()