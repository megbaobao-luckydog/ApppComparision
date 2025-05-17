import re

import pandas as pd
import json

from fontTools.subset import subset

from utils import amazon_page_processing
#%%
'''清洗lotion文件'''
# Read the raw text file
file_path = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/extracted_data/lotion.csv'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract product-price pairs using regex
pattern = r'(.+?)\s*¥(\d+\.?\d*)'  # Matches: (product text) ¥(price)
matches = re.findall(pattern, text)

# Create a DataFrame and save as CSV
df = pd.DataFrame(matches, columns=['product', 'price'])
output_path = ('/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/cleaned_data/lotion.csv')
df.to_csv(output_path, index=False, encoding='utf-8')

print("CSV saved successfully!")
print(df.head())  # Preview the first 5 rows

#%%
'''处理其他文件'''

import pandas as pd

# 路径配置
input_path = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/extracted_data'
file_names = ["cream", "mask", "serum"]  # 要处理的文件名（不带.csv后缀）
output_path = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/cleaned_data'

# 处理每个文件
for file in file_names:
    # 读取CSV文件（跳过第一行，不读取表头）
    df = pd.read_csv(f"{input_path}/{file}.csv", header=None, skiprows=1)

    # 提取第二列作为 product 列，并添加 price 列（默认值100）
    df = df[[1]].rename(columns={1: 'product'})
    df['price'] = 100  # 直接赋值为100（整列统一）

    # 去除 product 列的前后空格
    df['product'] = df['product'].str.strip()

    # 保存为新的CSV文件
    df.to_csv(f"{output_path}/{file}_cleaned.csv", index=False)

print("处理完成！生成的文件已保存至:", output_path)


#%%
'''AI 处理'''
import os
from ai import BeautyProductEnhancer  # Make sure this module is in your Python path

# Configure paths
input_dir = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/cleaned_data'
output_dir = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/ai_cleaned_data'

