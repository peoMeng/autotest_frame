from typing import TypeVar, Protocol, Type

import uiautomator2 as u2

from util.log import logger
from util.setter import argsetter


class UiautoBase:
    """基础页面类：支持通过变量值前缀 "=" 自动适配定位类型
    (如 conv_bar_setting_id = 'id=com.android.systemui:id/settings_button')
    默认使用text定位类型
    """

    # 可在这里添加定位类型
    _prefix_map = {
        "text": "text",
        "textContains": "textContains",
        "id": "resourceId",
        "desc": "description",
        "class": "className",
        "xpath": "xpath",
    }

    def __init__(self):
        logger.info(f"uiautomator2 connect {argsetter.device_id}")
        self.d = u2.connect(argsetter.device_id)

    @classmethod
    def _parse_locator(cls, expr: str):
        """定位元素前缀解析"""
        if "=" not in expr:
            return "text", expr

        prefix, value = expr.split("=", 1)
        if prefix not in cls._prefix_map:
            raise ValueError(f"Unsupported locator prefix: {prefix}")

        return cls._prefix_map[prefix], value

    def _selector(self, element: str):
        key, value = self._parse_locator(element)
        return self.d.xpath(value) if key == "xpath" else self.d(**{key: value})

    def click(self, element: str):
        self._selector(element).click()

    def exists(self, element: str) -> bool:
        return self._selector(element).exists

    def wait_exists(self, element: str, timeout=5):
        return self._selector(element).wait(timeout=timeout)

    def pkg_open_app(self, pkg: str):
        self.d.app_start(pkg)

    def swipe(self, swipe_type):
        self.d.swipe_ext(swipe_type)


TPage = TypeVar("TPage", bound=UiautoBase)


class PageFactory(Protocol):
    def __call__(self, page_cls: Type[TPage]) -> TPage: ...


if __name__ == "__main__":
    text_music = '音乐'
    uiauto_base = UiautoBase()
    uiauto_base.click(text_music)
