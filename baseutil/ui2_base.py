import uiautomator2 as u2

from common.log import logger
from common.task_info import device_id


class UiautomatorBase:
    """基础页面类：支持通过变量值前缀 "=" 自动适配定位类型
    (如 conv_bar_setting_id = 'id=com.android.systemui:id/settings_button')
    默认使用text定位类型
    注意：pkg、xpath定位单独调用对应的方法函数
    """

    # 可在这里添加定位类型
    prefix_map = {
        "text": "text",
        "textContains": "textContains",
        "id": "resourceId",
        "desc": "description",
        "class": "className",
        "pkg": "package_name",
        "xpath": "xpath",
    }

    def __init__(self):
        logger.info(f"uiautomator2 连接 {device_id}")
        self.d = u2.connect(device_id)
        # 定位类型解析，默认返回text类型和元素
        self.locator_resolver = (
            lambda locator_expr: (
                lambda prefix, value: {UiautomatorBase.prefix_map.get(prefix, "text"): value}
            )(*locator_expr.split("=", 1))
            if "=" in locator_expr
            else {"text": locator_expr}
        )

    def click(self, element: str):
        locator = self.locator_resolver(element)
        self.d(**locator).click()

    def xpath_click(self, element: str):
        locator = self.locator_resolver(element)
        self.d.xpath(**locator).click()

    def exists(self, element: str):
        locator = self.locator_resolver(element)
        return self.d(**locator).exists

    def wait_exists(self, element: str, timeout=5):
        locator = self.locator_resolver(element)
        return self.d(**locator).exists(timeout=timeout)

    def pkg_open_app(self, element: str):
        locator = self.locator_resolver(element)
        self.d.app_start(**locator)


if __name__ == "__main__":
    oppo_video_pkg = 'pkg=com.android.settings'
    UiautomatorBase().pkg_open_app(oppo_video_pkg)
