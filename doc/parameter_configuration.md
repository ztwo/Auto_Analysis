## 执行的参数配置


* 配置 data/test_info.ini ,

```ini

[test_package_name]
# 应用包名
package_name = com.x.x.x

[test_install_path]
* 被测试应用地址
path = /Users/joko/Auto_Analysis/data/app.apk

[test_device]
* device信息存放地址
device = /Users/joko/Auto_Analysis/data/incidental/device_info.yaml

[test_case]
* 测试case存放地址
case = /Users/joko/Auto_Analysis/testcase
* 测试报告存放地址
log_file = /Users/joko/Auto_Analysis/result
* 错误图片展示地址
error_img = /Users/joko/Auto_Analysis/data/incidental/error.png

[minicap]
* minicap地址:用于截图
minicap_path = /Users/joko/Auto_Analysis/data/minicap/bin/{}/minicap
minitouch_path = /Users/joko/Auto_Analysis/data/minicap/minitouch/{}/minitouch
minicapso_path = /Users/joko/Auto_Analysis/data/minicap/shared/android-{}/{}/minicap.so

[test_db]
* 存放测试记录的db地址
test_result = /Users/joko/Auto_Analysis/data/incidental/test.db

```

注:windows路径也如此相同写法:d:/file/1.x

* 配置 data/appium_parameter.yaml

```yaml
---
-
 appPackage: 应用包名
 appActivity: 启动Activity名
 appWaitActivity: 等待的Activity名
 unicodeKeyboard: True
 resetKeyboard: True
 resetKeyboard: True
 noReset: False
```
