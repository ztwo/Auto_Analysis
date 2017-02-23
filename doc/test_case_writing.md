## 测试用例编写规范

* 1: 需要了解yaml格式编写规范,建议使用pycharm编写,自带yaml文档检查器.
[yaml语法学习地址](http://www.ruanyifeng.com/blog/2016/07/yaml.html)
* 2: 用例名不可重复,会影响用例的继承

## 测试用例字段解释


| 字段                | 解释         | 演示        | 包含字段      | 是否必须 |
| ----------------- | ---------- | --------- | --------- | ---- |
| test_name         | 用例名        | login     | /         | 是    |
| test_id           | 用例id       | 0001      | /         | 否    |
| test_control_type | 查找控件方式     | xapth     | xpath, id | 否    |
| test_action       | 操作方法       | click     | 见下表       | 是    |
| test_control      | 控件         | com.xx.id | /         | 否    |
| test_text         | 断言、输入文本    | test      | /         | 否    |
| test_inherit      | 继承用例名      | login     | /         | 否    |
| test_range        | 循环本步骤次数    | 2         | /         | 否    |
| test_sleep        | 步骤执行后，等待秒  | 2         | /         | 否    |
| test_wait         | 配合断言，等待控件秒 | 30        | /         | 否    |


| test_action | 解释   | 所有字段                                     | 配合字段                                     | 辅助配合字段    |
| ----------- | ---- | ---------------------------------------- | ---------------------------------------- | --------- |
| click       | 点击   | click                                    | test_control_type，test_control           | /         |
| send_keys   | 发送文本 | send_keys                                | test_control_type，test_control，test_text | /         |
| swipe       | 滑动   | swipe_left,swipe_right,swipe_up,swipe_down | /                                        | /         |
| assert      | 断言   | assert                                   | test_control_type，test_control，test_text | test_wait |
| entity      | 实体按键 | entity_home，entity_back，entity_menu，entity_volume_up，entity_volume_down,entity_enter | /                                        | /         |

## 完整用例范例,用例名:login

```yaml
---
-
  test_name: 点击跳过
  test_id: 0001
  test_control_type: id
  test_action: click
  test_control: test.joko.com.myapplication:id/button1
-
  test_name: 输入帐号名
  test_id: 0002
  test_control_type: id
  test_action: send_keys
  test_control: test.joko.com.myapplication:id/editText
  test_text: 199999999
-
  test_name: 输入密码
  test_id: 0003
  test_control_type: id
  test_action: send_keys
  test_control: test.joko.com.myapplication:id/editText2
  test_text: 9999

-
  test_name: 点击登录
  test_id: 0004
  test_control_type: xpath
  test_action: click
  test_control: //android.widget.Button[contains(@text,'确定')]

-
  test_name: 向上滑动页面
  test_id: 0005
  test_action: swipe_up
  test_range: 3

-
  test_name: 向下滑动页面
  test_id: 0005
  test_action: swipe_down
  test_range: 3

```