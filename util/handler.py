import os

from PIL import Image

from util.setter import argsetter


class ImageHandler:

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

    @classmethod
    def text_is_image(cls, text, input_image_path):
        """
        检测图片中是否包含指定文本
        :param text: 要检测的文字
        :param input_image_path: 图片路径
        :return: (bool, ocr_text)
        """
        from paddleocr import PaddleOCR

        det_model_dir = (argsetter.base_dir + os.sep + 'libs' + os.sep +
                         'official_models' + os.sep + 'PP-OCRv5_server_det')
        rec_model_dir = (argsetter.base_dir + os.sep + 'libs' + os.sep +
                         'official_models' + os.sep + 'PP-OCRv5_server_rec')

        ocr = PaddleOCR(
            text_detection_model_dir=det_model_dir,
            text_recognition_model_dir=rec_model_dir,
            use_textline_orientation=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
        )

        result = ocr.predict(input_image_path)

        ocr_text = ""
        for line in result:
            rec_text_list = line.get("rec_texts", [])
            ocr_text += " ".join(rec_text_list)
        # 判断目标文本是否包含在识别结果中
        res = text in ocr_text

        return res, ocr_text
