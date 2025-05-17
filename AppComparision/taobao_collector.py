# import json
#
# from PIL.Image import Image
#
import json
import os

# from ocrmac import ocrmac
#
# annotations = ocrmac.OCR(snapshot_path).recognize()
# print(annotations)
#
#
# #%%
# import easyocr
# import cv2
# from matplotlib import pyplot as plt
# import numpy as np
# snapshot_path='/Users/mac/python_projects/src/platform_comparision/crawler_project/lotion/test.png'
# # reader=easyocr.Reader(['ch_sim'],gpu=False)
# # result=reader.readtext(snapshot_path)
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
#
# import easyocr
# reader = easyocr.Reader(['ch_sim'], gpu=False)  # 再次尝试初始化
#
# #%%
# import pytesseract
# import cv2
# import re
#
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
#
#
# def extract_price(text):
#     """从文本中提取价格（支持¥符号和纯数字格式）"""
#     price_match = re.search(r'¥(\d+\.?\d*)|\d+\.?\d*', text)
#     return price_match.group(0) if price_match else None
#
#
# def extract_products(image_path):
#     """从商品列表图片中提取商品名称和价格"""
#     # 读取图片并转换为灰度图
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     # 使用阈值处理增强文字清晰度
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#
#     # 定义各元素识别区域（示例比例）
#     regions = {
#         "导航栏": (0, 0, 100, 80),  # 顶部状态栏
#         "商品列表": (0, 120, 100, 900),  # 主体内容区
#         "价格区": (40, 20, 60, 30)  # 价格标签区域
#     }
#
#     # 批量识别函数
#     def extract_elements(image):
#         results = {}
#         for key, (top, left, height, width) in regions.items():
#             cropped = image.crop((left, top, left + width, top + height))
#         results[key] = pytesseract.image_to_string(cropped, lang='chi_sim+eng')
#         return results



#
#     # 使用Tesseract OCR提取文本（设置中文语言）
#     text = pytesseract.image_to_string(thresh, lang='chi_sim+eng')
#
#     # 分割商品条目（根据商品之间的空行或分隔线）
#     items = re.split(r'\n{2,}|\-{5,}', text.strip())
#
#     products = []
#     for item in items:
#         # 提取商品名称（通常在价格之前）
#         name = re.sub(r'\n.*', '', item).strip()  # 取第一行文本
#         price = extract_price(item)
#
#         if name and price:
#             products.append({
#                 'name': name,
#                 'price': price
#             })
#
#     return products
#
#
# # 使用示例（替换为实际图片路径）
#
# products = extract_products(snapshot_path)
#
# # 输出结果
# for idx, product in enumerate(products, 1):
#     print(f"商品 {idx}:")
#     print(f"名称: {product['name']}")
#     print(f"价格: {product['price']}")
#     print("-" * 30)

