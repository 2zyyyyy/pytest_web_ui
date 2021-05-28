# -*- coding: utf-8 -*-

import os
from typing import List
import yaml
from Public.logs import logger
from Config.ptahconf import TESTCASE_DIR, LOCATOR_DIR


# 读取Yaml数据
class GetLocatorYaml:
    """
     获取测试用例 locatorYaml数据类
    """

    def __init__(self, yaml_name: str, case_name: str) -> None:
        """
        :param yaml_name:  yaml 文件名称
        :param case_name:  用列名称 对应 yaml 用列
        """
        self.model_name = yaml_name  # 模块名称 对应yaml 文件名
        self.yaml_name = yaml_name  # yaml 文件名称 拼接后的路径
        self.case_name = case_name  # 用列名称 对应 yaml 用列

        self.FILE_PATH = os.path.join(LOCATOR_DIR, f"{self.yaml_name}")

    def open_yaml(self):
        """
        读取yaml文件
        :return: dict
        """

        try:
            with open(self.FILE_PATH, encoding='gbk') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
                return data
        except Exception as e:
            logger.error(e)
            logger.error(f'读取yaml失败！{e}')

    def get_yaml(self):
        """
        返回yaml文件数据
        :return: dict
        """
        yaml_data = self.open_yaml()
        return yaml_data[1:]  # 返回用列数据不包含 - model : login 部分 从列表1位置索引

    def get_current_data(self):
        """
        返回 yaml 当前用列的所有数据
        :return: dict
        """
        yaml_list = self.get_yaml()
        for yml in yaml_list:
            # 如果用列等于当前 用列就返回
            if yml.get('caseName') == self.case_name:
                return yaml
        return "caseName 不存在！"

    def count_test_data(self):
        """
        统计 yaml  data 测试数据的条数
        :return:
        """
        yaml_list = self.get_yaml()
        for y in yaml_list:
            # 如果用列等于当前 用列就返回
            if y.get('caseName') == self.case_name:
                return len(y.get('testData'))
        return "caseName 不存在！"

    def data_count(self):
        """
        统计 data  数据条数
        :return:
        """
        return self.count_test_data()

    def step_count(self):
        """
        统计 yaml 测试步骤条数
        :return:
        """
        data_list = self.get_yaml()

        for data in data_list:
            # 如果用列等于当前 用列就返回
            if data.get('caseName') == self.case_name:
                return len(data.get('element'))
        return "caseName 不存在！"

    def get_param(self, value: str) -> str:
        """
        获取 yaml用列参数
        :param value:  传递参数值
        :return:
        """

        yaml_list = self.get_yaml()
        for y in yaml_list:
            # 如果用列等于当前 用列就返回
            if y.get('caseName') == self.case_name:
                return y.get(value)
        return "caseName 不存在！"

    def get_set(self, index: int, value: str):
        """
        获取 set 用列步骤数据

        :param index: 列表索引位置
        :param value:  参数值
        :return:
        """

        data_list = self.get_yaml()
        if index < self.step_count():
            for data in data_list:
                # 如果用列等于当前 用列就返回
                if data.get('caseName') == self.case_name:
                    return data.get('element')[index].get(value)
        logger.error(f'{self.case_name}用列只有{self.step_count()}个步骤，你确输入了{index} 步！')
        return None

    def get_model(self):
        """
        返回yaml
        :return: dict
        """
        data = self.open_yaml()
        return data[0].get('model')  #

    def title(self):
        """
        返回用列 title 标题
        :return: str
        """
        return self.get_param('title')

    def preposition(self):
        """
        返回用列 preposition  前置条件
        :return: str
        """
        return self.get_param('preposition')

    def test_data_values(self, ):
        """
        读取yaml  测试数据的 values
        :return:  demo [('u1', 'p1', 'i1'), ('u2', 'p2', 'i2'), ('u3', 'p3', 'i3')]
        """

        data_values_list = []
        data_list = self.get_yaml()

        for data in data_list:
            # 如果用列等于当前 用列就返回 并且读取的是 yaml 数据
            if data.get('caseName') == self.case_name:
                data_list = data.get('testData')
                for i in data_list:
                    data_values_list.append(tuple(i.values()))
                return data_values_list

    def test_data(self, index: int, args: str) -> str:
        """
        **** ！应该会弃用
        返回 用列 测试 data 数据列表
        :param index: 列表的索引位置
        :param args: 字段的key  因为测试数据是可变的增加的
        :return:
        """
        data_list = self.get_yaml()

        if index < self.data_count():

            for data in data_list:
                # 如果用列等于当前 用列就返回 并且读取的是 yaml 数据

                if data.get('caseName') == self.case_name:
                    return data.get('testData')[index].get(args)
        logger.error(f'{self.case_name}用列只有{self.data_count()}条数据，你输入了第{index} 条！')

    def case_step(self, index: int) -> str:
        """
       返回 用列步骤 case_step 参数
       """
        return self.get_set(index, 'case_step')

    def types(self, index: int) -> str:
        """
        返回 用列步骤 types 参数
        """
        return self.get_set(index, 'types')

    def operate(self, index: int) -> str:
        """
        返回 用列步骤 operate 参数
        """
        return self.get_set(index, 'operate')

    def locate(self, index: int) -> str:
        """
        返回 用列步骤 locate 参数
        """
        return self.get_set(index, 'locate')

    def info(self, index: int) -> str:
        """
        返回 用列步骤 info 参数
        """
        return self.get_set(index, 'info')

    def expect(self, index: int) -> str:
        """
        返回 用列步骤 expect 参数
        """
        return self.get_set(index, 'expect')


