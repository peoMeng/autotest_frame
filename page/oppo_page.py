import os
from time import sleep

import allure

from base.ui2_base import UiautomatorBase
from common.common_api import Common
from common.log import logger
from common.task_info import path_run
from data.mobile_phone_element import OPPOElement


class OPPOUtil(UiautomatorBase):

    def appcenter_start(self, app_name):
        for _ in range(5):
            if self.wait_exists(app_name):
                logger.info(f"应用中心打开{app_name}应用")
                self.click(app_name)
                return True
            self.d.swipe_ext("left")
            sleep(2)
        logger.error(f"应用中心未找到{app_name}应用")
        return False

    def check_element_load(self, element):
        if self.wait_exists(element):
            logger.info(f"元素加载成功")
            return True
        else:
            logger.info(f"元素加载失败")
            return False

    def convenient_bar_start(self):
        self.d.open_notification()
        sleep(1)
        return self.check_element_load(OPPOElement.conv_bar_setting_id)

    def click_home(self):
        self.d.press("home")

    def upload_test_screen(self):
        try:
            screen_image = path_run + os.sep + 'android_screen.png'
            if os.path.exists(screen_image):
                os.remove(screen_image)
            self.d.screenshot(screen_image)
            Common.resize_image_with_aspect(screen_image, screen_image)
            sleep(0.1)
            allure.attach.file(screen_image, name="android_screen",
                               attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.exception(f"上传测试截图异常:{e}")
