## 控件查找方法

### id查找方式
* 利用Android sdk 自带的uiautomatorviewer工具

### xpath的查找方式

(资料)[http://www.cnblogs.com/paulwinflo/p/4738904.html]

* 根据文字的属性查找

//android.widget.TextView[contains(@text,'19')]

* 根据控件的index数组下标查找

//android.widget.TextView[contains(@index,0)]

* 根据相对路径来查找,从明显的分界来查找

//android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[contains(@index,0)]