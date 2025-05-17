import json
import logging
import queue
import random

from appium import webdriver
import time

from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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
            self.scroll_and_scrape()
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



    def _typecollectionview(self):
        element = self.driver.find_element(By.XPATH,
                                      '//XCUIElementTypeApplication[@name="拼多多"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeScrollView/XCUIElementTypeCollectionView')
        print(element.tag_name)
        return element

    def _proudct_price(self):
        view=self._typecollectionview()
        cells = view.find_elements(By.XPATH, 'XCUIElementTypeCell') # CELLS 是商品信息组
        # for c in cells:
     #     print(c.tag_name)
        # print('*' * 20)
        # print('0cells')
        product_price=[]
        for cell in cells:
            insidecells = cell.find_elements(By.XPATH, '//XCUIElementTypeOther')
            if len(insidecells) > 7:
                product_name = insidecells[7].get_attribute('name')  # 得到商品名
            else:
                product_name = None
                # 检查 insidecells 是否为空
            if insidecells:
                text = insidecells[-1].find_elements(By.XPATH, 'XCUIElementTypeStaticText')  # 得到一堆文本
                price = [i.text for i in text]
            else:
                price = []
            product_price.append((product_name, price))
        return product_price

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
                product_price=self._proudct_price()
                time2=time.time()
                print(counter)
                timecost=time2-time1
                print(timecost)
                counter+=1

                self._save_to_json(product_price, self.output_file)
                logging.info(f"✅ 完成抓取，共获取 {len(product_price)} 个文本，已保存到 {self.output_file}")
                print(f"✅ 完成抓取，共获取 {len(product_price)} 个文本，已保存到 {self.output_file}")
                # 2. 执行随机滑动

                self.scroll()


            except Exception as e:
                logging.error(f"⚠️ 滚动/抓取失败: {str(e)}")
                print(f'scroll and scape: {str(e)}')
                break


    def _save_to_json(self, snapshotlist, filename):
        """保存到 JSON 文件"""
        with open(filename, "a", encoding="utf-8") as f:
            json.dump(snapshotlist, f, ensure_ascii=False, indent=2)

#%%
collector=DataCollector('duoduocream')
collector.start()

