import allure
import pytest

from page.android_page import AndroidUtil
from util.common import AdbUtil, Allure
from util.log import logger


@allure.feature("应用中心")
class TestAppCenter:

    @staticmethod
    def setup_method():
        logger.info("---setup_method---")
        AdbUtil.back_home()

    @staticmethod
    def teardown_method():
        logger.info("---teardown_method---")
        AdbUtil.back_home()

    @pytest.mark.parametrize(
        "app_name, app_expect",
        AndroidUtil.get_appcenter_list(),
    )
    @pytest.mark.OPPO
    def test_appcenter_file_manager(self, android_util, app_name, app_expect):
        allure.dynamic.title(f"应用中心-{app_name}")
        allure.dynamic.description(f"""
            测试场景：应用中心打开{app_name}-检查页面UI-{app_expect}
            前置条件：
                1、安卓adb已连接
            测试步骤：
                1、应用中心打开{app_name}
                2、检查页面响应
            预期结果：
                1、{app_name}应用正常进入
            """)
        try:
            with Allure.step(f"---测试：应用中心{app_name}---"):
                android_util.upload_android_screen()
            with Allure.step(f"应用中心打开{app_name}"):
                android_util.appcenter_open_handle_pre(app_name)
            with Allure.step(f"检查页面UI加载{app_expect}"):
                android_util.check_element_load(app_expect)
        except Exception as e:
            raise e
