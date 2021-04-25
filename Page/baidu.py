# -*- coding: utf-8 -*-

import os
# import sys

# sys.path.append(os.pardir)
from Public.web_base import WebBase

'''
    Page对应 locatorYAML 操作页面
'''


class BaiDu(WebBase):
    yamlFile = os.path.basename(__file__).replace('py', 'yaml')  # 获取当前目运行文件 并替换为 yaml 后缀

    def input_search_content(self, content):
        """
        输入操作
        :return:
        """
        d = self.get_locator(self.yamlFile, 'input_search_content')
        self.web_expression(types=d.types(0), locate=d.locate(0), operate=d.operate(0), text=content, notes='输入搜索内容')

    def click_search_button(self):
        d = self.get_locator(self.yamlFile, 'click_search_button')
        self.web_expression(types=d.types(0), locate=d.locate(0), operate=d.operate(0), notes='点击百度一下')
        self.screen_shot('click_search_button')
