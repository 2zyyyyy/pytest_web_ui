# -*- coding: utf-8 -*-

import os
import re
from typing import List
import time
import shutil
from Config.setting import IS_CLEAN_REPORT
from Public.yaml_data import GetCaseYaml
from Config.ptahconf import REPORT_ALLURE_DIR, REPORT_JSON_DIR, SCREENSHOT_DIR
from Public.logs import logger


def sleep(s: float):
    """
    休眠秒数
    :param s:
    :return:
    """
    time.sleep(s)
    logger.info('强制休眠{}'.format(s))


class ErrorCustom(Exception):
    """
    自定义异常类
    """
    def __init__(self, message):
        super().__init__(message)


def str_re_int(string: str) -> list:
    """
    提取字符中的整数
    :param string: 字符串
    :return: list
    """
    find_list = re.findall(r'[1-9]+\.?[0-9]*', string)
    return find_list


def clean_report(filepath: str) -> None:
    """
    清除测试报告文件
    :param filepath:  str  清除路径
    :return:
    """
    del_list = os.listdir(filepath)
    if del_list:
        for f in del_list:
            file_path = os.path.join(filepath, f)

            # 判断是不是文件
            if os.path.isfile(file_path):
                if not file_path.endswith('.xml'):  # 不删除.xml文件
                    os.remove(file_path)
            else:
                os.path.isdir(file_path)
                shutil.rmtree(file_path)


def del_clean_report():
    """
    执行删除测试报告记录
    :return:
    """
    if IS_CLEAN_REPORT:  # 如果为 True 清除 REPORT_ALLURE_DIR、 REPORT_JSON_DIR 、REPORT_SCREEN_DIR 路径下报告
        dirs = [REPORT_ALLURE_DIR, REPORT_JSON_DIR, SCREENSHOT_DIR]
        for d in dirs:
            # dir_file = Path(dir) # 判断路径是否存在
            # if dir_file.is_file():
            clean_report(d)


class Get:
    """
    获取测试数据
    """

    @staticmethod
    def test_data(yaml_name: str, case_name: str) -> List:
        test_data = GetCaseYaml(yaml_name, case_name).test_data_values()
        return test_data