class GetCaseYaml(GetLocatorYaml):
    """
    获取测试用例 caseYaml数据类
    """

    def __init__(self, yaml_name: str, case_name: str):
        super(GetCaseYaml, self).__init__(yaml_name, case_name)
        self.model_name = yaml_name  # 模块名称 对应yaml 文件名
        self.yaml_name = yaml_name  # yaml 文件名称 拼接后的路径
        self.case_name = case_name  # 用列名称 对应 yaml 用列
        self.FILE_PATH = os.path.join(TESTCASE_DIR, f"{self.yaml_name}")


def case_data(yaml_name: str, case_name: str) -> List:
    """
    获取测试数据 以元素方式返回
    :param yaml_name: yaml 名称
    :param case_name:   用例数据
    :return:
    """
    test_data = GetCaseYaml(yaml_name, case_name).test_data_values()
    return test_data

# faker 信息数据
# class PersonalInfo:
#     """
#     基于 faker 封装个人测试信息类
#     """
#
#     @staticmethod
#     def random_name():
#         """
#         随机姓名
#         :return: str
#         """
#         return fake.name()
#
#     @staticmethod
#     def random_phone_number():
#         """
#         随机手机号码
#         :return:  int
#         """
#         return fake.phone_number()
#
#     @staticmethod
#     def random_email():
#         """
#         随机邮箱
#         :return:
#         """
#         return fake.email()
#
#     @staticmethod
#     def random_job():
#         """
#        随机职位
#        :return:
#        """
#         return fake.job()
#
#     @staticmethod
#     def random_ssn():
#         """
#        随机 省份证信息
#        :return:
#        """
#         return fake.ssn(min_age=18, max_age=90)
#
#     @staticmethod
#     def random_company():
#         """
#         随机 公司名
#         :return:
#         """
#         return fake.company()


# class AddressInfo:
#     """
#     基于 faker 封装地址相关测试信息类
#     """
#
#     @staticmethod
#     def random_city():
#         """
#         随机 城市
#         :return:  str
#         """
#         return fake.city_name()
#
#     @staticmethod
#     def random_province():
#         """
#         随机 省份
#         :return:  str
#         """
#         return fake.province()
#
#     @staticmethod
#     def random_country():
#         """
#         随机 国家
#         :return:  str
#         """
#         return fake.country()
#
#     @staticmethod
#     def random_address():
#         """
#         随机住址信息
#         :return:  str
#         """
#         return fake.address()


# class TimeInfo:
#     """
#     基于 faker 封装时间信息类
#     """
#
#     @staticmethod
#     def random_time():
#         """
#         随机时间24H   22:00:00
#         :return: str
#         """
#         return fake.time()
#
#     @staticmethod
#     def random_year():
#         """
#         随机月份
#         :return: str[0] -数字月  str[0] -英文月
#         """
#         return fake.month(), fake.month_name()
#
#     @staticmethod
#     def random_month():
#         """
#         随机年份
#         :return: str
#         """
#         return fake.month()
#
#     @staticmethod
#     def random_date_this_month():
#         """
#         随机 本月中的日期时间
#         :return: str
#         """
#         return fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
#
#     @staticmethod
#     def random_date_this_decade():
#         """
#         随机 本年中的日期时间
#         :return: str
#         """
#         return fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
#
#     @staticmethod
#     def random_date_time_this_century():
#         """
#         随机 本世纪中的日期和时间
#         :return: str
#         """
#         return fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)
#
#     @staticmethod
#     def random_day_of_week():
#         """
#         随机星期
#         :return:  str
#         """
#         return fake.day_of_week()
#
#     @staticmethod
#     def random_date_of_birth(age):
#         """
#         随机生日
#         :param age:  int  需要随机多少岁之内
#         :return:  str
#         """
#         return fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=age)
