import cv2
import numpy as np
from PIL import Image as P_Image
from skimage.metrics import structural_similarity as ssim

from common.log import logger


class ImageBase:

    @staticmethod
    def is_dark_image_but_not_black(image_array: np.ndarray, low_threshold=30, bright_ratio_threshold=0.05) -> (
            bool, float):
        """
        判断图像是否为“暗屏但非黑屏”。

        :param image_array: 图像数组 (BGR / RGB)
        :param low_threshold: 亮度下限（低于此值视为黑）
        :param bright_ratio_threshold: 明亮像素比例阈值（高于此视为非黑）
        :return: (bool, float) -> (是否暗非黑, 明亮像素比例)
        """
        # 转灰度
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_array

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
        total_pixels = gray.size
        bright_pixels = np.sum(hist[low_threshold:])
        bright_ratio = bright_pixels / total_pixels

        is_dark_but_not_black = bright_ratio > bright_ratio_threshold
        return is_dark_but_not_black, bright_ratio

    @staticmethod
    def extract_img_outline(res_mat: np.ndarray):
        """提取图像轮廓"""
        if res_mat.ndim == 2:
            gray_mat = res_mat
        elif res_mat.ndim == 3 and res_mat.shape[2] == 3:
            b, g, r = res_mat[:, :, 0], res_mat[:, :, 1], res_mat[:, :, 2]
            gray_mat = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
        else:
            raise ValueError("The number of channels in the input image not correct")

        gray_blur = cv2.GaussianBlur(gray_mat, (3, 3), 0)
        edges = cv2.Canny(gray_blur, 50, 150)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    @staticmethod
    def image_black_proportion_pil_detect_split(image: P_Image.Image,
                                                black_threshold=15,
                                                global_ratio_threshold=0.95,
                                                block_ratio_threshold=0.6,
                                                grid_size=3) -> (bool, float):
        """
        检测图像是否为黑屏（含全局黑屏或局部黑屏）
        :param image: PIL.Image 对象
        :param black_threshold: RGB <= 该值视为黑
        :param global_ratio_threshold: 全局黑像素比例阈值（≥此值视为黑屏）
        :param block_ratio_threshold: 子块黑像素比例阈值（≥此值视为局部黑屏）
        :param grid_size: 分块维度，默认3表示3×3
        :return: (is_black_screen, black_ratio)
        """
        if not isinstance(image, P_Image.Image):
            logger.warning("image must be of type PIL.Image.Image")
            return None, -1

        # 转 RGB，防止 RGBA 或灰度问题
        image = image.convert("RGB")
        image_array = np.array(image, dtype=np.uint8)

        # 黑色阈值范围
        lower_black = np.array([0, 0, 0], dtype=np.uint8)
        upper_black = np.array([black_threshold] * 3, dtype=np.uint8)

        # 黑色掩码
        mask = cv2.inRange(image_array, lower_black, upper_black)
        total_pixels = mask.size
        black_pixels = np.sum(mask == 255)
        black_proportion = round(black_pixels / total_pixels, 4)

        # Step 1: 全图检测
        if black_proportion >= global_ratio_threshold:
            return True, black_proportion

        # Step 2: 分块检测（3x3）
        h_splits = np.array_split(mask, grid_size, axis=0)
        for row in h_splits:
            v_splits = np.array_split(row, grid_size, axis=1)
            for sub_mask in v_splits:
                sub_ratio = np.sum(sub_mask == 255) / sub_mask.size
                if sub_ratio >= block_ratio_threshold:
                    return True, black_proportion

        return False, black_proportion

    @staticmethod
    def image_black_proportion_pil_detect(
            image: P_Image.Image,
            black_threshold=15,
            global_ratio_threshold=0.9,
            contour_count_limit=300,
            sub_area_ratio_threshold=0.4,
            sub_black_ratio_threshold=0.6
    ) -> (bool, float):
        """
        检测图像是否为黑屏（含全局黑屏或局部黑屏）

        :param image: PIL.Image 对象
        :param black_threshold: RGB <= 该值视为黑
        :param global_ratio_threshold: 全局黑像素比例阈值（≥此值视为黑屏）
        :param contour_count_limit: 轮廓数量阈值（超过此值使用分块法判断）
        :param sub_area_ratio_threshold: 子区域面积比例阈值（≥此值才参与局部判断）
        :param sub_black_ratio_threshold: 子区域黑色像素比例阈值（≥此值视为局部黑屏）
        :return: (is_black_screen, black_ratio)
        """

        # Step 0: 类型校验
        if not isinstance(image, P_Image.Image):
            logger.warning("image must be of type PIL.Image.Image")
            return None, -1.0

        # Step 1: 图像预处理
        image = image.convert("RGB")
        image_array = np.array(image, dtype=np.uint8)
        height, width, _ = image_array.shape

        # Step 2: 暗屏过滤（排除暗但有内容的画面）
        is_dark_screen, bright_ratio = ImageBase.is_dark_image_but_not_black(image_array)
        if is_dark_screen:
            return False, 0.0

        # Step 3: 全局黑色比例检测
        mask = cv2.inRange(image_array, (0, 0, 0), (black_threshold,) * 3)
        total_pixels = mask.size
        black_pixels = np.sum(mask == 255)
        black_ratio = round(float(black_pixels / total_pixels), 4)
        if black_ratio >= global_ratio_threshold:
            return True, black_ratio

        # Step 4: 中心区域亮度检测（快速排除非黑屏）
        binary = cv2.bitwise_not(mask)
        center_region = binary[height // 4:3 * height // 4, : width - 50]
        if np.any(center_region != 0):
            return False, black_ratio

        # Step 5: 轮廓检测（检测前景/亮度变化区域）
        contours, _ = ImageBase.extract_img_outline(binary)
        if len(contours) > contour_count_limit:
            res_split, prop_split = ImageBase.image_black_proportion_pil_detect_split(image)
            return res_split, prop_split

        # Step 6: 构造整图外轮廓与内部区域掩码
        outer_contour = np.array([
            [[0, 0]],
            [[width - 1, 0]],
            [[width - 1, height - 1]],
            [[0, height - 1]]
        ], dtype=np.int32)

        mask_outer = np.zeros_like(binary)
        color = (255,) if len(mask_outer.shape) == 2 else (255, 255, 255)
        cv2.drawContours(mask_outer, [outer_contour], -1, color, -1)

        mask_small_union = np.zeros_like(binary)
        if contours:
            cv2.drawContours(mask_small_union, contours, -1, color, -1)

        # Step 7: 局部区域黑度分析
        mask_large_region = cv2.bitwise_and(mask_outer, cv2.bitwise_not(mask_small_union))
        for sub_mask in [mask_large_region, mask_small_union]:
            sub_area = np.sum(sub_mask == 255)
            if sub_area == 0 or sub_area < sub_area_ratio_threshold * total_pixels:
                continue

            sub_black_pixels = np.sum((binary == 0) & (sub_mask == 255))
            sub_black_ratio = sub_black_pixels / sub_area

            if sub_black_ratio > sub_black_ratio_threshold:
                return True, black_ratio

        # Step 8: 默认返回非黑屏
        return False, black_ratio

    @staticmethod
    def image_blur_detect(image: P_Image.Image, threshold: float = 100.0) -> (bool, float):
        """
        检测图像是否模糊（失焦、运动模糊或压缩模糊）

        :param image: PIL.Image 对象
        :param threshold: 模糊判定阈值（Laplacian 方差 < threshold 视为模糊）
        :return: (is_blur, blur_score)
                 - is_blur: bool 是否模糊
                 - blur_score: float 模糊评分（越大越清晰）
        """
        if not isinstance(image, P_Image.Image):
            logger.warning("image must be of type PIL.Image.Image")
            return None, -1.0

        # 转换为 NumPy 数组
        image_np = np.array(image, dtype=np.uint8)

        # 转灰度
        if image_np.ndim == 3:
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        elif image_np.ndim == 2:
            gray = image_np
        else:
            logger.warning("The image dimensions not correct")
            return False, -1.0

        # Laplacian 方差
        laplacian_map = cv2.Laplacian(gray, cv2.CV_64F)
        blur_score = np.var(laplacian_map)

        # 判断模糊
        is_blur = blur_score < threshold

        return bool(is_blur), round(blur_score, 2)

    @staticmethod
    def image_flower_detect(image: P_Image.Image,
                            laplacian_var_threshold: float = 20000.0,
                            color_var_threshold: float = 5000.0,
                            hist_diff_threshold: float = 0.25) -> (bool, float):
        """
        检测图像是否花屏（单帧检测，无需前后帧）

        :param image: PIL.Image 对象
        :param laplacian_var_threshold: Laplacian 方差阈值（纹理过强视为花屏）
        :param color_var_threshold: RGB 通道标准差方差阈值（颜色分布异常视为花屏）
        :param hist_diff_threshold: 直方图平滑性指标阈值（默认0.25）
        :return: (is_flower, flower_score)
                 - is_flower: bool 是否花屏
                 - flower_score: float 花屏置信度分数（越高越异常）
        """
        if not isinstance(image, P_Image.Image):
            logger.warning("image must be of type PIL.Image.Image")
            return None, -1.0

        # --- Step 1: 转换为RGB与灰度图 ---
        image = image.convert("RGB")
        img_np = np.array(image, dtype=np.uint8)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # --- Step 2: Laplacian 方差检测（纹理混乱度） ---
        lap_var = float(np.var(cv2.Laplacian(gray, cv2.CV_64F)))

        # --- Step 3: 通道颜色方差检测（颜色不稳定性） ---
        color_std = np.std(img_np, axis=(0, 1))
        color_var = float(np.var(color_std))

        # --- Step 4: 灰度直方图平滑性检测 ---
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist / np.sum(hist)
        hist_diff = np.mean(np.abs(np.diff(hist.squeeze())))
        # hist_diff 越大，说明灰度分布波动越强（画面不平滑）

        # --- Step 5: 综合判断 ---
        is_flower = (
                lap_var > laplacian_var_threshold or
                color_var > color_var_threshold or
                hist_diff > hist_diff_threshold
        )

        # 综合置信度 = 三项归一化后的简单平均
        norm_lap = min(lap_var / laplacian_var_threshold, 1.0)
        norm_color = min(color_var / color_var_threshold, 1.0)
        norm_hist = min(hist_diff / hist_diff_threshold, 1.0)
        flower_score = round((norm_lap + norm_color + norm_hist) / 3, 3)

        return bool(is_flower), flower_score

    @staticmethod
    def image_green_frame_detect(image: P_Image.Image,
                                 green_ratio_threshold: float = 2,
                                 green_mean_threshold: float = 80.0) -> (bool, float):
        """
        检测图像是否为绿帧（Green Frame）

        :param image: PIL.Image 对象
        :param green_ratio_threshold: G 通道相对 R/B 通道的倍数阈值
        :param green_mean_threshold: G 通道平均亮度下限
        :return: (is_green, green_ratio)
                 - is_green: bool 是否绿帧
                 - green_ratio: float G 通道相对强度（越大越偏绿）
        """
        if not isinstance(image, P_Image.Image):
            logger.warning("image must be of type PIL.Image.Image")
            return None, -1.0

        # 转为 NumPy 数组
        image_np = np.array(image.convert("RGB"), dtype=np.uint8)

        # 计算各通道平均亮度
        mean_r = float(np.mean(image_np[:, :, 0]))
        mean_g = float(np.mean(image_np[:, :, 1]))
        mean_b = float(np.mean(image_np[:, :, 2]))

        # 计算绿色相对强度比
        green_ratio = mean_g / (np.mean([mean_r, mean_b]) + 1e-5)

        # 判定是否绿帧
        is_green = mean_g > green_mean_threshold and green_ratio > green_ratio_threshold

        return bool(is_green), round(float(green_ratio), 3)

    @staticmethod
    def comparison_ssim_image(
            image_1: P_Image.Image,
            image_2: P_Image.Image,
            resize: bool = True,
            use_color: bool = False,
            threshold: float = 0.9
    ) -> (bool, float):
        """
        计算两张图片的结构相似度（SSIM），并根据阈值判断是否相似

        :param image_1: PIL.Image 对象1
        :param image_2: PIL.Image 对象2
        :param resize: 若两张图尺寸不同，是否自动缩放到相同大小
        :param use_color: 是否使用彩色图进行SSIM比较（默认False使用灰度）
        :param threshold: 相似度阈值（默认0.9），相似度>=此值视为“相似”
        :return: (is_similar, similarity)
                 - is_similar: bool 是否相似
                 - similarity: float 相似度 [0, 1]
        """
        # Step 1: 尺寸对齐
        if resize and image_1.size != image_2.size:
            image_2 = image_2.resize(image_1.size)

        # Step 2: 转换为数组
        if use_color:
            img1 = np.array(image_1.convert('RGB'))
            img2 = np.array(image_2.convert('RGB'))
            similarity = ssim(img1, img2, channel_axis=-1)
        else:
            img1 = np.array(image_1.convert('L'))
            img2 = np.array(image_2.convert('L'))
            similarity = ssim(img1, img2)

        # Step 3: 结果判断
        similarity = round(float(similarity), 4)
        is_similar = similarity >= threshold

        return is_similar, similarity
