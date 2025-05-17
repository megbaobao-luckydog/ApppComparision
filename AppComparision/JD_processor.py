import pandas as pd
import json
import re
import os


class JDCleansingPipeline:
    def __init__(self, keyword):
        self.keyword = keyword
        self.input_file = f'/platform_comparision/JD/extracted_data/{keyword}.json'
        self.data_cleaned1 = f'/Users/mac/python_projects/src/platform_comparision/JD/wait4ai/{keyword}.csv'
        self.temp_file = f'/Users/mac/python_projects/src/platform_comparision/JD/wait4ai/{keyword}_temp.csv'
        self.data_cleaned2 = f'/Users/mac/python_projects/src/platform_comparision/JD/cleaned_data{keyword}.csv'

    def clean_data(self, df_sorted):
        """执行多步骤数据清洗"""
        # 步骤1: 删除包含特定字符的行
        df_filtered = df_sorted[
            ~(df_sorted['text'].str.contains('｜', na=False) |
              df_sorted['text'].str.contains('店', na=False))
        ]

        # 步骤2: 删除高频无意义文本
        value_counts = df_filtered['text'].value_counts().reset_index()
        value_counts.columns = ['text_value', 'count']
        meaningless_texts = set(value_counts[value_counts['count'] >= 5]['text_value'])
        df_filtered['ifmeaningless'] = df_filtered['text'].apply(lambda x: x not in meaningless_texts)
        df_filtered_removed = df_filtered[df_filtered['ifmeaningless'] == True]

        # 步骤3: 清理与价格相关的字段
        pattern = r"[\u4e00-\u9fa5]+[¥￥]\d+(?:\.\d+)?"
        matched_rows = df_filtered_removed[~df_filtered_removed["text"].str.contains(pattern, regex=True)]

        # 步骤4: 处理连续价格
        df_one_price = self.filter_consecutive_prices(matched_rows)

        # 步骤5: 重置索引
        df_one_price.reset_index(inplace=True)

        # 步骤6: 提取商品和价格对
        price_pattern = r'¥\d+(\.\d+)?'
        mask = df_one_price['text'].str.contains(price_pattern, regex=True)
        price_indices = df_one_price[mask].index.tolist()
        product_indices = [i - 1 for i in price_indices]

        selected_values = [
            [df_one_price['text'].iloc[b], df_one_price['text'].iloc[c]]
            for b, c in zip(product_indices, price_indices)
        ]

        df = pd.DataFrame(selected_values, columns=['product', 'price'])
        df.to_csv(self.data_cleaned1)
        return df

    def clean_data(self, df_sorted):
        """执行多步骤数据清洗"""
        # 步骤1: 删除包含特定字符的行
        df_filtered = df_sorted[
            ~(df_sorted['text'].str.contains('｜', na=False) |
              df_sorted['text'].str.contains('店', na=False))
        ]

        # 步骤2: 删除高频无意义文本
        value_counts = df_filtered['text'].value_counts().reset_index()
        value_counts.columns = ['text_value', 'count']
        meaningless_texts = set(value_counts[value_counts['count'] >= 5]['text_value'])
        df_filtered['ifmeaningless'] = df_filtered['text'].apply(lambda x: x not in meaningless_texts)
        df_filtered_removed = df_filtered[df_filtered['ifmeaningless'] == True]

        # 步骤3: 清理与价格相关的字段
        pattern = r"[\u4e00-\u9fa5]+[¥￥]\d+(?:\.\d+)?"
        matched_rows = df_filtered_removed[~df_filtered_removed["text"].str.contains(pattern, regex=True)]

        # 步骤4: 处理连续价格
        df_one_price = self.filter_consecutive_prices(matched_rows)

        # 步骤5: 重置索引
        df_one_price.reset_index(inplace=True)

        # 步骤6: 提取商品和价格对
        price_pattern = r'¥\d+(\.\d+)?'
        mask = df_one_price['text'].str.contains(price_pattern, regex=True)
        price_indices = df_one_price[mask].index.tolist()
        product_indices = [i - 1 for i in price_indices]

        selected_values = [
            [df_one_price['text'].iloc[b], df_one_price['text'].iloc[c]]
            for b, c in zip(product_indices, price_indices)
        ]

        df = pd.DataFrame(selected_values, columns=['product', 'price'])
        df.to_csv(self.data_cleaned1)
        return df

    @staticmethod
    def filter_consecutive_prices(df):
        """处理连续价格，保留每组中的第一个"""

        def is_price(text):
            if pd.isna(text):
                return False
            return bool(re.match(r'^[¥￥]\d+(\.\d{1,2})?$', str(text)))

        df['is_price'] = df['text'].apply(is_price)
        df['group'] = (df['is_price'] != df['is_price'].shift()).cumsum()
        df['to_keep'] = True

        for group_id, group in df.groupby('group'):
            if group['is_price'].all() and len(group) > 1:
                df.loc[group.index[1:], 'to_keep'] = False

        return df[df['to_keep']].drop(columns=['is_price', 'group', 'to_keep'])

    def clean_csv_line(self, line):
        """清理CSV行中的JSON结构"""
        if line.strip().startswith('"text":'):
            try:
                json_part = line[line.find('{'):line.rfind('}') + 1]
                data = json.loads(json_part)
                return data.get('text', '').replace(',', '，')
            except:
                return line.strip('", \n')
        return line.strip('", \n')




