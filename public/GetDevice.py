# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import lib.Utils as U
import lib.adbUtils
import yaml


def get_device():
    """

    :return: 返回Android设备列表
    """

    android_devices_list = []
    for device in U.cmd('adb devices').stdout.readlines():
        if 'device' in device and 'devices' not in device:
            device = device.split('\t')[0]
            android_devices_list.append(device)

    return android_devices_list


def set_device_yaml():
    """
    获取当前设备的Android version并且保存到yaml里
    :return:
    """
    device_lst = []
    for device in get_device():
        adb = lib.adbUtils.ADB(device)
        U.Logging.success(
            'get device:{},Android version:{}'.format(
                device, adb.get_android_version()))
        device_lst.append({'platformVersion': adb.get_android_version(
        ), 'deviceName': device, 'platformName': 'Android'})

    ini = U.ConfigIni()
    with open(ini.get_ini('test_device', 'device'), 'w') as f:
        yaml.dump(device_lst, f)
        f.close()


if __name__ == '__main__':
    set_device_yaml()
