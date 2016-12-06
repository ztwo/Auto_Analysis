# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/11 上午10:52
"""
import lib.adbUtils
import xml.etree.cElementTree as ET
import re
import lib.Utils as U
import threading
from multiprocessing import Queue
import os


class Ia:
    def __init__(self, all_result_path, device):
        """
        Queue模块是用于进程间通信的模块

        :param all_result_path: 本次测试创建的文件夹
        :param device: 设备id
        """
        self.all_result_path = all_result_path
        self.device = device
        self.adb = lib.adbUtils.ADB(self.device)
        self.queue = Queue(10)

    @U.l()
    def __uidump(self):
        """
        获取当前Activity控件树
        :return:xml在电脑内的地址存储地址
        """
        save_path = self.all_result_path + "/dump.xml"
        self.adb.get_focused_package_xml(save_path)
        return save_path

    @U.l()
    def __element(self):
        """
        同属性单个元素，返回单个坐标元组
        button_list:常见的确认,同意,按钮控件id
        """
        button0 = 'com.android.packageinstaller:id/ok_button'
        button1 = 'com.android.packageinstaller:id/btn_allow_once'
        button2 = 'com.android.packageinstaller:id/bottom_button_two'
        button3 = 'com.android.packageinstaller:id/btn_continue_install'
        button4 = 'android:id/button1'
        button5 = 'vivo:id/vivo_adb_install_ok_button'
        button_list = [button0, button1, button2, button3, button4, button5]
        self.__uidump()
        self.pattern = re.compile(r"\d+")
        if not os.path.exists(self.all_result_path + "/dump.xml"):
            U.Logging.warn('Failed to get xml')
            return None

        tree = ET.ElementTree(file=self.all_result_path + "/dump.xml")
        tree_iter = tree.iter(tag="node")
        for elem in tree_iter:
            if elem.attrib["resource-id"] in button_list:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                x_point = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y_point = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                return x_point, y_point
        else:
            return None

    def tap(self):
        """
        点击动作
        :return:
        """
        coordinate_points = self.__element()
        if coordinate_points is not None:
            self.adb.touch_by_element(coordinate_points)

    def tap_all(self):
        """
        不间断获取xml,并且点击。配合多线程使用
        :return:
        """
        while True:
            self.tap()
            if not self.queue.empty():
                break

    @U.l()
    def __install_app(self, package_name, app_file_path):
        """

        :param package_name: 应用的报名:com:x.x
        :param app_file_path: 应用的安装路径,注意需要绝对路径
        :return:
        """
        self.adb.quit_app(
            'com.android.packageinstaller')  # kill安装程序,用于处理oppo的一个bug
        if self.queue.empty():
            if self.adb.is_install(package_name):
                U.Logging.success(
                    'del {}-{}'.format(self.device, package_name))
                self.adb.remove_app(package_name)
            install_num = 0
            while install_num < 4:
                install_info = self.adb.install_app(app_file_path).stdout.readlines()
                U.Logging.success('install_info:%s'%install_info)
                if self.adb.is_install(package_name):
                    self.queue.put(1)
                    break
                else:
                    U.Logging.error('Reinstalling %s %s '%(package_name,self.device))
                    install_num += 1
            else:
                raise AssertionError('Reinstalling app error')

            # kill安装程序,用于处理oppo的一个bug
            self.adb.quit_app('com.android.packageinstaller')

    def main(self):
        """
        开启多线程:
                线程1:安装应用
                线程2:获取当前页面是否有可点击的按钮
        :return:
        """
        ini = U.ConfigIni()
        install_file = ini.get_ini('test_install_path', 'path')
        package_name = ini.get_ini('test_package_name', 'package_name')

        threads = []

        click_button = threading.Thread(target=self.tap_all, args=())
        threads.append(click_button)
        install_app = threading.Thread(
            target=self.__install_app, args=(
                package_name, install_file))
        threads.append(install_app)
        process_list = range(len(threads))

        for i in process_list:
            threads[i].start()
        for i in process_list:
            threads[i].join()

        self.adb.shell('"rm -r /data/local/tmp/*.xml"')


if __name__ == '__main__':
    a = Ia('/Users/joko/Desktop/temp', 'VGAMCQEI99999999')
    a.main()
