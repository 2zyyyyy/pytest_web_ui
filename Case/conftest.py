# -*- coding: utf-8 -*-

import pytest
from Public.driver_init import WebInit


@pytest.fixture(scope='function', autouse=True)
def driver():
    wb = WebInit()
    driver = wb.enable
    yield driver
    driver.quit()
