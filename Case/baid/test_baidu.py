# -*- coding: utf-8 -*-

import os

import pytest
import allure

from Page.baidu import BaiDu
from Public.yaml_data import case_data

yamlFile = os.path.basename(__file__).replace('py', 'yaml')  # 获取当前目录运行文件


class TestBaiDu:

    @allure.feature("百度搜索")  # 测试用例特性（主要功能模块）
    @allure.story("搜索验证")  # 模块说明
    @allure.title("输入内容并搜索")  # 用例标题
    @allure.description('输入多参数搜索')  # 用例描述
    @pytest.mark.testbaidu  # 用列标记
    @pytest.mark.parametrize('content', case_data(yamlFile, 'test_baidu_search'))  # 测试数据
    def test_baidu_search(self, driver, content):
        with allure.step('输入搜索内容'):
            BaiDu(driver).input_search_content(content)

        with allure.step('点击搜索'):
            BaiDu(driver).click_search_button()
