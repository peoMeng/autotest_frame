from time import sleep

import allure
import pytest

from common.common_api import Allure
from common.log import logger

from common.ui2_util import Uiautomatorutil, OPPOVar


class TestAppCenterFileManger:

    def setup_method(self):
        self.ui2_util = Uiautomatorutil()
        with Allure.step("---测试用例前置条件:返回主界面---"):
            self.ui2_util.click_home()
            sleep(1)

    def teardown_method(self):
        with Allure.step("---测试用例后置条件 :返回主界面---"):
            self.ui2_util.click_home()
            sleep(1)

    @allure.description(
        """
        测试场景：冒烟测试
        前置条件：1、安卓adb已连接
        测试步骤：1、应用中心打开文件管理
                2、检查页面响应
        预期结果：1、应用正常打开
        """
    )
    @allure.feature("应用中心文件管理")
    @pytest.mark.op
    def test_appcenter_file_manager(self):
        try:
            with Allure.step("---测试：应用中心文件管理---"):
                self.ui2_util.upload_test_screen()
            with Allure.step("1、应用中心打开文件管理"):
                logger.info("应用中心查找工具组件并打开")
                result = self.ui2_util.appcenter_start(OPPOVar.tool_name)
                sleep(1)
                self.ui2_util.upload_test_screen()
                assert result, "未找到工具组件"
                logger.info("应用中心查找文件管理并打开")
                result = self.ui2_util.appcenter_start(OPPOVar.file_manager_name)
                sleep(1)
                self.ui2_util.upload_test_screen()
                assert result, "未找到文件管理应用"
            with Allure.step("2、检查页面响应"):
                logger.info("检查文件管理页面")
                result = self.ui2_util.check_text_load(OPPOVar.file_manager_name, OPPOVar.file_manager_text)
                sleep(1)
                self.ui2_util.upload_test_screen()
                assert result, "打开文件管理应用失败"
        except Exception as e:
            with Allure.step("用例异常"):
                self.ui2_util.upload_test_screen()
            raise e
