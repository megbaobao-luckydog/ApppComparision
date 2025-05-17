import pandas as pd
import os
from ai import BeautyProductEnhancer  # 假设这是您的AI处理类

# 常量定义
INPUT_DIR = "/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/douyin/platform_data"
INTERIM_DIR = "/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data/douyin/platform_top_500_data"
AI_OUTPUT_DIR = "/processed_data/douyin/ai_cleaned_data"

# 文件映射配置（包含列名转换规则）
FILE_CONFIGS = {
    'creamnlotion': {
        'filename': '新抖-乳液面霜.xlsx',
        'nrows': 1000,
        'columns': {'商品标题': 'product', '售价': 'price'}
    },
    'mask': {
        'filename': '新抖-面膜.xlsx',
        'nrows': 500,
        'columns': {'商品标题': 'product', '售价': 'price'}
    },
    'serum': {
        'filename': '新抖-精华.xlsx',
        'nrows': 500,
        'columns': {'商品标题': 'product', '售价': 'price'}
    }
}


def preprocess_data(df, column_mapping):
    """数据预处理：列名转换和基础清洗"""
    # 列名转换
    df = df.rename(columns=column_mapping)

    # 价格处理（移除货币符号并转为数值）
    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).str.replace('[¥￥,]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # 商品名称处理
    if 'product' in df.columns:
        df['product'] = df['product'].str.strip()

    return df


def process_with_ai(input_path, output_path):
    """使用AI模块处理数据"""
    print(f"\n正在使用AI处理数据: {input_path} → {output_path}")
    enhancer = BeautyProductEnhancer()
    enhancer.process_and_save(input_path,output_path)  # 假设process()是执行处理的方法
    print(f"AI处理完成，结果已保存至: {output_path}")


def main_pipeline():
    """完整数据处理流程"""
    # 创建输出目录
    os.makedirs(INTERIM_DIR, exist_ok=True)
    os.makedirs(AI_OUTPUT_DIR, exist_ok=True)

    processed_dfs = {}

    for name, config in FILE_CONFIGS.items():
        print(f"\n正在处理 {name} 数据...")

        # 1. 读取原始数据
        raw_path = os.path.join(INPUT_DIR, config['filename'])
        df = pd.read_excel(raw_path, nrows=config['nrows'])

        # 2. 数据预处理
        df = preprocess_data(df, config['columns'])

        # 3. 保存预处理数据（供AI处理使用）
        interim_path = os.path.join(INTERIM_DIR, f"{name}.csv")
        df.to_csv(interim_path, index=False)
        print(f"预处理数据已保存: {interim_path}")

        # 4. AI处理
        ai_output_path = os.path.join(AI_OUTPUT_DIR, f"{name}_cleaned.csv")
        process_with_ai(interim_path, ai_output_path)

        # 存储处理后的DataFrame
        processed_dfs[name] = df

    print("\n所有数据处理完成！")
    return processed_dfs


if __name__ == '__main__':
    final_data = main_pipeline()

    # 示例：查看其中一个处理后的DataFrame
    print("\n乳液面霜数据示例:")
    print(final_data['creamnlotion'][['product', 'price']].head())