#%%
# import cv2
# import pytesseract
# import re
# import os
# from PIL.Image import Image
# import pytesseract
# from PIL import Image
# import cv2
# import re
# import os
# import numpy as np
#
# snapshot_path='/Users/mac/python_projects/src/platform_comparision/crawler_project/lotion/test.png'
#
# # ===== 配置优化 =====
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# LANGUAGES = 'chi_sim+eng'  # 支持中文和英文混合识别
# OCR_CONFIG = f'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.￥'  # 优化识别准确率
#
#
# # ===== 核心函数优化 =====
# def extract_price(text):
#     """增强版价格提取，支持多种格式"""
#     # 正则表达式升级，支持更多货币符号和格式
#     price_patterns = [
#         r'￥([\d.]+)',  # 人民币格式（标准）
#         r'¥([\d.]+)',  # 人民币符号变体
#         r'(\d{1,3}(?:,\d{3})*\.\d{2})',  # 带千位分隔符
#         r'(?:\d+[\.,]?\d*)元',  # 中文元格式
#         r'(?:\d+[\.,]?\d*)块'  # 口语化表达
#     ]
#     for pattern in price_patterns:
#         match = re.search(pattern, text)
#     if match: return match.group(1).replace(',', '')
#     return None
#
#
# def extract_products(image_path):
#     """优化后的商品信息提取"""
#     # 预处理增强
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     # 自适应阈值处理（针对复杂背景）
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
#
#     # 精准区域定位（根据图片实际布局调整）
#     regions = {
#         "导航栏": (0, 0, 400, 100),  # 灰色状态栏区域
#         "商品列表": (0, 100, 900, 800),  # 主内容区
#         "价格区": (350, 150, 120, 50)  # 价格标签精确区域
#     }
#
#     results = {}
#     for key, (top, left, width, height) in regions.items():
#         cropped = thresh[top:top + height, left:left + width]  # 使用阈值处理后的图像
#     text = pytesseract.image_to_string(
#         Image.fromarray(cropped),
#         lang=LANGUAGES,
#         config=OCR_CONFIG
#     ).strip()
#     results[key] = text
#     return results
#
#
# # ===== 扩展功能实现 =====
# def parse_product_info(text_block):
#     """结构化解析商品信息"""
#     info = {
#         'title': '',
#         'price': None,
#         'sales': None,
#         'shop': None
#     }
#
#     # 标题提取（取最长文本块）
#     lines = [line for line in text_block.split('') if line.strip()]
#     info['title'] = max(lines, key=len).strip()
#
#     # 价格提取
#     price_match = re.search(r'￥\d+\.?\d*', text_block)
#     info['price'] = price_match.group(0) if price_match else None
#
#     # 销量提取
#     sales_match = re.search(r'(?:[人|件|单]+收货|销量)[:：]\s*(\d+\.?\d*)', text_block)
#     info['sales'] = sales_match.group(1) if sales_match else None
#
#     # 店铺提取
#     shop_match = re.search(r'(?:官方|品牌|天猫)[官方|品牌]+旗舰店', text_block, re.I)
#     info['shop'] = shop_match.group(0).strip() if shop_match else '未知店铺'
#
#     return info
#
#
# # ===== 完整执行流程 =====
# if __name__ == "__main__":
#     # # 创建保存目录
#     # os.makedirs('output', exist_ok=True)
#     #
#     # # 处理所有图片
#     # for img_file in os.listdir('input'):
#     #     if not img_file.endswith('.jpg'):
#     #         continue
#     #
#     # img_path = os.path.join('input', img_file)
#     result = extract_products(snapshot_path)
#
#     # 解析结构化信息
#     # products = []
#     # text_blocks = result['商品列表'].split('') # 按换行分割不同商品
#     # for block in text_blocks:
#     #     if not block.strip():
#     #         continue
#     #
#     # product_info = parse_product_info(block)
#     # if product_info['price']:
#     #     products.append(product_info)
#
#     # # 保存结果
#     # with open(f'output/{img_file}.json', 'w', encoding='utf-8') as f:
#     #     json.dump(products, f, ensure_ascii=False, indent=2)
#     # print(f'已处理: {img_file} → 识别{len(products)}个商品')
#     print(result)

#%%
# import cv2
# import pytesseract
# import re
# from PIL import Image
#
# # 配置
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# LANGUAGES = 'chi_sim+eng'
# OCR_CONFIG = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.￥'
#
#
# def extract_all_text(image_path):
#     """提取图片中所有文本及其坐标"""
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
#
#     # 定义整个图片为区域
#     regions = {
#         "全部内容": (0, 0, img.shape[1], img.shape[0])
#     }
#
#     results = {}
#     for key, (top, left, width, height) in regions.items():
#         cropped = thresh[top:top + height, left:left + width]
#         text = pytesseract.image_to_data(
#             Image.fromarray(cropped),
#             lang=LANGUAGES,
#             config=OCR_CONFIG,
#             output_type=pytesseract.Output.DICT
#         )
#
#         # 解析每个文字块的坐标和内容
#         for i in range(len(text['text'])):
#             x, y, w, h = text['left'][i], text['top'][i], text['width'][i], text['height'][i]
#             content = text['text'][i].strip()
#             if content:  # 过滤空白字符
#                 results[(x, y, x + w, y + h)] = content
#
#     return results
#
#
# def main():
#     # img_path = "product_list.jpg"  # 替换为实际路径
#     all_text = extract_all_text(snapshot_path)
#
#     print("所有文本及其坐标：")
#     for (x1, y1, x2, y2), text in all_text.items():
#         print(f"坐标: ({x1},{y1})-({x2},{y2}) | 内容: {text}")
#
#
# if __name__ == "__main__":
#     main()

