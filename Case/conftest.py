# -*- coding: utf-8 -*-

import pytest
from Public.driver_init import WebInit


@pytest.fixture(scope='function', autouse=True)
def driver():
    wb = WebInit()
    driver = wb.enable
    yield driver
    driver.quit()


# 生成environment.properties文件
def pytest_session_finish(session):
    with open("{}/Results/environment.properties".format(session.config.rootdir), "w") as f:
        f.write("Browser=Chrome\nBrowser.Version=89.0.4389.90\nRemake=environment")
