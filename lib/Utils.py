# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import time
import subprocess
import os
import sys
import ConfigParser
import sqlite3
import re


def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def sleep(s):
    return time.sleep(s)


def cmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,bufsize=1,close_fds=True)


class ConfigIni():
    def __init__(self):
        self.current_directory = os.path.split(
            os.path.realpath(sys.argv[0]))[0]
        self.path = os.path.split(__file__)[0].replace('lib','data/test_info.ini')
        self.cf = ConfigParser.ConfigParser()

        self.cf.read(self.path)

    def get_ini(self, title, value):
        return self.cf.get(title, value)

    def set_ini(self, title, value, text):
        self.cf.set(title, value, text)
        return self.cf.write(open(self.path, "wb"))

    def add_ini(self, title):
        self.cf.add_section(title)
        return self.cf.write(open(self.path))

    def get_options(self, data):
        # 获取所有的section
        options = self.cf.options(data)
        return options


class colour:
    @staticmethod
    def c(msg, colour):
        try:
            from termcolor import colored, cprint
            p = lambda x: cprint(x, '%s' % colour)
            return p(msg)
        except:
            print (msg)

    @staticmethod
    def show_verbose(msg):
        colour.c(msg, 'white')

    @staticmethod
    def show_debug(msg):
        colour.c(msg, 'blue')

    @staticmethod
    def show_info(msg):
        colour.c(msg, 'green')

    @staticmethod
    def show_warn(msg):
        colour.c(msg, 'yellow')

    @staticmethod
    def show_error(msg):
        colour.c(msg, 'red')


class Logging:
    flag = True

    @staticmethod
    def error(msg):
        if Logging.flag == True:
            # print get_now_time() + " [Error]:" + "".join(msg)
            colour.show_error(get_now_time() + " [Error]:" + "".join(msg))

    @staticmethod
    def warn(msg):
        if Logging.flag == True:
            colour.show_warn(get_now_time() + " [Warn]:" + "".join(msg))

    @staticmethod
    def info(msg):
        if Logging.flag == True:
            colour.show_info(get_now_time() + " [Info]:" + "".join(msg))

    @staticmethod
    def debug(msg):
        if Logging.flag == True:
            colour.show_debug(get_now_time() + " [Debug]:" + "".join(msg))

    @staticmethod
    def success(msg):
        if Logging.flag == True:
            colour.show_verbose(get_now_time() + " [Success]:" + "".join(msg))


def l():
    """
    打印log
    文件名+函数名,return
    :return:
    """

    def log(func):
        def wrapper(*args, **kwargs):
            t = func(*args, **kwargs)
            filename = str(sys.argv[0]).split('/')[-1].split('.')[0]
            Logging.success('{}:{}, return:{}'.format(filename, func.__name__, t))
            return t

        return wrapper

    return log


class Asql:
    def __init__(self, ):
        ini = ConfigIni()
        test_db_path = ini.get_ini('test_db', 'test_result')
        self.conn = sqlite3.connect(test_db_path)
        self.cursor = self.conn.cursor()
        self.__is_table()

    def execute(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return: 提交数据
        """
        self.cursor.execute(*args, **kwargs)

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def __is_table(self):
        """
        判断表是否存在
        :return:
        """
        self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='test_results'")
        row = self.cursor.fetchone()
        if row[0] != 1:
            self.__built_table()

    def __built_table(self):
        """
        建表
        :return:
        """
        self.execute("""
        CREATE TABLE test_results
        (
            case_id INTEGER PRIMARY KEY,
            case_name TEXT,
            device_name TEXT,
            cpu_list TEXT,
            mem_list TEXT,
            execution_status TEXT,
            created_time DATETIME DEFAULT (datetime('now', 'localtime'))
        );""")

    def insert_per(self, case_name, device_name, cpu_list, mem_list, execution_status, ):
        key = "(case_name,device_name,cpu_list,mem_list,execution_status,created_time)"
        values = "('{}','{}','{}','{}','{}','{}')" \
            .format(case_name, device_name, cpu_list, mem_list, execution_status, get_now_time())
        self.execute("INSERT INTO test_results {} VALUES {}".format(key, values))

    def select_per(self, case_name, device_name):
        statement = "select * from test_results where " \
                    "case_name = '{}' " \
                    "and " \
                    "device_name = '{}' " \
                    "and " \
                    "execution_status = 1 " \
                    "order by created_time desc".format(case_name, device_name)
        self.cursor.execute(statement)
        row = self.cursor.fetchone()
        if row is not None:
            cpu = re.findall(r"\d+\.?\d*", row[3])
            mem = re.findall(r"\d+\.?\d*", row[4])
            return [int(i) for i in cpu], [int(i) for i in mem]
        else:
            return None


if __name__ == '__main__':
    a = Asql()
    print (a.select_per('login1', 'sanxing'))
    a.close()
