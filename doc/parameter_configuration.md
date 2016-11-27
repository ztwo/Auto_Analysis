## 执行的参数配置


* 配置 data/test_info.ini

```ini

[test_package_name]
package_name = com.x.x.x
#（应用报名）


[test_info]
info = /Users/joko/Documents/Auto_Analysis/data/appium_parameter.yaml

[test_install_path]
path = 应用安装地址

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
