import sys

import pytest
from Config.ptahconf import *
from Public.logs import logger
from Public.common import del_clean_report, ErrorCustom


class RunPytest:

    @classmethod
    def run_module(cls, m, m_list, directory):
        """
        判断运行模块
        :param m:  模块
        :param m_list:  多模块列表
        :param directory: 生成结果项目目录名称
        :return:
        """
        var = cls.value_division(m_list)
        json_dir = directory
        if m == 'all':  # all 运行所有模块用例
            logger.info('运行当前项目所有用例开始！！！')
            pytest.main(
                ['-s', '-v', '-W',
                 'ignore:Module already imported:pytest.PytestWarning',
                 '--alluredir', f'{json_dir}', f'{CASE_DIR}'])
            return True

        elif ',' not in m and m != 'all' and m.startswith('test'):  # 传递1个模块时执行
            logger.info(f'运行当前项目模块用例{m}开始！！！')
            pytest.main(['-s', '-v', '-m', f'{m}', f'-n={n}', f'--reruns={reruns}', '-W',
                         'ignore:Module already imported:pytest.PytestWarning', '--alluredir', f'{json_dir}',
                         f'{CASE_DIR}'])
            return True

        elif ',' in m and len(m_list) <= 5:  # 传递2个模块时执行
            logger.info(f'运行当前项目模块用例{m_list}开始！！！')
            pytest.main(
                ['-s', '-v', '-m', f'{var}', f'-n={n}', f'--reruns={reruns}', '-W',
                 'ignore:Module already imported:pytest.PytestWarning', '--alluredir', f'{json_dir}',
                 f'{CASE_DIR}'])
            return True

        else:  # 运行传递模块用例
            logger.info(f'模块名称错误！！！')
            return False

    @classmethod
    def output_path(cls, directory):
        """
        生成测试报告路径
        :param directory: 目录名称
        :return:
        """
        # 测试用例结果目录
        report_json_dir = os.path.join(BASE_DIR, "output", "{}".format(directory), "report_json")

        # 测试结果报告目录
        report_allure_dir = os.path.join(BASE_DIR, "output", "{}".format(directory), "report_allure")

        # 测试截图目录 暂时不生成零时图片目录
        # screen_dir = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_screen")

        # 判断路径文件是否存在 不存在就创建
        list_path_dir = [report_json_dir, report_allure_dir]
        for path in list_path_dir:
            if not os.path.exists(path):
                os.makedirs(path)

        return report_json_dir, report_allure_dir

    @classmethod
    def run(cls):
        """
        正式运行所有脚本
        :return:
        """
        # 执行前检查是否清除报告
        del_clean_report()

        # 接收参数
        results_dir, module_name, m_list = cls.receiving_argv()

        # 生成测试结果目录
        report_json_dir, report_allure_dir = cls.output_path(results_dir)

        # 判断运行模块
        run_module = cls.run_module(module_name, m_list, report_json_dir)

        # 生成测试报告
        if run_module:
            os.system(f'allure generate {prpore_json_dir} -o {prpore_allure_dir} --clean')
            logger.info('测试报告生成完成！')

            html_index = os.path.join(prpore_allure_dir, 'index.html')
            logger.info(html_index)
            return html_index

    @classmethod
    def receiving_argv(cls):
        """
        接收系统输入参数   1模块名称 2生成结果目录名称  Python run.py all 1 1 demo
        :return:
        """
        # 1模块名称
        try:
            module_name = sys.argv[1]
            m_list = None
            if ',' in module_name:
                m_list = module_name.split(',')

            # 2 生成结果目录名称
            results_dir = sys.argv[2]

            return results_dir, module_name, m_list
        except Exception as e:
            logger.error(e)
            raise ErrorCustom('输入参数错误！')

    @staticmethod
    def run_debug():
        """
        debug 时调试
        :return:
        """

        # 执行前检查是否清除报告
        del_clean_report()

        pytest.main(
            ['-s', '-v', '-n=1', '--reruns=0', '-W', 'ignore:Module already imported:pytest.PytestWarning',
             '--alluredir',
             f'{report_json_dir}', f'{CASE_DIR}'])

        os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')
        logger.info('测试报告生成完成！')


if __name__ == '__main__':
    # RunPytest.run()
    RunPytest.run_debug()
