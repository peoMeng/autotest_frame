from time import sleep

import allure
import pytest
from pytest_assume.plugin import assume

from common.common_api import Allure
from common.log import logger
from data.mobile_phone_element import OPPOElement
from page.oppo_page import OPPOUtil


@allure.feature("应用中心")
class TestAppCenterOppoVideo:

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
        测试步骤：1、应用中心打开oppo视频
                2、检查页面响应
        预期结果：1、应用正常打开
        """
    )
    @allure.title("应用中心oppo视频")
    @pytest.mark.op
    def test_appcenter_oppo_video(self):
        try:
            with Allure.step("---测试：应用中心oppo视频---"):
                self.oppo_util.upload_test_screen()
            with Allure.step("1、应用中心打开oppo视频"):
                logger.info("应用中心查找oppo视频应用并打开")
                self.oppo_util.appcenter_start(OPPOElement.oppo_video_name)
                sleep(1)
                self.oppo_util.upload_test_screen()
            with Allure.step("2、检查页面响应"):
                logger.info("检查oppo视频页面")
                result = self.oppo_util.check_element_load(OPPOElement.oppo_video_text)
                sleep(1)
                self.oppo_util.upload_test_screen()
                with assume:
                    assert result, "打开oppo视频应用失败"
        except Exception as e:
            raise e
