import os
from contextlib import contextmanager

import allure
import uiautomator2 as u2
from PIL import Image

from common.log import logger
from common import task_info


class Common:

    @classmethod
    def resize_image_with_aspect(cls, input_image_path, output_image_path, max_size=(1500, 700)):
        """
        保持图片原始比例进行压缩。
        :param input_image_path: 输入图片路径
        :param output_image_path: 输出图片路径
        :param max_size: 最大边长，图片将不会超过这个尺寸
        """
        img = Image.open(input_image_path)
        # 等比缩放并保持原始宽高比
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(output_image_path, optimize=True, quality=85)


class Allure:

    @staticmethod
    @contextmanager
    def step(step_msg):
        with allure.step(step_msg):
            logger.info(step_msg)
            yield
