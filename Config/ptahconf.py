# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Linux 系统浏览器驱动路劲
LINUX_CHROME = os.path.join(BASE_DIR, "driver", "linux", "chromedriver")  # 谷歌浏览器
LINUX_FIREFOX = os.path.join(BASE_DIR, "driver", "linux", "geckodriver")  # 火狐浏览器

# Windows 系统浏览器驱动路劲
IE_PATH = os.path.join(BASE_DIR, "driver", "windows", "IEDriverServer.exe")  # ie浏览器
WIN_CHROME = os.path.join(BASE_DIR, "driver", "windows", "chromedriver.exe")  # 谷歌浏览器
WIN_FIREFOX = os.path.join(BASE_DIR, "driver", "windows", "geckodriver.exe")  # 火狐浏览器

# Mac 系统浏览器驱动路劲
MAC_CHROME = os.path.join(BASE_DIR, "driver", "mac", "chromedriver")  # 谷歌浏览器
MAC_FIREFOX = os.path.join(BASE_DIR, "driver", "mac", "geckodriver")  # 火狐浏览器

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "log")

# 测试用例集路径

CASE_DIR = os.path.join(BASE_DIR, "case", )

# yaml测试用列数据路径
TESTCASE_DIR = os.path.join(BASE_DIR, "database", "caseYAML", )  # 测试数据
LOCATOR_DIR = os.path.join(BASE_DIR, "database", "locatorYAML", )  # 定位数据

# 测试文件路径
DATA_FILE = os.path.join(BASE_DIR, "database", "file")

# 测试用例结果目录
REPORT_JSON_DIR = os.path.join(BASE_DIR, "output", "report_json")

# 测试结果报告目录
REPORT_ALLURE_DIR = os.path.join(BASE_DIR, "output", "report_allure")

# 测试截图目录
SCREENSHOT_DIR = os.path.join(BASE_DIR, "output", "report_screen")
