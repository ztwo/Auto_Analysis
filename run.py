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
