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
import public.CleanProcess


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
    initialization_arrangement_case()
    import public.GetDevice

    public.GetDevice.set_device_yaml()

    import po.integration
    from multiprocessing import Pool


    def case_sun(device):
        a = po.integration.RunApp(device)
        a.case_start()


    device_list = po.integration.get_device_info()
    pool = Pool(len(device_list))
    pool.map(case_sun, device_list)
    pool.close()
    pool.join()
    cp = public.CleanProcess.Cp()
    cp.clean_process_all()
