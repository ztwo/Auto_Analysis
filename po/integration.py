# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/5 下午1:00
"""

import time
import os
import yaml
from appium import webdriver
import lib.Utils as U
import ExecuteCase
import public.StartAppium
import public.GetHtml
import public.GetLog
import public.CleanProcess
import public.Performance
import public.installApp
import public.GetCase
import random


class RunApp(object):
    def __init__(self, device_l):
        """
        self.time:用于建立存放文件的目录
        """
        self.time = time.strftime(
            "%Y-%m-%d_%H_%M_%S",
            time.localtime(
                time.time()))
        self.device_l = device_l
        self.device = self.device_l['deviceName']
        U.Logging.info('start test device:%s' % self.device)

        self.all_result_path = self.mkdir_file()
        self.ia = public.installApp.Ia(self.all_result_path, self.device)

    def mkdir_file(self):
        """

        :return:创建日志存放文件夹
        """
        ini = U.ConfigIni()
        result_file = str(ini.get_ini('test_case', 'log_file'))
        result_file_every = result_file + '/' + \
                            time.strftime("%Y-%m-%d_%H_%M_%S{}".format(random.randint(10, 99)),
                                          time.localtime(time.time()))
        file_list = [
            result_file,
            result_file_every,
            result_file_every + '/log',
            result_file_every + '/per',
            result_file_every + '/img',
            result_file_every + '/status']
        if not os.path.exists(result_file):
            os.mkdir(result_file)

        for file_path in file_list:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        return result_file_every

    def __install_app(self):
        self.ia.main()

    @U.l()
    def __get_appium_port(self):
        """

        :return: 开启appium端口
        """
        sp = public.StartAppium.Sp(self.device)
        self.appium_port = sp.main()
        return self.appium_port

    @U.l()
    def clear_process(self):
        """

        :return: 清理appium与logcat进程
        """
        cp = public.CleanProcess.Cp()
        cp.clean_process(self.appium_port, self.device)
        return self.appium_port

    def start_appium(self):
        """
        启动driver
        :return:
        """

        number_of_starts = 0
        while number_of_starts < 6:
            try:
                self.driver = webdriver.Remote(
                    'http://127.0.0.1:%s/wd/hub' %
                    self.__get_appium_port(), self.device_l)
                U.Logging.debug('appium start %s success' % self.device)
                return self.driver
            except Exception as e:
                number_of_starts += 1
                U.Logging.error('Failed to start appium :{}'.format(e))
                U.Logging.error(
                    'Try restarting the appium :{},Trying the {} frequency'.format(self.device, number_of_starts))
                U.sleep(5)
        if number_of_starts > 5:
            U.Logging.error('Can not start appium, the program exits')
            exit()

    def analysis(self, yaml_name, yaml_path):
        """
        继承driver开始测试
        :param path_yaml: 测试用例地址
        :return:
        """

        s = ExecuteCase.start_case(
            self.start_appium(),
            yaml_name,
            yaml_path,
            self.all_result_path,
            self.device)
        return s.main()

    def case_start(self):
        """
        控制diver开启 and 关闭,且清理进程
        执行步骤:
            1:安装应用
            2:开启driver,并且执行测试
            3:关闭driver
            4:清理logcat appium 进程
        :return:
        """

        test_case_yaml = public.GetCase.case_yaml_file().items()
        if not test_case_yaml:
            U.Logging.error('not yaml found ')
        else:
            for yaml_name, yaml_path in test_case_yaml:
                U.Logging.success('yaml path:{}'.format(yaml_path))
                self.__install_app()

                self.analysis(yaml_name, yaml_path)
                try:
                    self.driver.quit()
                except Exception as e:
                    U.Logging.warn('driver quit Error %s'%e)
                self.clear_process()


def get_device_info():
    """
    获取当前电脑连接的devices
    :return: 返回设备列表
    """
    device_list = []
    ini = U.ConfigIni()
    test_info = ini.get_ini('test_info', 'info')
    test_device = ini.get_ini('test_device', 'device')
    with open(test_info) as f:
        test_dic = yaml.load(f)[0]

    with open(test_device) as f:
        for device in yaml.load(f):
            device_list.append(dict(test_dic.items() + device.items()))

    return device_list


if __name__ == '__main__':
    import public.GetDevice

    public.GetDevice.set_device_yaml()
    for device in get_device_info():
        a = RunApp(device)
        a.case_start()
