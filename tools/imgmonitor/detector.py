import os

from PIL import Image as P_Image

from common.log import logger
from tools.imgmonitor.base import ImageBase


class ImageDetector:

    @staticmethod
    def detect_black_image(image_path: str):
        """
        检测指定路径图像是否为黑屏
        :param image_path: 图像路径
        :return: (bool) 是否为黑屏，路径不存在返回 None
        """
        # Step 1: 路径检查
        if not image_path or not os.path.exists(image_path):
            logger.warning(f"图像路径不存在: {image_path}")
            return None

        # Step 2: 打开图像
        img = P_Image.open(image_path)

        # Step 3: 黑屏检测
        res_black, proportion = ImageBase.image_black_proportion_pil_detect(img)
        logger.debug(f"黑色区域占比: {proportion}")
        return res_black

    @staticmethod
    def detect_blur_image(image_path: str):
        """
        检测指定路径图像是否为模糊、马赛克
        :param image_path: 图像路径
        :return: (bool) 是否为黑屏，路径不存在返回 None
        """
        # Step 1: 路径检查
        if not image_path or not os.path.exists(image_path):
            logger.warning(f"图像路径不存在: {image_path}")
            return None

        # Step 2: 打开图像
        img = P_Image.open(image_path)

        # Step 3: 黑屏检测
        res_black, proportion = ImageBase.image_blur_detect(img)
        logger.debug(f"模糊度评分: {proportion}")
        return res_black

    @staticmethod
    def detect_flower_image(image_path: str):
        """
        检测指定路径图像是否为花屏
        :param image_path: 图像路径
        :return: (bool) 是否为黑屏，路径不存在返回 None
        """
        # Step 1: 路径检查
        if not image_path or not os.path.exists(image_path):
            logger.warning(f"图像路径不存在: {image_path}")
            return None

        # Step 2: 打开图像
        img = P_Image.open(image_path)

        # Step 3: 黑屏检测
        res_black, proportion = ImageBase.image_flower_detect(img)
        logger.debug(f"花屏置信度评分: {proportion}")
        return res_black

    @staticmethod
    def detect_green_image(image_path: str):
        """
        检测指定路径图像是否为绿帧
        :param image_path: 图像路径
        :return: (bool) 是否为黑屏，路径不存在返回 None
        """
        # Step 1: 路径检查
        if not image_path or not os.path.exists(image_path):
            logger.warning(f"图像路径不存在: {image_path}")
            return None

        # Step 2: 打开图像
        img = P_Image.open(image_path)

        # Step 3: 黑屏检测
        res_black, proportion = ImageBase.image_green_frame_detect(img)
        logger.debug(f"G 通道相对强度: {proportion}")
        return res_black