#%%
import pytesseract
import re
from PIL import Image
import cv2
# 配置
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
LANGUAGES = 'chi_sim+eng'
OCR_CONFIG = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.￥'

# 打开图片
# image = Image.open(snapshot_path)  # 请将 'your_image.jpg' 替换为实际图片路径
img = cv2.imread(snapshot_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)


#%%
from PIL import Image
im=Image.open(snapshot_path)
print(im)
im.show()
#%% preprocessing
img=cv2.imread(snapshot_path)
cv2.imshow('original image',img)
cv2.waitKey(0)

#%%
import matplotlib.pyplot as plt
import pytesseract
import re
from PIL import Image
import cv2
snapshot_path='/Users/mac/python_projects/src/platform_comparision/crawler_project/lotion/test.png'
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    height, width, depth = im_data.shape
    figsize = width / float(dpi), height / float(dpi)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(im_data, cmap='gray')
    plt.show()

display(snapshot_path)

#%%
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_image = grayscale(img)
cv2.imshow('/Users/mac/python_projects/src/platform_comparision/crawler_project/gray.jpg', gray_image)

#%%
image = cv2.imread(snapshot_path)
base_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))
dilate = cv2.dilate(thresh, kernal, iterations=1)
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_dilated.png", dilate)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
LANGUAGES = 'chi_sim+eng'
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if h > 200 and w > 250:
        roi = base_image[y:y+h, x:x+w]
        cv2.rectangle(image, (x,y), (x+w, y+h), (36, 255, 12), 2)

cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_boxes.png", image)
True
ocr_result_original = pytesseract.image_to_string(base_image)
print(ocr_result_original)

#%%
import cv2
import pytesseract

image = cv2.imread(snapshot_path)
base_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))
dilate = cv2.dilate(thresh, kernal, iterations=1)
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_dilated.png", dilate)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# 修改为只识别英文
LANGUAGES = 'chi_sim+eng'
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 250:
        roi = base_image[y:y + h, x:x + w]
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_boxes.png", image)
ocr_result_original = pytesseract.image_to_string(base_image, lang=LANGUAGES)
print(ocr_result_original)

#%%
import cv2
import pytesseract

image = cv2.imread(snapshot_path)
base_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))  # 修正变量名从 'kernal' 到 'kernel'
dilate = cv2.dilate(thresh, kernel, iterations=1)
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_dilated.png", dilate)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
LANGUAGES = 'chi_sim+eng'  # 修改为只识别中英文
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 250:
        roi = base_image[y:y + h, x:x + w]
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_boxes.png", image)
ocr_result_original = pytesseract.image_to_string(base_image, lang=LANGUAGES)
print(ocr_result_original)

#%%
import cv2
import pytesseract
import numpy as np


# 读取图片
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
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_dilated.png", dilate)

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
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_boxes.png", image)

# 进行 OCR 识别
ocr_result_original = pytesseract.image_to_string(base_image, lang=LANGUAGES)
print(ocr_result_original)

#%%
import cv2
import pytesseract
import numpy as np



# 读取图片
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
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_dilated.png", dilate)

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
cv2.imwrite("/Users/mac/python_projects/src/platform_comparision/crawler_project/sample_boxes.png", image)

# 进行 OCR 识别
ocr_result_original = pytesseract.image_to_string(base_image, lang=LANGUAGES)

# 处理输出文本，使其结构更整齐
lines = ocr_result_original.splitlines()
cleaned_lines = [line.strip() for line in lines if line.strip()]
neat_output = "\n".join(cleaned_lines)

print(neat_output)
#%%

product_pattern = re.compile(r'([^¥\n]+)?¥(\d+(?:\.\d+)?)[\s\S]*?([^>]+旗舰店)?')
matches = product_pattern.findall(neat_output)
# 输出结果
for product, price, store in matches:
    print(f"商品名: {product.strip()}")
    print(f"价格: ¥{price}")
    print(f"店铺: {store.strip()}")
    print()


#%%
import json
import queue
import threading
from datetime import time, datetime
import logging
import random
import time
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os



