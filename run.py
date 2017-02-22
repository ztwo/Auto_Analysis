# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/10 下午3:55
"""
import os
import sys

main_view = os.path.split(os.path.realpath(sys.argv[0]))[0]
sys.path.append(main_view)
import public.CleanProcess
import public.GetDevice
import po.integration
import public.CheckEnvironment
public.CheckEnvironment.check_environment()

import threading


class r(threading.Thread):
    def __init__(self, device, ):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
        a = po.integration.RunApp(self.device)
        a.case_start()


def run_device():
    public.GetDevice.set_device_yaml()
    device_list = po.integration.get_device_info()
    for device in device_list:
        test_run = r(device)
        test_run.start()
    test_run.join()


if __name__ == '__main__':
    run_device()
    cl = public.CleanProcess.Cp()
    cl.clean_process_all()
