import pytest
from Config.ptahconf import *
from Public.logs import logger


class RunPytest:
    @staticmethod
    def output_path():
        """
        生成测试报告路径
        :return:
        """
        # 测试用例结果目录(Json格式)
        report_json_dir = os.path.join(BASE_DIR, "Output", "report_json")
        # 测试结果报告目录(Allure测试报告)
        report_allure_dir = os.path.join(BASE_DIR, "Output", "report_allure")

        # 判断路径文件是否存在 不存在就创建
        list_path_dir = [report_json_dir, report_allure_dir]
        for path in list_path_dir:
            if not os.path.exists(path):
                os.makedirs(path)
        logger.info("测试结果文件路径：{}", list_path_dir)
        return report_json_dir, report_allure_dir

    @classmethod
    def run(cls):
        """
        正式运行所有脚本
        :return:
        """

        # 生成测试结果目录
        report_json_dir, report_allure_dir = cls.output_path()

        # 生成测试报告
        os.system(f'pytest -s -q --alluredir {report_json_dir}')
        os.system(f'allure generate {report_json_dir} -o {report_allure_dir} --clean')
        logger.info('测试报告生成完成！')

        html_index = os.path.join(report_allure_dir, 'index.html')
        logger.info(html_index)

        return html_index

    @staticmethod
    def run_debug():
        """
        debug时调试
        :return:
        """
        pytest.main(
            ['-s', '-v', '-W', 'ignore:Module already imported:pytest.PytestWarning',
             '--alluredir', f'{REPORT_JSON_DIR}', f'{CASE_DIR}'])

        os.system(f'allure generate {REPORT_JSON_DIR} -o {REPORT_ALLURE_DIR} --clean')
        logger.info('测试报告生成完成！')


if __name__ == '__main__':
    # RunPytest.run_debug()
    RunPytest.run()
