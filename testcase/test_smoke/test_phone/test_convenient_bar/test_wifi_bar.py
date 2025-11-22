from time import sleep

import allure
import pytest
from pytest_assume.plugin import assume

from common.common_api import Allure
from common.log import logger
from data.mobile_phone_element import OPPOElement
from page.oppo_page import OPPOUtil


@allure.feature("便捷栏")
class TestConvenientBarWLAN:

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
        测试步骤：1、打开便捷栏和WLAN界面
                2、检查页面响应
        预期结果：1、WLAN正常打开
        """
    )
    @allure.title("便捷栏WLAN界面")
    @pytest.mark.op
    def test_appcenter_wifi(self):
        try:
            with Allure.step("---测试：便捷栏WLAN---"):
                self.oppo_util.upload_test_screen()
            with Allure.step("1、打开便捷栏和WLAN界面"):
                logger.info("下滑便捷栏并检查")
                self.oppo_util.convenient_bar_start()
                sleep(1)
                self.oppo_util.upload_test_screen()
                self.oppo_util.click(OPPOElement.conv_bar_WLAN_expand_id)
                sleep(1)
            with Allure.step("2、检查页面响应"):
                logger.info("检查WLAN界面")
                result = self.oppo_util.check_element_load(OPPOElement.WLAN_text)
                sleep(1)
                self.oppo_util.upload_test_screen()
                with assume:
                    assert result, "打开WLAN界面失败"
        except Exception as e:
            raise e