class DataCollector():
    """同步数据采集器（含多线程存储）"""

    def __init__(self,keyword):
        self.queue = queue.Queue()
        # self.storage_thread = StorageThread(self.queue)
        self.driver = None
        self.running = False
        self.list_element=None
        # self.LOCATOR_NAVIGATION_ELEMENT = (By.XPATH, '//XCUIElementTypeOther[@name="亚马逊海外购"]//XCUIElementTypeOther['
        #                                              '@name="商品列表"]')
        # self.LOCATOR_PRODUCTS = (By.XPATH, '//XCUIElementTypeOtherStaticText[contains(@name, "乳液")]')
        self.output_file=f'/Users/mac/python_projects/src/platform_comparision/crawler_project/{keyword}.json'

    def start(self):
        """启动采集服务"""
        logging.info("[采集器] 已启动")
        self.running = True
        try:
            self._init_driver()
            # self.scroll()
            # # self._navigate_to_list()
            self.scroll_and_scrape()
            # self.check_session()
            # self._collect_products()
        except KeyboardInterrupt:
            logging.info("[采集器]用户中断采集")
        except Exception as e:
            logging.error(f"[采集器] 启动过程中出错: {str(e)}")
        finally:
            self.stop()

    def stop(self):
        """停止采集服务"""
        self.running = False
        if self.driver:
            self.driver.quit()
        # self.storage_thread.stop()

    def _init_driver(self):
        """初始化Appium驱动"""
        options = XCUITestOptions().load_capabilities({
            "platformName": "iOS",
            "automationName": "XCUITest",
            "udid": "00008110-000A49811E01401E",
            # "bundleId": "com.amazon.AmazonCN",
            "newCommandTimeout": 300,
            "wdaStartupRetries": 3,
            "simpleIsVisibleCheck": True
        })
        self.driver = webdriver.Remote('http://localhost:4723', options=options)
        self.wait = WebDriverWait(self.driver, 10)
        print("[数据采集器] WebDriver 已启动")

    def scroll(self):
        # 随机决定滑动起始位置， 滑动幅度， 和停留时间
        window = self.driver.get_window_size()
        start_x = window['width'] * (0.45 + random.random() * 0.1)
        start_y = window['height'] * (0.75 + random.random() * 0.1)
        end_x = window['width'] * (0.45 + random.random() * 0.1)
        end_y = window['height'] * (0.15 + random.random() * 0.1)

        self.driver.execute_script('mobile: swipe', {
            'direction': 'up',
            'velocity': random.randint(600, 1000),
            'startX': start_x,
            'startY': start_y,
            'endX': end_x,
            'endY': end_y,
            'duration': random.randint(800, 1200)
        })

        # 横向滑动
        # if random.random() < 0.2:
        #     self.driver.execute_script('mobile: swipe', {
        #         'direction': random.choice(['left', 'right']),
        #         'duration': random.randint(300, 600)
        #     })

    def scroll_and_scrape(self, max_scrolls=300):

        #初始化文件， 避免追加
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        """滚动并抓取商品信息"""
        counter=1

        for scroll_attempt in range(max_scrolls):
            try:
                time1=time.time()
                # 1. 获取当前页面快照
                self.take_screenshots()
                time2=time.time()
                timecost=time2-time1
                print(timecost)
                counter+=1
                self.scroll()

            except Exception as e:
                logging.error(f"⚠️ 滚动/抓取失败: {str(e)}")
                print(f'scroll and scape: {str(e)}')
                break

    def take_screenshots(self,
                         save_dir="/Users/mac/python_projects/src/platform_comparision/crawler_project/serum"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 去掉最后3位毫秒
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)

        try:
            # 检查保存目录是否存在，如果不存在则创建
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            # 使用完整的文件路径保存截图
            if self.driver.save_screenshot(filepath):
                print(f"截图已保存到: {filepath}")
            else:
                print("截图保存失败")
        except Exception as e:
            logging.error(f"截图时出错: {str(e)}")



                #
    # def _save_to_json(self, snapshotlist, filename):
    #     """保存到 JSON 文件"""
    #     with open(filename, "a", encoding="utf-8") as f:
    #         json.dump(snapshotlist, f, ensure_ascii=False, indent=2)

#%%
collector = DataCollector('taobaoserum')
collector.start()
#%%
