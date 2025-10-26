import os
from time import sleep

import allure

from baseutil.ui2_base import UiautomatorBase
from common.common_api import Common
from common.log import logger
from common.task_info import base_dir


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
    conv_bar_setting_id = 'id=com.android.systemui:id/settings_button'
    conv_bar_WLAN_expand_id = 'id=com.android.systemui:id/expand_indicator'


class OPPOUtil(UiautomatorBase):

    def open_app(self, pkg_name):
        logger.info(f"打开{pkg_name}应用")
        self.pkg_open_app(pkg_name)

    def appcenter_start(self, local_text):
        for _ in range(5):
            if self.exists(local_text):
                logger.info(f"应用中心打开{local_text}应用")
                self.click(local_text)
                return True
            self.d.swipe_ext("left")
            sleep(2)
        logger.error(f"应用中心未找到{local_text}应用")
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
            if self.exists(text):
                logger.info(f"回到{text}界面成功")
                return True
        logger.error(f"回到{text}界面失败")
        return False

    def convenient_bar_start(self):
        self.d.open_notification()
        sleep(1)
        return self.check_id_load('便捷栏', OPPOVar.conv_bar_setting_id)

    def check_id_load(self, id_name, resource_id):
        if self.exists(resource_id):
            logger.info(f"{id_name}加载成功")
            return True
        else:
            logger.error(f"{id_name}加载失败")
            return False

    def click_home(self):
        self.d.press("home")

    def upload_test_screen(self):
        try:
            screen_image = base_dir + os.sep + 'test_screen.png'
            if os.path.exists(screen_image):
                os.remove(screen_image)
            self.d.screenshot(screen_image)
            Common.resize_image_with_aspect(screen_image, screen_image)
            sleep(0.1)
            allure.attach.file(screen_image, name="测试截图",
                               attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.exception(f"上传测试截图异常:{e}")