# Initialize the enhancer
b = BeautyProductEnhancer()

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process all files in input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv') or filename.endswith('.txt'):  # Process both CSV and text files
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, f"enhanced_{filename}")

        try:
            b.process_and_save(input_file, output_file)
            print(f"Successfully processed {filename} -> enhanced_{filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

print("All files processed!")

#%%
path='/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/extracted_data'
file_name=["cream","mask","serum"]
columns=['product_name','price']
new_column_names=['product','price']
#进行去product 列去控制， 如重复值
output_path='/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/cleaned_data'

#%%
class AMCleansingPipeline:
    # 类属性（所有实例共享）
    BASE_DATA_PATH = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/extracted_data'


    def __init__(self, keyword):
        self.keyword = keyword
        # 实例特有的路径（基于类属性构建）
        self.extracted_data = f'{self.BASE_DATA_PATH}/{keyword}.json'
        self.data_cleaned1 = f'{self.BASE_CLEAN_PATH}/{keyword}.csv'
        self.temp_file = f'{self.BASE_CLEAN_PATH}/{keyword}_temp.csv'
        self.data_cleaned2 = f'{self.BASE_CLEAN_PATH}/cleaned_data{keyword}.csv'

    @classmethod
    def load_and_preprocess(cls, keyword):
        """类方法版本，无需实例化即可调用"""
        # 使用类属性构建路径
        input_path = f'{cls.BASE_DATA_PATH}/{keyword}.json'

        # 读取和处理数据
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        df_raw = pd.json_normalize(data)
        print('原始数据:', df_raw.shape)
        return amazon_page_processing.process_dataframe(df_raw)

    @classmethod
    def remove_consecutive_duplicates(cls,df, column_name):

        if column_name not in df.columns:
            raise ValueError(f"列 '{column_name}' 不存在于DataFrame中")

        # 标记非连续重复的行
        mask = df[column_name] != df[column_name].shift(1)

        # 应用筛选
        return df[mask].reset_index(drop=True)

    @classmethod
    def split_series_by_threshold(cls, df, column_name):
        threshold = 220

        # 拆分数据并重置索引
        df_left = df[df[column_name] < threshold].reset_index(drop=True)
        df_right = df[df[column_name] >=threshold].reset_index(drop=True)

        # 水平拼接
        result = pd.concat([df_left, df_right], axis=1)

        # 添加后缀区分
        result.columns = [f'{col}_≤{threshold}' if idx < len(df_left.columns)
                          else f'{col}_>{threshold}'
                          for idx, col in enumerate(result.columns)]

        return result


    @classmethod
    def filter_location_x(cls, df):
        if 'location.x' not in df.columns:
            raise ValueError("DataFrame中缺少'location.x'列")
        copy=df.copy()
        # 添加标记列
        copy['is_target_x'] = copy['location.x'].isin([18, 220])
        copy['x_type'] = copy['location.x'].apply(
            lambda x: 'x_18' if x == 18 else ('x_220' if x == 220 else None)
        )
        return copy[copy['is_target_x']==True]

    @classmethod
    def pivot_18_220(df, x_col='location.x', group_cols=['location.y', 'page']):
        # 筛选出18和220的数据
        filtered = df[df[x_col].isin([18, 220])].copy()

        # 添加标记列
        filtered['x_type'] = filtered[x_col].apply(lambda x: 'x_18' if x == 18 else 'x_220')

        # 使用pivot_table进行透视
        pivoted = filtered.pivot_table(
            index=group_cols,
            columns='x_type',
            values=[x_col] + [col for col in df.columns if col not in [x_col] + group_cols],
            aggfunc='first'  # 取第一个匹配的值
        )

        # 扁平化多级列索引
        pivoted.columns = [f'{col[0]}_{col[1]}' if col[1] else col[0] for col in pivoted.columns]

        # 重置索引
        result = pivoted.reset_index()

        return result

    @classmethod
    def filter_price(cls,df,column):
        cleaned_df = df[~df[column].str.startswith('¥', na=False)]
        return cleaned_df

df1=AMCleansingPipeline.load_and_preprocess('amazon_lotion')
df2=AMCleansingPipeline.filter_location_x(df1)
df3=AMCleansingPipeline.split_series_by_threshold(df2,'location.x')
df4=AMCleansingPipeline.filter_price(df3,'text_≤220')
df5=df4.drop_duplicates(subset=['text_≤220'])
df5.to_csv('/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/amazon/extracted_data/lotion.csv')
#%%
''''''




#%%
    #
    # def clean_data(self, df_sorted):
    #     """执行多步骤数据清洗并返回最终DataFrame"""
    #     # 步骤1: 删除包含特定字符的行
    #     df_filtered = df_sorted[
    #         ~(df_sorted['text'].str.contains('｜', na=False) |
    #           df_sorted['text'].str.contains('店', na=False))
    #     ]
    #
    #     # 步骤2: 删除高频无意义文本
    #     value_counts = df_filtered['text'].value_counts().reset_index()
    #     value_counts.columns = ['text_value', 'count']
    #     meaningless_texts = set(value_counts[value_counts['count'] >= 5]['text_value'])
    #     df_filtered['ifmeaningless'] = df_filtered['text'].apply(lambda x: x not in meaningless_texts)
    #     df_filtered_removed = df_filtered[df_filtered['ifmeaningless'] == True]
    #
    #     # 步骤3: 清理与价格相关的字段
    #     pattern = r"[\u4e00-\u9fa5]+[¥￥]\d+(?:\.\d+)?"
    #     matched_rows = df_filtered_removed[~df_filtered_removed["text"].str.contains(pattern, regex=True)]
    #
    #     # 步骤4: 处理连续价格
    #     df_one_price = self._process_prices(matched_rows)
    #
    #     # 步骤5: 提取商品和价格对
    #     price_pattern = r'¥\d+(\.\d+)?'
    #     mask = df_one_price['text'].str.contains(price_pattern, regex=True)
    #     price_indices = df_one_price[mask].index.tolist()
    #     product_indices = [i - 1 for i in price_indices]
    #
    #     selected_values = [
    #         [df_one_price['text'].iloc[b], df_one_price['text'].iloc[c]]
    #         for b, c in zip(product_indices, price_indices)
    #     ]
    #
    #     df = pd.DataFrame(selected_values, columns=['product', 'price'])
    #     return df
    #
    # def _process_prices(self, df):
    #     """内部方法：处理价格数据"""
    #     # 重置索引确保顺序
    #     df = df.reset_index(drop=True)
    #
    #     # 标记价格行
    #     df['is_price'] = df['text'].apply(lambda x: bool(re.match(r'^[¥￥]\d+(\.\d{1,2})?$', str(x))))
    #
    #     # 分组连续价格
    #     df['group'] = (df['is_price'] != df['is_price'].shift()).cumsum()
    #     df['to_keep'] = True
    #
    #     # 处理每组价格
    #     for group_id, group in df.groupby('group'):
    #         if group['is_price'].all() and len(group) > 1:
    #             df.loc[group.index[1:], 'to_keep'] = False
    #
    #     # 返回清理后的数据
    #     return df[df['to_keep']].drop(columns=['is_price', 'group', 'to_keep'])
    #
    # def process_and_save(self, df_sorted):
    #     """整合处理流程并保存结果"""
    #     # 执行清洗流程
    #     cleaned_df = self.clean_data(df_sorted)
    #
    #     # 保存中间结果
    #     cleaned_df.to_csv(self.data_cleaned1, index=False)
    #
    #     # 执行去重处理
    #     self._deduplicate_file(self.data_cleaned1, self.temp_file)
    #
    #     # 返回处理后的DataFrame
    #     return pd.read_csv(self.temp_file)
    #
    # def _deduplicate_file(self, input_path, output_path):
    #     """内部方法：文件去重处理"""
    #     # 读取并清理行数据
    #     with open(input_path, 'r', encoding='utf-8') as f:
    #         cleaned_lines = [self.clean_csv_line(line) for line in f]
    #
    #     # 去重并写入临时文件
    #     with open(output_path, 'w', encoding='utf-8') as f:
    #         seen = set()
    #         for line in cleaned_lines:
    #             if line not in seen:
    #                 seen.add(line)
    #                 f.write(line + '\n')




#%%



