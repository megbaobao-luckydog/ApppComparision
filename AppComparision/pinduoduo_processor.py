import pandas as pd
import json
import re
import os
from typing import List, Dict
from dataclasses import dataclass
from ai import BeautyProductEnhancer

# ======================
# 配置层（明确分离人工和AI输出路径）
# ======================
@dataclass
class Config():
    keyword: str
    input_dir: str = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/pinduoduo/extracted_data'
    human_output_dir: str = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/pinduoduo/cleaned_data'
    ai_output_dir: str = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/pinduoduo/ai_cleaned_data'

    @property
    def input_json(self) -> str:
        return f"{self.input_dir}/{self.keyword}.json"

    @property
    def cleaned_csv(self) -> str:
        return f"{self.human_output_dir}/{self.keyword}_human.csv"

    @property
    def ai_cleaned_csv(self) -> str:
        return f"{self.ai_output_dir}/{self.keyword}_ai.csv"


# ======================
# 清洗模块（人工处理部分）
# ======================
class HumanDataCleaner:
    """人工清洗流程（无临时文件）"""

    @classmethod
    def full_clean_pipeline(cls, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        完整人工清洗流程：
        1. 基础清洗 -> 2. 结构化提取 -> 3. 内存去重
        """
        # 管道式处理
        return (raw_df
                .pipe(cls._check_raw_df)
                # .pipe(cls._remove_junk_rows)
                # .pipe(cls._filter_high_freq_text)
                # .pipe(cls._handle_prices)
                # .pipe(cls._extract_products)
                .pipe(cls._deduplicate))


    @classmethod
    def _check_raw_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        """检查并打印原始数据的基本信息"""
        print(f"数据基本信息：")
        df.info()
        print(f"数据前几行：\n{df.head().to_string()}")
        return df

    @staticmethod
    def _remove_junk_rows(df: pd.DataFrame) -> pd.DataFrame:
        """删除含无效标记的行"""
        return df[~df['product'].str.contains('｜|店', regex=True, na=False)]

    @staticmethod
    def _filter_high_freq_text(df: pd.DataFrame) -> pd.DataFrame:
        """基于词频过滤"""
        freq = df['product'].value_counts()
        return df[~df['product'].isin(freq[freq >= 5].index)]

    @staticmethod
    def _handle_prices(df: pd.DataFrame) -> pd.DataFrame:
        """价格字段处理"""
        df['is_price'] = df['text'].str.match(r'^[¥￥]\d+(\.\d+)?$', na=False)
        df['group'] = (~df['is_price']).cumsum()

        # 标记每组保留第一个价格
        keep_mask = df.groupby('group')['is_price'].transform(
            lambda x: ~x.duplicated() if x.all() else True
        )
        return df[keep_mask].drop(columns=['is_price', 'group'])

    @staticmethod
    def _extract_products(df: pd.DataFrame) -> pd.DataFrame:
        """提取商品-价格对"""
        price_mask = df['text'].str.contains(r'[¥￥]\d+', na=False)
        price_indices = df[price_mask].index

        products = []
        for idx in price_indices:
            if idx > 0:  # 确保有商品名
                clean_price = re.sub(r'[^¥￥\d.]', '', df['text'].iloc[idx])
                products.append({
                    'product': df['text'].iloc[idx - 1],
                    'price': clean_price,
                    'raw_text': df['text'].iloc[idx]  # 保留原始文本供AI处理
                })
        return pd.DataFrame(products)

    @staticmethod
    def _deduplicate(df: pd.DataFrame) -> pd.DataFrame:
        """联合去重"""
        return df.drop_duplicates(subset=['product'])


# ======================
# AI处理模块
# ======================
class AIDataProcessor:
    """AI专用处理流程"""

    @classmethod
    def process_and_save(cls, input_data, output_path: str):
        """
        处理数据并保存结果

        参数:
            input_data: 输入数据，可以是DataFrame或其他格式
            output_path: 输出文件路径
        """

        # 2. 使用增强器处理
        enhancer = BeautyProductEnhancer()
        enhanced_data = enhancer.process_and_save(input_data, output_path)

        # 3. 保存结果
        enhanced_data.to_csv(output_path, index=False)
        print(f"数据已成功保存到: {output_path}")



# ======================
# 主控制器
# ======================
class DataPipeline:
    def __init__(self, config: Config):
        self.cfg = config
        self._prepare_dirs()

    def _prepare_dirs(self):
        """确保输出目录存在"""
        os.makedirs(self.cfg.human_output_dir, exist_ok=True)
        os.makedirs(self.cfg.ai_output_dir, exist_ok=True)

    def execute(self):
        """执行完整流程"""
        # 1. 加载原始数据
        with open(self.cfg.input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        processed_data = []

        for item in data:
            product_name = item[0] or "无商品名称"
            price_info = item[1]

            if price_info:
                price = f"{price_info[0]}{price_info[1]}"
            else:
                price = "暂无报价"

            processed_data.append({"product": product_name, "price": price})

        raw_df = pd.DataFrame(processed_data)

        raw_df = raw_df[raw_df['product'] != '无商品名称']

        print(raw_df.head())

        # 2. 人工清洗并保存
        cleaned = HumanDataCleaner.full_clean_pipeline(raw_df)
        cleaned.to_csv(self.cfg.cleaned_csv, index=False)
        print(f"人工清洗结果已保存至: {self.cfg.cleaned_csv}")

        # 3. AI处理并保存
        AIDataProcessor.process_and_save(self.cfg.cleaned_csv, self.cfg.ai_cleaned_csv)
        print(f"AI处理结果已保存至: {self.cfg.ai_cleaned_csv}")


# ======================
# 执行入口
# ======================
if __name__ == '__main__':
    pipeline = DataPipeline(Config(keyword='serum'))
    pipeline.execute()


