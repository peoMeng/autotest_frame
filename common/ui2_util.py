import os
from time import sleep

import allure
import uiautomator2 as u2

from common.common_api import Common
from common.log import logger
from common.task_info import device_id, path_run


class OPPOVar:
    # 应用名
    oppo_video_name = 'OPPO 视频'
    music_name = '音乐'
    soft_store_name = '软件商店'
    theme_store_name = '主题商店'
    setting_name = '设置'
    tool_name = '工具'
    file_manager_name = '文件管理'
    # 加载文字
    oppo_video_text = '推荐'
    music_text = '乐库'
    soft_store_text = '游戏'
    theme_store_text = '字体'
    setting_text = '搜索设置项'
    file_manager_text = '文件'
    WLAN_text = '可用网络'
    # 便捷栏
    conv_bar_setting_id = 'com.android.systemui:id/settings_button'
    conv_bar_WLAN_expand_id = 'com.android.systemui:id/expand_indicator'


class Uiautomatorutil:
    def __init__(self):
        logger.info(f"uiautomator2连接设备{device_id}")
        self.d = u2.connect(device_id)

    def open_app(self, pkg_name):
        logger.info(f"打开{pkg_name}应用")
        self.d.app_start(pkg_name)

    def close_app(self, pkg_name):
        logger.info(f"关闭{pkg_name}应用")
        self.d.app_stop(pkg_name)

    def appcenter_start(self, app_name):
        for _ in range(5):
            if self.d(text=app_name).exists:
                logger.info(f"应用中心打开{app_name}应用")
                self.d(text=app_name).click()
                return True
            self.d.swipe_ext("left")
            sleep(2)
        logger.error(f"应用中心未找到{app_name}应用")
        return False

    def check_text_load(self, app_name, load_text):
        if self.d(text=load_text).wait(timeout=5):
            logger.info(f"打开{app_name}成功")
            return True
        else:
            logger.error(f"打开{app_name}失败")
            return False

    def back_text_home(self, text):
        logger.info(f"回到{text}界面")
        for _ in range(4):
            self.d.swipe_ext("right")
            sleep(1)
            if self.d(text=text).exists:
                logger.info(f"回到{text}界面成功")
                return True
        logger.error(f"回到{text}界面失败")
        return False

    def convenient_bar_start(self):
        self.d.open_notification()
        sleep(1)
        return self.check_id_load('便捷栏', OPPOVar.conv_bar_setting_id)

    def check_id_load(self, id_name, resource_id):
        if self.d(resourceId=resource_id).wait(timeout=5):
            logger.info(f"{id_name}加载成功")
            return True
        else:
            logger.error(f"{id_name}加载失败")
            return False

    def click_home(self):
        self.d.press("home")

    def upload_test_screen(self):
        try:
            screen_image = path_run + os.sep + 'test_screen.png'
            if os.path.exists(screen_image):
                os.remove(screen_image)
            self.d.screenshot(screen_image)
            Common.resize_image_with_aspect(screen_image, screen_image)
            sleep(0.1)
            allure.attach.file(screen_image, name="测试截图",
                               attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.exception(f"上传测试截图异常:{e}")
