# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/16 下午2:05
"""
import os
import sys

main_view = os.path.split(os.path.realpath(sys.argv[0]))[0]
main_view = main_view.replace('\\', '/')
sys.path.append(main_view)
import lib.Utils as U
import public.CheckEnvironment


def initialization_arrangement_case():
    ini = U.ConfigIni()
    ini.set_ini('minicap', 'minicap_path', main_view + '/data/minicap/bin/{}/minicap')
    ini.set_ini('minicap', 'minitouch_path', main_view + '/data/minicap/minitouch/{}/minitouch')
    ini.set_ini('minicap', 'minicapso_path', main_view + '/data/minicap/shared/android-{}/{}/minicap.so')

    ini.set_ini('test_case', 'case', main_view + '/testcase')
    ini.set_ini('test_case', 'log_file', main_view + '/result')
    ini.set_ini('test_case', 'error_img', main_view + '/data/incidental/error.png')

    ini.set_ini('test_device', 'device', main_view + '/data/incidental/device_info.yaml')

    ini.set_ini('test_db', 'test_result', main_view + '/data/incidental/test.db')

    ini.set_ini('test_install_path', 'path', main_view + '/data/app.apk')
    ini.set_ini('test_info', 'info', main_view + '/data/appium_parameter.yaml')


if __name__ == '__main__':
    public.CheckEnvironment.check_environment()
    initialization_arrangement_case()
    import run
    run.run_device()