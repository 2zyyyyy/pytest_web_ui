# -*- coding: utf-8 -*-

import time
import os
import pyautogui
import pyperclip
import allure
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from Public.common import ErrorCustom
from Public.yaml_data import GetLocatorYaml, GetCaseYaml
from Public.logs import logger
from Config.ptahconf import SCREENSHOT_DIR, MAC_CHROME
from Config.setting import POLL_FREQUENCY, IMPLICITLY_WAIT_TIME


class Base:
    yamlFile = None

    def __init__(self):
        self.driver = MAC_CHROME

    def get_title(self):
        """
        获取当前页面  title
        :return:
        """
        title = self.driver.title
        logger.info(f"获取当前title {title}")
        return title

    def get_url(self):
        """
        获取当前页面的URL
        :return:
        """
        current_url = self.driver.current_url
        logger.info(f"获取当前url {current_url}")
        return current_url

    def get_url_html(self):
        """
        获取当前页面 html内容
        :return:
        """
        source_html = self.driver.page_source
        return source_html

    def refresh(self):
        """
        刷新当前页面
        :return:
        """
        logger.info('刷新当前页面')
        return self.driver.refresh()

    def back(self):
        """
        返回上一个页面
        :return:
        """
        logger.info('返回上一个页面')
        return self.driver.back()

    def forward(self):
        """
        前进到下一个页面
        :return:
        """
        logger.info('前进到下一个页面')
        return self.driver.forward()

    def base_click(self):
        """
        点击页面
        :return:
        """
        base_click = self.driver.click()
        return base_click

    def switch_to_iframe_el(self, index):
        """
        切换iframe
        :param index: int 索引位置
        :return:
        """
        return self.driver.switch_to.frame(index)

    def web_scroll(self, direction):
        """
        网页滚动
        :param direction: str   up 向上   Down 向下
        :return:
        """
        if direction == "up":
            logger.info('滚动到顶部')
            self.driver.execute_script("window.scrollBy(0, -10000);")
        if direction == "down":
            logger.info('滚动到底部')
            self.driver.execute_script("window.scrollBy(0, 10000)")

    def current_window(self):
        """
        获取当前窗口句柄 不能单一使用 实际获取的不是当前句柄
        :return:
        """
        current_window = self.driver.current_window_handle
        logger.info(f'获取当前句柄 {current_window}')
        return current_window

    def all_handle(self):
        """
        获取所有句柄
        :return:  list
        """
        handle = self.driver.window_handles
        logger.info(f'获取所有句柄 {handle}')
        return handle

    def switch_windows(self, index):
        """
        多窗口切换
        :param index: 列表索引 all_handle的列表索引位置
        :return:
        """
        index_handle = self.all_handle()[index]
        try:
            logger.info(f'窗口已经切换{index_handle}')
            return self.driver.switch_to.window(index_handle)

        except Exception as e:
            logger.error("查找窗口句柄handle异常-> {0}".format(e))

    def switch_frame(self, el):
        """
        #切换到iframe
        :param el: 可以是element 或者是 元素
        :return:
        """
        self.driver.switch_to.frame(el)

    def switch_default_content(self):
        """
        返回默认节点
        :return:
        """
        self.driver.switch_to.default_content()

    def switch_parent_frame(self):
        """
        返回父节点
        :return:
        """
        self.driver.switch_to.parent_frame()

    def accept(self):
        """
        警告框处理 确认
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.accept()
            logger.info('警告框已确认')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def dismiss(self):
        """
        警告框处理  取消
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.dismiss()
            logger.info('警告框已取消')
            return accept
        except Exception as e:
            logger.error("查找dismiss弹出框异常-> {0}".format(e))

    def alert_text(self):
        """
        警告框处理 提取警告框文本
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.text
            logger.info(f'警告框文本信息为 {accept}')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def screen_shot(self, doc):
        """
        截取当前界面图片
        :param doc:  str 名称
        :return:
        """
        file_name = doc + "." + str(round(time.time() * 1000)) + ".png"
        if len(file_name) >= 200:
            file_name = str(round(time.time() * 1000)) + ".png"
        file_path = os.path.join(SCREENSHOT_DIR, file_name)

        self.driver.save_screenshot(file_path)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=file_name,
                      attachment_type=allure.attachment_type.PNG)
        logger.info(f"截图成功已经存储在: {file_path}")

    def get_dropdown_options_count(self, types, locate):
        """
        获取下拉选项的个数
        :param locate or types: 定位类型
        :param locate: 定位器
        :return:
        """

        element = self.used_operate(types, locate)
        sel = Select(element)
        options = sel.options
        return options

    def element_hover(self, types, locate):
        """
        获取元素后悬停到元素位置
        :param locate or types: 定位类型
        :param locate: 定位器
        :return:
        """
        element = self.used_operate(types, locate)
        hover = ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"鼠标悬停位置{locate}")
        return hover

    def element_hover_clicks(self, types, locate):
        """
        获取元素后悬停到元素位置 后点击该元素
        :param locate or types: 定位类型
        :param locate: 定位器
        :return:
        """
        element = self.used_operate(types, locate)
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(0.5)
        self.used_double_click(types=types, locate=locate)
        logger.info(f"鼠标悬停位置{locate}")

    def save_as_img(self, types, locate, filename, sleep=1):
        """
        图片另存为  下载文件也可以直接使用
        :param locate or types: 定位类型
        :param locate: 定位器
        :param filename: 图片名称 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待window 窗口时间 默认 1 秒
        :return: str path 文件路径
        """
        # 右键点击
        self.used_right_click(types=types, locate=locate)
        # 图片另存为
        pyautogui.typewrite(['V'])

        # 将地址以及文件名复制
        pic_dir = os.path.join(SCREENSHOT_DIR, f'{filename}.jpg')
        pyperclip.copy(pic_dir)

        # 等待窗口打开，以免命令冲突，粘贴失败，试过很多次才有0.8，具体时间自己试
        time.sleep(sleep)

        # 热键组合: hotkey() 可以模拟组合热键, 比如: ctrl-c, ctrl-a, ctrl-v 等
        pyautogui.hotkey('ctrlleft', 'V')

        # 保存
        pyautogui.press('enter')
        logger.info(f'图片路径为{filename}！')
        return pic_dir

    def upload_files(self, types, locate, filepath, sleep=1):
        """
        文件上传
        :param locate or types: 定位类型
        :param locate: 定位器
        :param filepath: 文件路径 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待window 窗口时间 默认 1 秒
        :return:
        """
        self.used_right_click(types, locate)

        time.sleep(sleep)

        # 支持中文路径
        pyperclip.copy(filepath)
        time.sleep(sleep)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('enter', presses=2)
        logger.info(f'上传文件路径{filepath}')

    def select_locate(self, types, locate, value):
        """
        下拉框操作  **此函数只支持 Select标签 其它标签不支持
        :param types:  定位类型
        :param locate: 定位参数
        :param value:   #选项文字内容
            # 通过index进行选择
            .select_by_index(1)
            # 通过value进行选择
            .select_by_value("2")
            select_by_visible_text("Male")
            # 通过选项文字进行选择
        :return:
        """
        select = self.used_operate(types, locate)
        Select(select).select_by_visible_text(value)

    @staticmethod
    def get_by_type(types):
        """
        获取定位类型
        :param types:  str  in(id,name,xpath,css,class,link,partial_link,tag)
        :return:  False
        """
        locator_type = types.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "partial_link":
            return By.PARTIAL_LINK_TEXT
        elif locator_type == "tag":
            return By.TAG_NAME
        else:
            logger.info(f"Locator type {locator_type} not correct/supported")
            raise Exception('定位类型错误！！！！')

    def is_element_displayed(self, types, locate):
        """
        检查元素是否可见
        :param types:定位类型
        :param locate: 定位器
        :return:
        """
        is_displayed = False
        element = None

        if locate:
            element = self.used_operate(types, locate)
        if element is not None:
            is_displayed = element.is_displayed()
            logger.info(f"Element is displayed with locate: {locate} and types: {types}")
        else:
            logger.error(f"Element is not displayed with locate: {locate} and types: {types}")
        return is_displayed

    def is_element_exist(self, types, locate):
        """
        检查元素是否存在
        :param types: 定位类型 used_operate 函数传递过来
        :param locate: 定位器
        :return:
        """
        if self.wait_for_element(types, locate):
            element_list = self.driver.find_elements(types, locate)
            if len(element_list) > 0:
                logger.info(f"找到元素 {locate}")
                return True
            else:
                logger.info("元素未找到")
                return False

    def wait_for_element(self, types, locate):
        """
        等待元素被加载  配合 isElementExist 函数检查元素是否存在
        :param types: 定位类型  used_operate 函数传递过来
        :param locate:  定位器
        :return:
        """
        timeout = IMPLICITLY_WAIT_TIME
        poll = POLL_FREQUENCY
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll)

            element = wait.until(ec.presence_of_element_located((types, locate)))
            logger.info(f'等待页面元素 {locate} {types}  存在')
            return element
        except Exception as e:
            logger.error('等待元素错误,元素在等待时间内未出现！')
            logger.error(e)

    def used_operate(self, types, locate, el=None):
        """
        获取元素  此函数配合 isElementExist 检查元素是否存在
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :return: driver 对象
        """
        types = self.get_by_type(types)
        # logger.info(notes)
        if self.is_element_exist(types, locate):
            if el is not None:
                # find_element 不为空时 查询多个
                element = self.driver.find_elements(types, locate)
            else:
                # find_element 为空时 查询单个
                element = self.driver.find_element(types, locate)
            return element
        else:
            logger.error('定位元素错误未找到！')

    def used_text(self, types, locate, el=None, index=None):
        """
        获取元素  提取文本内容
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index:
        :return: driver 对象
        """

        if el is not None and index is not None:
            # 多个定位
            return self.used_operate(types=types, locate=locate, el=el)[index].text
        else:
            # 单个定位提取文本元素必须是唯一 如果多个时默认返回第一个
            return self.used_operate(types=types, locate=locate).text

    def used_click(self, types, locate, el=None, index=None):
        """
        获取元素后  点击
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            self.used_operate(types=types, locate=locate, el=el)[index].click()
        else:
            # 单个定位点击
            self.used_operate(types=types, locate=locate).click()

    def used_right_click(self, types, locate, el=None, index=None):
        """
        获取元素后 右键点击
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        if el is not None and index is not None:
            element = self.used_operate(types=types, locate=locate, el=el)[index].click()
            ActionChains(self.driver).context_click(element).perform()
        else:
            # 单个定位点击
            element = self.used_operate(types=types, locate=locate, ).click()
            ActionChains(self.driver).context_click(element).perform()

    def used_double_click(self, types, locate, el=None, index=None):
        """
        获取元素后 双击
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        if el is not None and index is not None:
            element = self.used_operate(types=types, locate=locate, el=el)[index]
            ActionChains(self.driver).double_click(element).perform()
        else:
            # 单个定位点击
            element = self.used_operate(types=types, locate=locate)
            ActionChains(self.driver).double_click(element).perform()

    def used_input(self, types, locate, text, el=None, index=None):
        """
        获取元素后输入 并支持键盘操作
        :param types: 定位类型
        :param text: 文本信息
        :param locate:  定位元素或者 表达式
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        if el is not None and index is not None:
            self.used_operate(types=types, locate=locate, el=el)[index].send_keys(text)
        else:
            self.used_operate(types=types, locate=locate, ).send_keys(text)

    def used_clear(self, types, locate, el=None, index=None):
        """
        清除输入框  * 此方法不适用时 请用js_clear
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        """

        if el is not None and index is not None:
            self.used_operate(types=types, locate=locate, el=el)[index].clear()
        else:
            self.used_operate(types=types, locate=locate).clear()

    def js_clear(self, types, locate, el=None, index=None):
        """
        js方式清除 输入框
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        if el is not None and index is not None:
            element = self.used_operate(types=types, locate=locate, el=el)[index]
        else:
            element = self.used_operate(types=types, locate=locate)

        self.driver.execute_script("arguments[0].value = '';", element)

    def execute_js(self, js: str):
        """
        执行js
        :param js: js 语法
        """
        self.driver.execute_script(js)

    def used_clear_continue_input(self, types, locate, text, el=None, index=None):
        """
        清除数据在输入
        :param types: 定位类型
        :param locate: 定位元素
        :param text: 输入文本
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        self.used_clear(types=types, locate=locate, el=el, index=index)
        time.sleep(3)
        self.used_input(types=types, locate=locate, text=text, el=el, index=index)


class WebBase(Base):
    """
     常用定位方式  'id', 'name', 'xpath', 'css', 'class', 'link', 'partial_link', 'tag'
    """

    @staticmethod
    def get_locator(yaml_names=None, case_names=None):
        """
        获取定位数据
        :param yaml_names:  yaml 路径
        :param case_names:   用例名称
        :return:
        """

        if yaml_names is not None:
            d = GetLocatorYaml(yaml_name=yaml_names, case_name=case_names)
            return d
        else:
            raise ErrorCustom('yaml路径不能为空！')

    @staticmethod
    def get_case(yaml_names=None, case_names=None):
        """
        获取用例数据
        :param yaml_names: yaml 路径
        :param case_names:  用例名称
        :return:
        """
        if yaml_names is not None:
            d = GetCaseYaml(yaml_name=yaml_names, case_name=case_names)
            return d
        else:
            raise ErrorCustom('yaml路径不能为空！')

    def __if_commonly_used_predicate(self, types, locate, operate=None, text=None, el=None, index=None, wait=0.5):
        """
        * 私有方法不继承
        判断 CommonlyUsed 执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作 类型input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) ,
        :param text: 输入文本内容
        :param el: 输入文本内容
        :param wait: 默认 等待0.5 秒
        :return:
        """
        if operate is None:
            time.sleep(wait)
            return self.used_operate(types=types, locate=locate, el=el)

        elif operate == 'text':  # 提取文本
            time.sleep(wait)
            return self.used_text(types=types, locate=locate, el=el, index=index)

        elif operate == 'click':  # 点击操作
            time.sleep(wait)
            self.used_click(types=types, locate=locate, el=el, index=index)

        elif operate == 'input':  # 输入操作
            if text is not None:
                time.sleep(wait)
                return self.used_input(types=types, locate=locate, text=text, el=el, index=index)
            logger.error(' 函数必须传递 text 参数')

        elif operate == 'clear':  # 清除操作
            time.sleep(wait)
            return self.used_clear(types=types, locate=locate, el=el, index=index)

        elif operate == 'clear_continue_input':  # 清除后在输入操作
            if text is not None:
                time.sleep(wait)
                return self.used_clear_continue_input(types=types, locate=locate, text=text, el=el, index=index)
            logger.info(' 函数必须传递 text 参数')
        else:
            logger.info('暂时不支持此操作！！！')
            logger.error("""
        目前只支持类型 ： input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) 
            """)

    def web_expression(self, types, locate, operate=None, text=None, el=None, index=None, wait=0.5, notes=None):
        """
        web 执行操作判断
        :param types: 定位类型
        :param locate: 表达 或者定位元素
        :param operate: 执行操作  input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)  * 只支持 5种
        :param text : 输入文本内容
        :param el: 单个/多个  默认 el=None 单个  / 如果 el = 's' 代表多个
        :param index:
        :param wait: 默认 等待0.5 秒
        :param notes: 帮助说明 /说明此步骤
        :return:
        """

        if types in ('id', 'name', 'xpath', 'css', 'class', 'link', 'partial_link', 'tag'):
            logger.info(notes)
            return self.__if_commonly_used_predicate(types=types, locate=locate, operate=operate, text=text, el=el,
                                                     index=index,
                                                     wait=wait)

        else:
            logger.error(f'输入的{operate}操作类型，暂时不支持！！')
            logger.error("""只支持 id,name,xpath,css,class,link,partial_link,tag 定位方式""")
