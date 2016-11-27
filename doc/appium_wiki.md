## appium文档

* 官网中文文档:[点我](http://appium.io/slate/cn/v1.6.0/?python#)

* 开源地址:[点我](https://github.com/appium/appium)

### 安装方法

* 1: npm install -g cnpm --registry=https://registry.npm.taobao.org

* 2: cnpm install -g appium --no-cache

### 注销安装unlock setting

* 取消安装unlock和setting
路径:/Users/joko/appium/node_modules/appium-android-driver/lib/android-helpers.js
  // await helpers.pushSettingsApp(adb);
  // await helpers.pushUnlock(adb);
