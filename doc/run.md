## Auto_Analysis配置文档

#### 安装node

[官网地址](https://nodejs.org/en/download/)

* OS:brew install node
* windows,linux参照官网

#### 安装appium

* 1: npm install -g cnpm --registry=https://registry.npm.taobao.org

* 2: cnpm install -g appium --no-cache

### python

方法请自行查找

### 运行

* git 源码
* cd Auto_Analysis
* python setup.py install
* python run.py

注:性能图片生成用到了matplotlib,如果setup未安装成功

* Linux:sudo apt-get install python-matplotlib

### 参数配置

* 参见:parameter_configuration文档

### 用例编写

* 参见test_case_writing文档

### 测试报告

* 参见test_report文档

### 其他

* appium:appium_wiki文档

* 控件查找:controls_operations文档

* 如果想单线程运行,请运行:po.integration