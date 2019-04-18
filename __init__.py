"""
Log.py
    日志
    记录日志调用 LoggerSingleton.instance() 进行统一操作
    文件等级为 warning 以上

Setting.py
    配置文件读取
    默认配置设置
    logo读取

BrowserSingleton.py
    浏览器实例
    推荐使用-->chrome 需要匹配内核的 chromedriver
    可以配置 chrome firefox 或 基于 chromium 内核的浏览器
    默认为chrome (推荐)
    firefox 需要修改配置文件进行一些设置
    基于 chromium 内核的浏览器 需手动修改并配置内核型号（未测试 不推荐）

BrowserOperate.py
    对浏览器操作方法的封装
    该模块中全部为 @staticmethod, @staticmethod
    不需要生成该类实例

ExcelOperate.py
    对Excel的读取和信息筛选
    后期想完全解耦合可重构为类似BrowserOperate形式

EntryWindow.ui
    UI文件
    使用 PyUIC 生成 基于python的界面
    使用 qtDesigner 编辑

EntryWindow.py
    UI 文件生成的代码

MainWindow.py
    主窗口
    包含窗口控件进行操作
    控制Excel读取和向浏览器填充
    三个线程独立处理复杂操作 避免主窗口无法响应

GradeEntryProgram.py
    程序入口

"""
