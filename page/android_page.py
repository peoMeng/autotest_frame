import os
from time import sleep

import allure

from base.ui2_base import UiautoBase
from data.android_element import AndroidElement
from util.common_service import PageMeta, platform_register
from util.handler import ImageHandler
from util.log import logger
from util.setter import argsetter


class AndroidUtil(UiautoBase, metaclass=PageMeta):

    @platform_register("OPPO")
    def appcenter_open_handle_pre(self, app_name):
        """应用中心打开处理前置"""
        handle_pre_mapper = {
            AndroidElement.file_manager: self.handle_file_manager_pre,
        }
        handle_pre = handle_pre_mapper.get(app_name)
        if handle_pre:
            logger.info(f"{app_name}前置处理")
            handle_pre()
        if not self.appcenter_open_app(app_name):
            logger.error(f"应用中心未找到{app_name}应用")
            return False
        self.upload_android_screen()
        return True

    @platform_register("OPPO")
    def appcenter_open_app(self, app_name):
        for _ in range(5):
            if self.wait_exists(app_name):
                self.click(app_name)
                return True
            self.upload_android_screen()
            self.swipe("left")
        return False

    def check_element_load(self, element):
        if self.wait_exists(element):
            logger.info("元素加载成功")
            self.upload_android_screen()
            return True
        else:
            logger.error("元素加载失败")
            self.upload_android_screen()
            return False

    def handle_file_manager_pre(self):
        self.appcenter_open_app(AndroidElement.tool)

    def upload_android_screen(self):
        try:
            screen_image = argsetter.path_run + os.sep + 'android_screen.png'
            if os.path.exists(screen_image):
                os.remove(screen_image)
            self.d.screenshot(screen_image)
            ImageHandler.resize_image_with_aspect(screen_image, screen_image)
            sleep(0.1)
            allure.attach.file(screen_image, name="android_screen",
                               attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"上传测试截图异常:{e}")
