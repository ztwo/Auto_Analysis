## Auto_Analysis

### 简介
Auto_Analysis是基于appium编写的自动化测试工具。使用方法简单，编写yaml文件格式的测试用例即可。支持Android，多台设备并行，性能采集等。

### 环境要求

* macOS，linux，windows
* appium 1.5.0+
* python 2.7 

### 工具特性

执行编写yaml格式的testcase，执行后即可得到测试报告

* 1：支持Android 4.2.2 以上
* 2：支持多设备并行测试
* 3：性能采集与对比
* 4：支持log采集与清洗
* 5：对appium异常的一些封装
* 6：用例编写支持继承多重继承，大部分用例仅需写两个步骤即可

### 快速开始

* git clone https://github.com/ztwo/Auto_Analysis.git
* cd Auto_Analysis
* python setup.py install
* python demo_run.py
* result内查看测试报告

### 执行效果
![12](http://7xwbkf.com1.z0.glb.clouddn.com/2016-11-11%2017.22.53.gif)

### 报告样式 
![20161123810772016-11-23pm.png](http://7xwbkf.com1.z0.glb.clouddn.com/20161123810772016-11-23pm.png)
