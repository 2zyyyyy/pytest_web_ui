# -*- coding: utf-8 -*-

import sys
import os
import time
import requests
from Public.common import ErrorCustom
from selenium import webdriver
from Public.logs import logger
from Config.ptahconf import IE_PATH
from Config.ptahconf import LOG_DIR
from Config.setting import BROWSER_NAME
from Config.setting import URL
from Config.ptahconf import LINUX_CHROME, LINUX_FIREFOX, MAC_CHROME, MAC_FIREFOX, WIN_CHROME, WIN_FIREFOX

sys.path.append('../')
DAY = time.strftime("%Y-%m-%d", time.localtime(time.time()))


class WebInit:
    """
    返回浏览器驱动
    """

    def __init__(self):
        self.browser = BROWSER_NAME.lower()
        self.baseurl = URL

    @staticmethod
    def inspect_url_code(url):
        """
        判断url 地址正常请求
        """
        try:
            rep = requests.get(url, timeout=5)  # 默认设置5秒超时
            code = rep.status_code
            if code == 200:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f'请求地址异常{e}！！')

    @property
    def url(self):
        return self.baseurl

    @url.setter
    def url(self, value):
        self.baseurl = value

    @property
    def linux_firefox_args(self):
        """
        linux os firefox browser parameter  只能在 linux 调试
        :return:
        """
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=1200x600')
        return options

    @property
    def linux_chrome_args(self):
        """
        linux os chrome browser parameter
        :return:
        """
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')  # 取消沙盒模式
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        option.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        return option

    @property
    def enable(self):
        return self.setup()

    def browser_setup_args(self, driver):
        """
        单机浏览器参数设置
        :param driver: driver驱动浏览器
        :return:
        """
        driver.maximize_window()
        driver.get(self.url)
        return driver

    def setup(self):
        """
        设置单机版 浏览器驱动
        :return:
        """
        # 判断当前系统
        try:
            if self.inspect_url_code(self.url):  # 如果项目地址正常
                current_sys = sys.platform.lower()
                log_path = os.path.join(LOG_DIR, f'{DAY}firefox.log')

                if current_sys == 'linux':  # linux系统

                    if self.browser == 'chrome':  # 谷歌浏览器
                        option = self.linux_chrome_args
                        driver = webdriver.Chrome(executable_path=LINUX_CHROME, options=option)
                        return self.browser_setup_args(driver)

                    elif self.browser == 'firefox':  # 火狐浏览器
                        options = self.linux_firefox_args
                        driver = webdriver.Firefox(executable_path=LINUX_FIREFOX, options=options,
                                                   service_log_path=log_path)
                        drivers = self.browser_setup_args(driver)
                        return drivers  # 在linux下启用 火狐浏览器需要借助Display

                    else:
                        raise ErrorCustom(f'linux系统不支持此浏览器: {self.browser}')

                elif current_sys == 'darwin':  # mac 系统

                    if self.browser == 'chrome':
                        driver = webdriver.Chrome(executable_path=MAC_CHROME)
                        return self.browser_setup_args(driver)

                    elif self.browser == 'firefox':
                        driver = webdriver.Firefox(executable_path=MAC_FIREFOX, service_log_path=log_path)
                        return self.browser_setup_args(driver)

                    elif self.browser == 'safari':
                        driver = webdriver.Safari()
                        return self.browser_setup_args(driver)

                    else:
                        raise ErrorCustom(f'mac系统不支持此浏览器: {self.browser}')

                elif current_sys == 'win32':

                    if self.browser == 'ie':
                        logger.warning('请确保当前服务器安装IE!')
                        driver = webdriver.Ie(executable_path=IE_PATH)
                        return self.browser_setup_args(driver)

                    if self.browser == 'chrome':
                        driver = webdriver.Chrome(executable_path=WIN_CHROME)
                        return self.browser_setup_args(driver)

                    elif self.browser == 'firefox':
                        driver = webdriver.Firefox(executable_path=WIN_FIREFOX, service_log_path=log_path)
                        return self.browser_setup_args(driver, )

                    else:
                        logger.info(f'windows系统不支持此浏览器: {self.browser}')
                        raise ErrorCustom(f'windows系统不支持此浏览器: {self.browser}')
                else:
                    logger.info(f'当前{current_sys}系统不支持！')
                    raise ErrorCustom('当前{current_sys}系统不支持！')
            else:
                logger.error('项目地址地址请求异常！！！')
                raise ErrorCustom('项目地址地址请求异常！！！')

        except Exception as e:
            logger.error(f'浏览器驱动启动失败 {e}')
            raise Exception("浏览器驱动启动失败!!!!")
