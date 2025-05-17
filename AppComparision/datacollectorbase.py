import json
import queue
import threading
from abc import abstractmethod
from datetime import time
import logging
import random
import time
import pandas as pd
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DataCollectorBase():
    """同步数据采集器（含多线程存储）"""

    def __init__(self):
        self.queue = queue.Queue()
        # self.storage_thread = StorageThread(self.queue)
        self.driver = None
        self.running = False
        self.list_element = None
        # self.LOCATOR_NAVIGATION_ELEMENT = (By.XPATH, '//XCUIElementTypeOther[@name="亚马逊海外购"]//XCUIElementTypeOther['
        #                                              '@name="商品列表"]')


    def start(self):
        """启动采集服务"""
        logging.info("[采集器] 已启动")
        self.running = True
        try:
            self._init_driver()
            self.scroll_and_scrape()
            self.is_session_valid()
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
    @abstractmethod
    def scroll_and_scrape(self):
        pass

    def is_session_valid(self):
        try:
            # 尝试获取当前上下文（简单操作验证会话）
            self.driver.contexts
            return True
        except Exception as e:
            print(f"会话失效: {e}")
            return False





