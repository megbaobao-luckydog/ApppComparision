
#%%
import json
import queue
import threading
from datetime import time
import logging
import random
import time
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from datacollectorbase import DataCollectorBase

#%%
class DataCollector(DataCollectorBase):
    def __init__(self):
        super().__init__()

    def scroll_and_scrape(self, max_scrolls=300):

        # 初始化文件， 避免追加
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        """滚动并抓取商品信息"""
        counter = 1

        for scroll_attempt in range(max_scrolls):
            try:
                time1 = time.time()
                # 1. 获取当前页面快照
                snapshot = self._get_element_snapshot()
                time2 = time.time()
                print(counter)
                print(f'snapshot:{snapshot}')
                timecost = time2 - time1
                print(timecost)
                counter += 1

                self._save_to_json(snapshot, self.output_file)
                logging.info(f"✅ 完成抓取，共获取 {len(snapshot)} 个文本，已保存到 {self.output_file}")
                print(f"✅ 完成抓取，共获取 {len(snapshot)} 个文本，已保存到 {self.output_file}")
                # 2. 执行随机滑动
                self.scroll()

            except Exception as e:
                logging.error(f"⚠️ 滚动/抓取失败: {str(e)}")
                print(f'scroll and scape: {str(e)}')
                break

        def _get_element_snapshot(self):
            """获取元素快照"""
            snapshot = []
            try:
                collection_view = self.driver.find_element(By.XPATH,
                                                           '//XCUIElementTypeApplication[@name="JD"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView')  # iOS
                # collection_view = driver.find_element(By.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")  # Android
                elements = collection_view.find_elements(By.XPATH, '//XCUIElementTypeStaticText[@visible="true"]')

                for elem in elements:
                    try:
                        snapshot.append({
                            "text": elem.get_attribute("value") or elem.get_attribute("name") or "",
                            "location": elem.location
                        })
                    except:
                        continue

                logging.info(f"📸 获取到 {len(snapshot)} 个有效元素快照")
                return snapshot

            except Exception as e:
                logging.error(f"⚠️ 获取快照时出错: {str(e)}")
                return []


#%%
collector = DataCollector('cream')
collector.start()



