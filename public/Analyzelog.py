# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/15 下午1:44
"""
import lib.Utils as U
import GetFilePath
import os


class Anl:
    def __init__(self, all_result_path):
        self.all_result_path = all_result_path

    @U.l()
    def __log_file(self, all_path_result, the_suffix_name):
        """

        :return: 日志列表
        """
        return GetFilePath.all_file_path(
            all_path_result, the_suffix_name).values()

    def analyze(self, log_file):
        """
        过滤Exception到log文件夹内
        :param log_file: log的路径
        :return:
        """
        errorId = 0
        go_on_id = 0
        log_filter_name = os.path.split(log_file)[1].split('.')[0]
        with open(self.all_result_path + '/log/{}filter.log'.format(log_filter_name), 'w') as s:

            with open(log_file) as f:
                for line in f:
                    if 'Exception' in line:
                        go_on_id = 1
                        s.write('#' + '-' * 40 + '\n')
                        s.write(line)
                        errorId = line.split('(')[1].split(')')[0].strip()
                    elif go_on_id == 1:
                        if errorId in line:
                            s.write(line)
                        else:
                            go_on_id = 0

    def main(self):
        """
        获取log,生成filter log
        :return:
        """
        for log_file in self.__log_file(self.all_result_path, '.log'):
            self.analyze(log_file)


if __name__ == '__main__':
    a = Anl('/Users/joko/Documents/Auto_Analysis/result/2016-11-27_20_23_1239')
    a.main()
