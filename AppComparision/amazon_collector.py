import csv
import json
import queue
import threading
from datetime import time
import logging
import random
import time
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from datacollectorbase import DataCollectorBase
from datetime import datetime

#%%
class DataCollector(DataCollectorBase):
    def __init__(self):
        super().__init__()

    def scroll_and_scrape(self, times=300):
        global res
        count = 1
        while count <= times:
            time1=time.time()
            res = self.extract()
            print(res)
            time2=time.time()
            print(time2-time1)
            self.scroll()
            self.scroll()
            count += 1

    def extract(self):
        xpath = '//XCUIElementTypeOther[@name="亚马逊海外购"]/XCUIElementTypeOther[4]'

        # 从文件加载上次处理进度
        last_processed = self.load_progress()
        visible_texts = []
        processed_count = 0

        try:
            print(f'定位容器元素')
            container = self.driver.find_element(By.XPATH, xpath)

            # 根据上次进度构建XPath（从上次位置+1开始）
            start_pos = last_processed + 1 if last_processed else 1
            subxpath = f'.//XCUIElementTypeOther[position() >= {start_pos} and position() <= {start_pos + 49}]'

            print(f'查找子容器（从位置 {start_pos} 开始）')
            sub_containers = container.find_elements(By.XPATH, subxpath)
            print(f'找到 {len(sub_containers)} 个子容器')

            for i, sub_container in enumerate(sub_containers):
                # 计算当前绝对位置
                current_pos = start_pos + i

                try:
                    # 提取文本元素
                    text_elements = sub_container.find_elements(By.CLASS_NAME, 'XCUIElementTypeStaticText')

                    for text_elem in text_elements:
                        text = text_elem.text.strip()
                        if text:
                            print(f"提取文本: {text}")
                            visible_texts.append(text)

                except StaleElementReferenceException:
                    print(f"元素过期，跳过位置 {current_pos}")
                    continue  # 直接跳过当前元素

                # 每处理10个元素保存一次进度
                if current_pos % 10 == 0:
                    self.save_progress(current_pos)
                    print(f"已保存进度：位置 {current_pos}")

            # 全部处理完成后保存最终进度
            if sub_containers:
                final_pos = start_pos + len(sub_containers) - 1
                self.save_progress(final_pos)
                print(f"本轮处理完成，保存进度：位置 {final_pos}")

            # 写入CSV（追加模式）
            if visible_texts:
                with open('lotion.csv', 'a') as f:
                    f.write('\n'.join(visible_texts) + '\n')

            return visible_texts

        except NoSuchElementException:
            print("未找到元素")
            return []

    def load_progress(self):
        """从文件加载上次处理的位置"""
        try:
            with open('progress.txt', 'r') as f:
                position = int(f.read().strip())
                print(f"加载进度：从位置 {position} 继续")
                return position
        except (FileNotFoundError, ValueError, TypeError):
            print("未找到进度文件或进度无效，从头开始")
            return 0  # 默认从头开始

    def save_progress(self, position):
        """保存当前处理的位置到文件"""
        with open('progress.txt', 'w') as f:
            f.write(str(position))

    def get_last_processed_position(self):
        """从文件中读取上次处理的最后一个元素的位置"""
        try:
            with open('last_position.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return None

    def save_last_processed_position(self, position):
        """保存当前处理的最后一个元素的位置"""
        with open('last_position.txt', 'w') as f:
            f.write(str(position))

