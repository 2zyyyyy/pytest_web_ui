# -*- coding: utf-8 -*-

# 通用配置
CASE_TYPE = 'web'  # 项目类型  'app'  # web

IS_CLEAN_REPORT = True  # 是否清除 测试历史测试报告结果 * 默认清除

# selenium/appium配置
IMPLICITLY_WAIT_TIME = 10  # 显示等待最长时间 /s

POLL_FREQUENCY = 0.2  # 显示等待元素出现时 在此时间内检索一次 /s

# Web端配置
URL = "https://www.baidu.com/"  # # 项目地址 web 时选择

BROWSER_NAME = "Chrome"  # "Chrome" "Firefox" "Ie"  "Safari"  # 浏览器选择

# db配置
MYSQL = {'user': 'root', 'password': 'root', 'port': 3306, 'host': '127.0.0.1', 'db': 'test'}

