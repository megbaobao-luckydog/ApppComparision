import json
import os
import queue
import threading
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
os.chdir('/Users/mac/python_projects/src/platform_comparision/crawler_project')

#%%


from datacollectorbase import DataCollectorBase


df_product_price = pd.DataFrame(columns=['product', 'price'])

class DataCollector(DataCollectorBase):
    def __init__(self):
        super().__init__()

    def scroll_and_scrape(self, times=300):
        global df_product_price
        count = 1
        while count <= times:
            time1=time.time()
            res = self.extract()
            time2=time.time()
            print(time2-time1)
            df_temp = pd.DataFrame(res, columns=["product", "price"])
            df_product_price = pd.concat([df_product_price, df_temp], axis=0, ignore_index=True)
            self.scroll()
            count += 1

    def extract(self):
        def generate_xpath_produt(index):
            return f'(//XCUIElementTypeOther[@name="lynxview"])[{index}]/XCUIElementTypeOther/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther'

        def generate_xpath_price(index):
            return f'(//XCUIElementTypeOther[@name="lynxview"])[{index}]/XCUIElementTypeOther/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]'

        path_list = []
        for i in range(1, 4):
            path_product = generate_xpath_produt(i)
            path_price = generate_xpath_price(i)
            path_list.append((path_product, path_price))

        product_price_list = []
        for a, b in path_list:
            try:
                sub_text_product = self.driver.find_element(By.XPATH, a)
                element_product = sub_text_product.find_element(By.CLASS_NAME, 'XCUIElementTypeStaticText')
                product = element_product.text

                sub_text_price = self.driver.find_element(By.XPATH, b)
                elements_price = sub_text_price.find_elements(By.CLASS_NAME, 'XCUIElementTypeStaticText')
                for i in range(0, len(elements_price)):
                    if '¥' in elements_price[i].text:
                        price = elements_price[i - 1].text
                        continue
                product_price_list.append((product, price))
            except NoSuchElementException:
                break
        return product_price_list


#%%
collector=DataCollector()
collector.start()
#%%
df_product_price=df_product_price.dropna(subset=['product'])

#%%
keyword=input()
df_product_price.to_csv(f'/Users/mac/python_projects/src/platform_comparision/douyin/{keyword}.csv')




