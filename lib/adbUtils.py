# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import platform
import subprocess
import re
from time import sleep
import time
import os
import random

PATH = lambda p: os.path.abspath(p)

# 判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

# 判断是否设置环境变量ANDROID_HOME
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(
            os.environ["ANDROID_HOME"],
            "platform-tools",
            "adb.exe")
    else:
        command = os.path.join(
            os.environ["ANDROID_HOME"],
            "platform-tools",
            "adb")
else:
    raise EnvironmentError(
        "Adb not found in $ANDROID_HOME path: %s." %
        os.environ["ANDROID_HOME"])


class ADB(object):
    """
    单个设备，可不传入参数device_id
    """

    def __init__(self, device_id=""):
        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s %s" % device_id

    def adb(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args),)
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def get_device_state(self):
        """
        获取设备状态： offline | bootloader | device
        """
        return self.adb("get-state").stdout.read().strip()

    def get_device_id(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip()

    def get_android_version(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        return self.shell(
            "getprop ro.build.version.release").stdout.read().strip()

    def get_sdk_version(self):
        """
        获取设备SDK版本号
        """
        return self.shell("getprop ro.build.version.sdk").stdout.read().strip()

    def get_device_model(self):
        """
        获取设备型号
        """
        return self.shell("getprop ro.product.model").stdout.read().strip()

    def get_pid(self, package_name):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.android.settings")
        """
        if system is "Windows":
            pidinfo = self.shell(
                "ps | findstr %s$" %
                package_name).stdout.read()
        else:
            pidinfo = self.shell(
                "ps | %s -w %s" %
                (find_util, package_name)).stdout.read()

        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return pattern.findall(" ".join(result))[0]

    def kill_process(self, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if self.shell("kill %s" %
                              str(pid)).stdout.read().split(": ")[-1] == "":
            return "kill success"
        else:
            return self.shell("kill %s" %
                              str(pid)).stdout.read().split(": ")[-1]

    def quit_app(self, package_name):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.android.settings")
        """
        self.shell("am force-stop %s" % package_name)

    # def get_focused_package_and_activity(self):
    #     """
    #     获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
    #     """
    #     pattern = re.compile(r"[a-zA-Z0-9.]+/.[a-zA-Z0-9.]+")
    #     out = self.shell(
    #         "dumpsys window w | %s \/ | %s name=" %
    #         (find_util, find_util)).stdout.read().strip()
    #
    #     return pattern.findall(out)[0]

    def get_focused_package_and_activity(self):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        out = self.shell(
            "dumpsys activity activities | %s mFocusedActivity" %
            find_util).stdout.read().strip().split(' ')[3]
        return out

    def get_current_package_name(self):
        """
        获取当前运行的应用的包名
        """
        return self.get_focused_package_and_activity().split("/")[0]

    def get_current_activity(self):
        """
        获取当前运行应用的activity
        """
        return self.get_focused_package_and_activity().split("/")[-1]

    def get_battery_level(self):
        """
        获取电池电量
        """
        level = self.shell("dumpsys battery | %s level" %
                           find_util).stdout.read().split(": ")[-1]

        return int(level)

    def get_backstage_services(self, page_name):
        """

        :return: 指定应用后台运行的services
        """
        services_list = []
        for line in self.shell(
                        'dumpsys activity services %s' %
                        page_name).stdout.readlines():
            if line.strip().startswith('intent'):
                service_name = line.strip().split('=')[-1].split('}')[0]
                if service_name not in services_list:
                    services_list.append(service_name)

        return services_list

    def get_current_backstage_services(self):
        """

        :return: 当前应用后台运行的services
        """
        package = self.get_current_package_name()
        return self.get_backstage_services(package)

    def get_battery_status(self):
        """
        获取电池充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        """
        status_dict = {1: "BATTERY_STATUS_UNKNOWN",
                       2: "BATTERY_STATUS_CHARGING",
                       3: "BATTERY_STATUS_DISCHARGING",
                       4: "BATTERY_STATUS_NOT_CHARGING",
                       5: "BATTERY_STATUS_FULL"}
        status = self.shell("dumpsys battery | %s status" %
                            find_util).stdout.read().split(": ")[-1]

        return status_dict[int(status)]

    def get_battery_temp(self):
        """
        获取电池温度
        """
        temp = self.shell("dumpsys battery | %s temperature" %
                          find_util).stdout.read().split(": ")[-1]

        return int(temp) / 10.0

    def get_screen_resolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        pattern = re.compile(r"\d+")
        out = self.shell(
            "dumpsys display | %s DisplayDeviceInfo" %
            find_util).stdout.read()
        display = pattern.findall(out)

        return int(display[0]), int(display[1])

    def reboot(self):
        """
        重启设备
        """
        self.adb("reboot")

    def fast_boot(self):
        """
        进入fastboot模式
        """
        self.adb("reboot bootloader")

    def get_system_app_list(self):
        """
        获取设备中安装的系统应用包名列表
        """
        sysApp = []
        for packages in self.shell("pm list packages -s").stdout.readlines():
            sysApp.append(packages.split(":")[-1].splitlines()[0])

        return sysApp

    def get_third_app_list(self):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdApp = []
        for packages in self.shell("pm list packages -3").stdout.readlines():
            thirdApp.append(packages.split(":")[-1].splitlines()[0])

        return thirdApp

    def get_matching_app_list(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.shell(
                        "pm list packages %s" %
                        keyword).stdout.readlines():
            matApp.append(packages.split(":")[-1].splitlines()[0])

        return matApp

    def get_app_start_total_time(self, component):
        """
        获取启动应用所花时间
        usage: getAppStartTotalTime("com.android.settings/.Settings")
        """
        time = self.shell("am start -W %s | %s TotalTime" %
                          (component, find_util)).stdout.read().split(": ")[-1]
        return int(time)

    def install_app(self, app_file):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("/Users/joko/Downloads/1.apk")
        INSTALL_FAILED_ALREADY_EXISTS	应用已经存在，或卸载了但没卸载干净	adb install 时使用 -r 参数，或者先 adb uninstall <packagename> 再安装
        INSTALL_FAILED_INVALID_APK	无效的 APK 文件
        INSTALL_FAILED_INVALID_URI	无效的 APK 文件名	确保 APK 文件名里无中文
        INSTALL_FAILED_INSUFFICIENT_STORAGE	空间不足	清理空间
        INSTALL_FAILED_DUPLICATE_PACKAGE	已经存在同名程序
        INSTALL_FAILED_NO_SHARED_USER	请求的共享用户不存在
        INSTALL_FAILED_UPDATE_INCOMPATIBLE	以前安装过同名应用，但卸载时数据没有移除	先 adb uninstall <packagename> 再安装
        INSTALL_FAILED_SHARED_USER_INCOMPATIBLE	请求的共享用户存在但签名不一致
        INSTALL_FAILED_MISSING_SHARED_LIBRARY	安装包使用了设备上不可用的共享库
        INSTALL_FAILED_REPLACE_COULDNT_DELETE	替换时无法删除
        INSTALL_FAILED_DEXOPT	dex 优化验证失败或空间不足
        INSTALL_FAILED_OLDER_SDK	设备系统版本低于应用要求
        INSTALL_FAILED_CONFLICTING_PROVIDER	设备里已经存在与应用里同名的 content provider
        INSTALL_FAILED_NEWER_SDK	设备系统版本高于应用要求
        INSTALL_FAILED_TEST_ONLY	应用是 test-only 的，但安装时没有指定 -t 参数
        INSTALL_FAILED_CPU_ABI_INCOMPATIBLE	包含不兼容设备 CPU 应用程序二进制接口的 native code
        INSTALL_FAILED_MISSING_FEATURE	应用使用了设备不可用的功能
        INSTALL_FAILED_CONTAINER_ERROR	sdcard 访问失败	确认 sdcard 可用，或者安装到内置存储
        INSTALL_FAILED_INVALID_INSTALL_LOCATION	不能安装到指定位置	切换安装位置，添加或删除 -s 参数
        INSTALL_FAILED_MEDIA_UNAVAILABLE	安装位置不可用	一般为 sdcard，确认 sdcard 可用或安装到内置存储
        INSTALL_FAILED_VERIFICATION_TIMEOUT	验证安装包超时
        INSTALL_FAILED_VERIFICATION_FAILURE	验证安装包失败
        INSTALL_FAILED_PACKAGE_CHANGED	应用与调用程序期望的不一致
        INSTALL_FAILED_UID_CHANGED	以前安装过该应用，与本次分配的 UID 不一致	清除以前安装过的残留文件
        INSTALL_FAILED_VERSION_DOWNGRADE	已经安装了该应用更高版本	使用 -d 参数
        INSTALL_FAILED_PERMISSION_MODEL_DOWNGRADE	已安装 target SDK 支持运行时权限的同名应用，要安装的版本不支持运行时权限
        INSTALL_PARSE_FAILED_NOT_APK	指定路径不是文件，或不是以 .apk 结尾
        INSTALL_PARSE_FAILED_BAD_MANIFEST	无法解析的 AndroidManifest.xml 文件
        INSTALL_PARSE_FAILED_UNEXPECTED_EXCEPTION	解析器遇到异常
        INSTALL_PARSE_FAILED_NO_CERTIFICATES	安装包没有签名
        INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES	已安装该应用，且签名与 APK 文件不一致	先卸载设备上的该应用，再安装
        INSTALL_PARSE_FAILED_CERTIFICATE_ENCODING	解析 APK 文件时遇到 CertificateEncodingException
        INSTALL_PARSE_FAILED_BAD_PACKAGE_NAME	manifest 文件里没有或者使用了无效的包名
        INSTALL_PARSE_FAILED_BAD_SHARED_USER_ID	manifest 文件里指定了无效的共享用户 ID
        INSTALL_PARSE_FAILED_MANIFEST_MALFORMED	解析 manifest 文件时遇到结构性错误
        INSTALL_PARSE_FAILED_MANIFEST_EMPTY	在 manifest 文件里找不到找可操作标签（instrumentation 或 application）
        INSTALL_FAILED_INTERNAL_ERROR	因系统问题安装失败
        INSTALL_FAILED_USER_RESTRICTED	用户被限制安装应用
        INSTALL_FAILED_DUPLICATE_PERMISSION	应用尝试定义一个已经存在的权限名称
        INSTALL_FAILED_NO_MATCHING_ABIS	应用包含设备的应用程序二进制接口不支持的 native code
        INSTALL_CANCELED_BY_USER	应用安装需要在设备上确认，但未操作设备或点了取消	在设备上同意安装
        INSTALL_FAILED_ACWF_INCOMPATIBLE	应用程序与设备不兼容
        does not contain AndroidManifest.xml	无效的 APK 文件
        is not a valid zip file	无效的 APK 文件
        Offline	设备未连接成功	先将设备与 adb 连接成功
        unauthorized	设备未授权允许调试
        error: device not found	没有连接成功的设备	先将设备与 adb 连接成功
        protocol failure	设备已断开连接	先将设备与 adb 连接成功
        Unknown option: -s	Android 2.2 以下不支持安装到 sdcard	不使用 -s 参数
        No space left on devicerm	空间不足	清理空间
        Permission denied ... sdcard ...	sdcard 不可用
        """
        # for line in self.adb("install -r %s" % app_file).stdout.readlines():
        #     if 'Failure' in line:
        #         print line.strip()
        return self.adb("install -r %s" % app_file)

    def is_install(self, packageName):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.example.apidemo")
        """
        if self.get_matching_app_list(packageName):
            return True
        else:
            return False

    def remove_app(self, packageName):
        """
        卸载应用
        args:
        - packageName -:应用包名，非apk名
        """
        return self.adb("uninstall %s" % packageName)

    def clear_app_data(self, packageName):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.shell(
                        "pm clear %s" %
                        packageName).stdout.read().splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def reset_current_app(self):
        """
        重置当前应用
        """
        packageName = self.get_current_package_name()
        component = self.get_focused_package_and_activity()
        self.clear_app_data(packageName)
        self.start_activity(component)

    def get_app_install_path(self, path_name):
        """
        获取第三方应用安装地址
        :return:
        """
        t = self.shell("pm path %s" % path_name).stdout.readlines()
        return ''.join(t).strip().split(':')[1]

    def pull_install_app(self, save_path):
        """
        获取当前Android设备第三方应用包，并且pull到本地
        :param save_path: 存放路径
        :return:
        """
        for app_package_name in self.get_third_app_list():
            install_app_path = self.get_app_install_path(app_package_name)
            self.pull(install_app_path, save_path + '/' + app_package_name + '.apk')

    def start_activity(self, component):
        """
        启动一个Activity
        usage: startActivity(component = "com.android.settinrs/.Settings")
        """
        self.shell("am start -n %s" % component)

    def start_web_page(self, url):
        """
        使用系统默认浏览器打开一个网页
        usage: startWebpage("http://www.baidu.com")
        """
        self.shell("am start -a android.intent.action.VIEW -d %s" % url)

    def call_phone(self, number):
        """
        启动拨号器拨打电话
        usage: callPhone(10086)
        """
        self.shell(
            "am start -a android.intent.action.CALL -d tel:%s" %
            str(number))

    def send_key_event(self, keycode):
        """
        发送一个按键事件
        args:
        - keycode -:
        http://developer.android.com/reference/android/view/KeyEvent.html
        usage: sendKeyEvent(keycode.HOME)
        """
        self.shell("input keyevent %s" % str(keycode))
        sleep(0.5)

    def long_press_key(self, keycode):
        """
        发送一个按键长按事件，Android 4.4以上
        usage: longPressKey(keycode.HOME)
        """
        self.shell("input keyevent --longpress %s" % str(keycode))
        sleep(0.5)

    def touch(self, e=None, x=None, y=None):
        """
        触摸事件
        usage: touch(e), touch(x=0.5,y=0.5)
        """
        width, high = self.get_screen_resolution()
        if (e is not None):
            x = e[0]
            y = e[1]
        if (0 < x < 1):
            x = x * width
        if (0 < y < 1):
            y = y * high

        self.shell("input tap %s %s" % (str(x), str(y)))
        sleep(0.5)

    def get_focused_package_xml(self, save_path):
        file_name = random.randint(10, 99)
        self.shell(
            'uiautomator dump /data/local/tmp/{}.xml'.format(file_name)).communicate()
        self.adb('pull /data/local/tmp/{}.xml {}'.format(file_name,
                                                         save_path)).communicate()

    def touch_by_element(self, element):
        """
        点击元素
        usage: touchByElement(Element().findElementByName(u"计算器"))
        """
        self.shell("input tap %s %s" % (str(element[0]), str(element[1])))
        sleep(0.5)

    def touch_by_ratio(self, ratioWidth, ratioHigh):
        """
        通过比例发送触摸事件
        args:
        - ratioWidth -:width占比, 0<ratioWidth<1
        - ratioHigh -: high占比, 0<ratioHigh<1
        usage: touchByRatio(0.5, 0.5) 点击屏幕中心位置
        """
        self.shell("input tap %s %s" %
                   (str(ratioWidth *
                        self.get_screen_resolution[0]), str(ratioHigh *
                                                            self.get_screen_resolution[1])))
        sleep(0.5)

    def swipe_by_coord(self, start_x, start_y, end_x, end_y, duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(800, 500, 200, 500)
        """
        self.shell(
            "input swipe %s %s %s %s %s" %
            (str(start_x),
             str(start_y),
             str(end_x),
             str(end_y),
             str(duration)))
        sleep(0.5)

    def swipe(
            self,
            e1=None,
            e2=None,
            start_x=None,
            start_y=None,
            end_x=None,
            end_y=None,
            duration=" "):
        """
        滑动事件，Android 4.4以上可选duration(ms)
        usage: swipe(e1, e2)
               swipe(e1, end_x=200, end_y=500)
               swipe(start_x=0.5, start_y=0.5, e2)
        """
        width, high = self.get_screen_resolution()
        if (e1 is not None):
            start_x = e1[0]
            start_y = e1[1]
        if (e2 is not None):
            end_x = e2[0]
            end_y = e2[1]
        if (0 < start_x < 1):
            start_x = start_x * width
        if (0 < start_y < 1):
            start_y = start_y * high
        if (0 < end_x < 1):
            end_x = end_x * width
        if (0 < end_y < 1):
            end_y = end_y * high

        self.shell(
            "input swipe %s %s %s %s %s" %
            (str(start_x),
             str(start_y),
             str(end_x),
             str(end_y),
             str(duration)))
        sleep(0.5)

    def swipe_by_ratio(
            self,
            start_ratioWidth,
            start_ratioHigh,
            end_ratioWidth,
            end_ratioHigh,
            duration=" "):
        """
        通过比例发送滑动事件，Android 4.4以上可选duration(ms)
        usage: swipeByRatio(0.9, 0.5, 0.1, 0.5) 左滑
        """
        x_point, y_point = self.get_screen_resolution()
        self.shell("input swipe %s %s %s %s %s" %
                   (str(start_ratioWidth *
                        x_point), str(start_ratioHigh *
                                      y_point), str(end_ratioWidth *
                                                    x_point), str(end_ratioHigh *
                                                                  y_point), str(duration)))
        sleep(0.5)

    def swipe_to_left(self):
        """
        左滑屏幕
        """
        self.swipe_by_ratio(0.8, 0.5, 0.2, 0.5)

    def swipe_to_right(self):
        """
        右滑屏幕
        """
        self.swipe_by_ratio(0.2, 0.5, 0.8, 0.5)

    def swipe_to_up(self):
        """
        上滑屏幕
        """
        self.swipe_by_ratio(0.5, 0.8, 0.5, 0.2)

    def swipe_to_down(self):
        """
        下滑屏幕
        """
        self.swipe_by_ratio(0.5, 0.2, 0.5, 0.8)

    def long_press(self, e=None, x=None, y=None):
        """
        长按屏幕的某个坐标位置, Android 4.4
        usage: longPress(e)
               longPress(x=0.5, y=0.5)
        """
        self.swipe(
            e1=e,
            e2=e,
            start_x=x,
            start_y=y,
            end_x=x,
            end_y=y,
            duration=2000)

    def long_press_element(self, e):
        """
       长按元素, Android 4.4
        """
        self.shell(
            "input swipe %s %s %s %s %s" %
            (str(
                e[0]), str(
                e[1]), str(
                e[0]), str(
                e[1]), str(2000)))
        sleep(0.5)

    def long_press_by_ratio(self, ratio_width, ratio_high):
        """
        通过比例长按屏幕某个位置, Android.4.4
        usage: longPressByRatio(0.5, 0.5) 长按屏幕中心位置
        """
        self.swipe_by_ratio(
            ratio_width,
            ratio_high,
            ratio_width,
            ratio_high,
            duration=2000)

    def send_text(self, string):
        """
        发送一段文本，只能包含英文字符和空格，多个空格视为一个空格
        usage: sendText("i am unique")
        """
        text = str(string).split(" ")
        out = []
        for i in text:
            if i != "":
                out.append(i)
        length = len(out)
        for i in xrange(length):
            self.shell("input text %s" % out[i])
            # if i != length - 1:
            #     self.sendKeyEvent(keycode.SPACE)
        sleep(0.5)

    def screen_shot(self, appPath):
        """
        获取当前设备的截图,导出到指定目录
        """
        self.shell("/system/bin/screencap -p /sdcard/temp.png")
        time.sleep(3)
        self.adb("pull /sdcard/temp.png %s" % appPath)

    def version_name(self):
        """
        查询当前屏幕应用版本
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'versionName' in package:
                return package.split('=', 2)[1].strip()

    def specifies_app_version_name(self, package):
        """
        获取指定应用的versionName
        :param package:应用包名
        :return: 包名,versionName
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        package).stdout.readlines():
            if 'versionName' in package:
                return package.split('=', 2)[1].strip()

    def version_code(self):
        """
        查询当前屏幕应用versionCode
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'versionCode' in package:
                return package.split('=', 2)[1].split(' ', 2)[0]

    def first_install_time(self):
        """
        查询当前屏幕应用安装时间
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'firstInstallTime' in package:
                return package.split('=', 2)[1].strip()

    def last_update_time(self):
        """
        查询当前屏幕应用安装更新时间
        """
        for package in self.shell(
                        'dumpsys package %s' %
                        self.get_current_package_name()).stdout.readlines():
            if 'lastUpdateTime' in package:
                return package.split('=', 2)[1].strip()

    def wifi_name(self):
        """
        查询连接wifi名称
        """
        for package in self.shell('dumpsys wifi').stdout.readlines():
            if package.startswith('mWifiInfo'):
                wifi_name = re.findall(r'SSID:([^"]+), BSSID', package)
                if not wifi_name:
                    return None
                else:
                    return wifi_name[0].strip()

    def get_network_state(self):
        """
        设备是否连上互联网
        :return:
        """
        if 'unknown' in self.shell('ping -w 1 www.baidu.com').stdout.readlines()[0]:
            return False
        else:
            return True

    def get_cpu(self, package_name):
        """
        获取当前cpu百分比
        """
        p = self.shell(
            'top -n 1 -d 0.5 | %s %s' %
            (find_util, package_name))
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r.endswith(package_name):
                lst = [cpu for cpu in r.split(' ') if cpu]
                return int(lst[2].split('%', 1)[0])

    def __mem_pss(self, package_name):
        """
        获取当前应用内存
        """
        p = self.shell(
            'top -n 1 -d 0.5 | %s %s' %
            (find_util, package_name))
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r.endswith(package_name):
                lst = [mem for mem in r.split(' ') if mem]
                return int(lst[6].split('K')[0])

    def __mem_mem_total(self):
        p = self.shell('cat proc/meminfo')
        while True:
            r = p.stdout.readline().strip().decode('utf-8')
            if r and 'MemTotal' in r:
                lst = [MemTotal for MemTotal in r.split(' ') if MemTotal]
                return int(lst[1])

    def get_mem(self, package_name):
        """
        获取当前内存百分比
        """
        try:
            return int(
                self.__mem_pss(package_name) /
                float(
                    self.__mem_mem_total()) *
                100)
        except:
            return None

    def fill_disk(self):
        """
        填满手机磁盘，需root
        """
        self.shell('dd if=/dev/zero of=/mnt/sdcard/bigfile')

    def del_fill_disk(self):
        """
        删除填满磁盘的大文件
        """
        self.shell('rm -r /mnt/sdcard/bigfile')

    def backup_apk(self, package_name, path):
        """
        备份应用与数据
        - all 备份所有
        -f 指定路径
        -system|-nosystem
        -shared 备份sd卡
        """
        self.adb(
            'backup -apk %s -f %s/mybackup.ab' %
            (package_name, path))

    def restore_apk(self, path):
        """
        恢复应用与数据
        - all 备份所有
        -f 指定路径
        -system|-nosystem
        """
        self.adb('restore %s' % path)

    def c_logcat(self):
        """

        :return: 清理缓存中的log
        """
        return self.adb('logcat -c')

    def logcat(self, log_path):
        return self.adb('logcat -v time > %s&' % (log_path))

    def get_cpu_version(self):
        """
        获取cpu基带版本
        :return: arm64-v8a
        """
        t = self.shell(
            "getprop ro.product.cpu.abi | tr -d '\r'").stdout.readlines()
        return ''.join(t).strip()

    def pull(self, remote_file, local_file):
        """

        :param remote_file: 拉取文件地址
        :param local_file: 存放文件地址
        :return:
        """
        return self.adb('pull %s %s' % (remote_file, local_file))

    def rm(self, remote_file):
        """

        :param remote_file: 删除文件地址
        :return:
        """
        return self.shell(remote_file)

    def rm_minicap_jpg(self, remote_file):
        """

        :param remote_file: 删除minicap图片缓存
        :return:
        """
        self.rm('rm -r /data/local/tmp/%s.jpg' % (remote_file))

    def get_disk(self):
        """
        获取手机磁盘信息
        :return: Used:用户占用,Free:剩余空间
        """
        for s in self.shell('df').stdout.readlines():
            if '/mnt/shell/emulated' in s or '/storage/sdcard0' in s:
                lst = []
                for i in s.split(' '):
                    if i:
                        lst.append(i)
                return 'Used:%s,Free:%s' % (lst[2], lst[3])

    def get_dmesg(self):
        """

        :return:内核日志
        """
        t = self.shell("dmesg").stdout.readlines()
        return ''.join(t).strip()

    def get_device_name(self):
        """

        :return: 设备名 :SM-G9006W
        """
        t = self.shell("getprop ro.product.model").stdout.readlines()
        return ''.join(t).strip()

    def get_battery(self):
        """

        :return:全部电量相关信息
        """
        t = self.shell("dumpsys battery").stdout.readlines()
        return ''.join(t).strip()

    def get_wm_density(self):
        """
        屏幕密度
        :return:Physical density: 480
        """
        t = self.shell("wm density").stdout.readlines()
        return ''.join(t).strip()

    def get_window_displays(self):
        """

        :return:显示屏参数
        """
        t = self.shell("dumpsys window displays").stdout.readlines()
        return ''.join(t).strip()

    def get_mac_address(self):
        """

        :return:mac地址
        """
        t = self.shell("cat /sys/class/net/wlan0/address").stdout.readlines()
        return ''.join(t).strip()

    def get_cpu_info_all(self):
        """

        :return:cpu全部信息
        """
        t = self.shell("cat /proc/cpuinfo").stdout.readlines()
        return ''.join(t).strip()

    def get_cpu_mem_all(self):
        """

        :return:内存全部信息
        """
        t = self.shell("cat /proc/meminfo").stdout.readlines()
        return ''.join(t).strip()

    def get_sys_all(self):
        """

        :return:设备全部信息
        """
        t = self.shell("cat /system/build.prop").stdout.readlines()
        return ''.join(t).strip()

    def get_ps(self):
        """

        :return:设备全部进程信息
        """
        t = self.shell("ps").stdout.readlines()
        return ''.join(t).strip()

    def get_cpu_mem_info(self):
        """

        :return:当前设备cpu与内存全部信息
        """
        t = self.shell("top -n 1 -d 0.5").stdout.readlines()
        return ''.join(t).strip()

    def get_phone_ime(self):
        """

        :return:获取设备已安装的输入法包名
        """
        ime_list = [ime.strip() for ime in self.shell("ime list -s").stdout.readlines()]
        return ime_list

    def set_phone_ime(self, arg):
        """

        :return: 更改手机输入法
        """
        self.shell("ime set %s" % arg)


if __name__ == "__main__":
    A = ADB()
    print A.get_focused_package_and_activity()
