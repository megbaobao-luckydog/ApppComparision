import os
import cv2
import pytesseract




def process_image_and_ocr(snapshot_path):

    BASE_PATH = '/Users/mac/python_projects/src/platform_comparision/taobao/screenshot'

    image = cv2.imread(snapshot_path)
    base_image = image.copy()

    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 去除噪声
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # 二值化
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # 形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    # 保存处理后的图片
    processed_image_path = "/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_dilated.png"
    cv2.imwrite(processed_image_path, dilate)

    # 设置 Tesseract 路径
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

    # 只识别中英文
    LANGUAGES = 'chi_sim+eng'

    # 查找轮廓
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

    # 遍历轮廓
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h > 200 and w > 250:
            roi = base_image[y:y + h, x:x + w]
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

    # 保存标记后的图片
    marked_image_path = "/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_boxes.png"
    cv2.imwrite(marked_image_path, image)

    # 进行 OCR 识别
    ocr_result_original = pytesseract.image_to_string(base_image, lang=LANGUAGES)

    # 处理输出文本，使其结构更整齐
    lines = ocr_result_original.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    neat_output = "\n".join(cleaned_lines)

    return neat_output



