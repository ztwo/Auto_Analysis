# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/21 上午11:54
"""
import os


def all_file_path(root_directory, extension_name):
    """

    :return: 遍历文件目录
    """
    file_dic = {}
    for parent, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if 'filter' not in filename:
                if filename.endswith(extension_name):
                    path = os.path.join(parent, filename).replace('\\', '/')
                    file_dic[filename] = path
    return file_dic
