from time import sleep

import allure
import pytest

from common.common_api import Allure
from common.log import logger
from pages.oppo_page import OPPOUtil, OPPOVar


class TestAppCenterMusic:

    def setup_method(self):
        self.oppo_util = OPPOUtil()
        with Allure.step("---测试用例前置条件:返回主界面---"):
            self.oppo_util.click_home()
            sleep(1)

    def teardown_method(self):
        with Allure.step("---测试用例后置条件:返回主界面---"):
            self.oppo_util.click_home()
            sleep(1)

    @allure.description(
        """
        测试场景：冒烟测试
        前置条件：1、安卓adb已连接
        测试步骤：1、应用中心打开音乐
                2、检查页面响应
        预期结果：1、应用正常打开
        """
    )
    @allure.feature("应用中心音乐")
    @pytest.mark.op
    def test_appcenter_music(self):
        try:
            with Allure.step("---测试：应用中心音乐---"):
                self.oppo_util.upload_test_screen()
            with Allure.step("1、应用中心打开音乐"):
                logger.info("应用中心查找音乐应用并打开")
                result = self.oppo_util.appcenter_start(OPPOVar.music_name)
                sleep(1)
                self.oppo_util.upload_test_screen()
                assert result, "未找到音乐应用"
            with Allure.step("2、检查页面响应"):
                logger.info("检查音乐页面")
                result = self.oppo_util.check_text_load(OPPOVar.music_name, OPPOVar.music_text)
                sleep(1)
                self.oppo_util.upload_test_screen()
                assert result, "打开音乐应用失败"
        except Exception as e:
            with Allure.step("用例异常"):
                self.oppo_util.upload_test_screen()
            raise e
