# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/16 上午10:48
"""
import lib.Utils as U
import GetFilePath


@U.l()
def case_yaml_file():
    """

    :return: 返回当前设备下的yaml test case列表
    """
    ini = U.ConfigIni()
    yaml_path = ini.get_ini('test_case', 'case')
    return GetFilePath.all_file_path(yaml_path, '.yaml')


if __name__ == '__main__':
    print case_yaml_file()
