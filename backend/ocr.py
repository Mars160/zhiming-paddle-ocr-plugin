import logging

from paddleocr import PaddleOCR

model = PaddleOCR(use_angle_cls=True, use_gpu=False)


def ocr(img):
    logging.warning('start')
    ocr_result = model.ocr(img, cls=True)[0]
    result = []
    for i in ocr_result:
        result.append(i[1][0])
    logging.warning(result)
    return result
