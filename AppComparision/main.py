import os
from typing import re

from matplotlib import pyplot as plt
import pandas as pd
from visual import *

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
#%%
from merge_data import DataMerger
df=DataMerger().load_and_merge_data()
df.drop_duplicates(inplace=True)


#%%
'''以下都是可视化， 本来的设计是所有的绘图过程都封装到visual包中进行调用， 但因为工作量较大， 有的直接展示在本文档中未进行封装'''


#%%

'''统计不平平台数据量'''
platform_counts = df['platform'].value_counts().sort_values()

# 然后绘制柱状图
platform_counts.plot(kind='bar', color='skyblue', figsize=(10,5))
plt.title('data count from differnet app')
plt.xlabel('app')
plt.ylabel('product count')
plt.xticks(rotation=45)
plt.show()

#%%
'''不同平台价格对比'''
#价格处理
def strict_price_extraction(ref_price):
    """严格提取纯数字价格（确保仅含数字和最多1个小数点）"""
    if pd.isna(ref_price):
        return None

    # 统一处理特殊字符
    s = str(ref_price).strip().replace('¥', '').replace('￥', '').replace('元', '')

    # 核心正则：匹配纯数字（可含小数点，但不含任何其他字符）
    match = re.fullmatch(r'\d+\.?\d*', s.split('/')[0].strip())
    return float(match.group()) if match else None


def validate_prices(df):
    """执行严格价格验证并生成报告"""
    # 提取价格并标记无效记录
    df['extracted_price'] = df['参考价格'].apply(strict_price_extraction)
    df['is_valid'] = ~df['extracted_price'].isna()

    # 生成验证报告
    valid_count = df['is_valid'].sum()
    invalid_samples = df[~df['is_valid']]['参考价格'].unique()[:5]  # 展示前5个无效样例

    print(f"验证结果：\n"
          f"- 总记录数：{len(df)}\n"
          f"- 有效价格记录：{valid_count} ({valid_count / len(df):.1%})\n"
          f"- 无效样例：{list(invalid_samples)}\n")

    return df[df['is_valid']].copy()  # 返回仅含有效价格的DataFrame


# 执行验证
clean_df = validate_prices(df)

# 验证后分析（确保所有价格均为纯数字）
print("有效价格示例（前5条）：")
print(clean_df[['参考价格', 'extracted_price']].head().to_string(index=False))

#对不同平台价格数据进行加工和可视化

def generate_platform_price_data(clean_df):
    """
    为每个平台生成标准price_data格式

    参数:
        clean_df: 必须包含列 'platform' 和 'extracted_price'

    返回:
        dict: {平台名: price_data列表}
    """
    # 定义价格分段标准（可根据业务需求调整）
    bins = [0, 200, 500, 1000, float('inf')]
    labels = ["经济型", "中端", "高端", "豪华"]

    # 生成区间显示文本（与bins对应）
    range_texts = [
        "<¥200",
        "¥200-500",
        "¥500-1000",
        "¥1000+"
    ]

    # 按平台分组处理
    platform_results = {}

    for platform, group in clean_df.groupby('platform'):
        # 跳过空平台
        if pd.isna(platform):
            continue

        # 分组统计
        counts = pd.cut(
            group['extracted_price'],
            bins=bins,
            labels=labels,
            right=False
        ).value_counts().reindex(labels, fill_value=0)

        # 计算百分比
        total = counts.sum()
        percentages = (counts / total * 100).round(1)

        # 构建标准price_data格式
        platform_results[platform] = [
            (labels[i], range_texts[i], int(counts.iloc[i]), float(percentages.iloc[i]))
            for i in range(len(labels))
        ]

    return platform_results


# 使用示例（接续之前的清洗步骤）
platform_price_data = generate_platform_price_data(clean_df)

output_dir = 'platform_price_distributions'
os.makedirs(output_dir, exist_ok=True)

# 批量处理每个平台
for platform, price_data in platform_price_data.items():
    try:
        # 调用可视化函数（传入平台名称）
        plot_price_distribution(price_data,title=platform)

        # 保存图表
        filename = f"{platform}_price_distribution.png"
        plt.savefig(
            os.path.join(output_dir, filename),
            bbox_inches='tight',
            dpi=300
        )
        plt.close()
        print(f"✅ 已保存: {filename}")

    except Exception as e:
        print(f"❌ {platform} 处理失败: {str(e)}")

print(f"\n所有图表已保存至: {os.path.abspath(output_dir)}")

#%%
'''产地分布'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 假设df是原始数据
plt.figure(figsize=(15, 8))

# 1. 按平台分组统计产地
platform_country = df.groupby(['platform', '品牌产地']).size().unstack().fillna(0)

# 2. 标准化处理（显示百分比）
platform_percent = platform_country.div(platform_country.sum(axis=1), axis=0) * 100

# 3. 绘制堆叠柱状图
platform_percent.plot(kind='bar',
                     stacked=True,
                     colormap='tab20',
                     width=0.8,
                     edgecolor='white')

# 4. 图表美化
plt.title('各平台品牌产地分布对比', fontsize=16, pad=20)
plt.xlabel('平台', fontsize=12)
plt.ylabel('占比(%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), title='品牌产地')

# 5. 添加数据标签
for platform in platform_percent.index:
    cumulative = 0
    for country in platform_percent.columns:
        value = platform_percent.loc[platform, country]
        if value > 5:  # 只显示占比超过5%的标签
            plt.text(platform_percent.index.get_loc(platform),
                    cumulative + value/2,
                    f'{value:.1f}%',
                    ha='center',
                    va='center',
                    fontsize=10)
        cumulative += value

plt.tight_layout()
plt.show()
#%%

#%%
'''功效处理'''


# 数据清洗
df_clean = df[['platform', '功效']].dropna().copy()  # 保留平台和功效列

# 规范功效格式
df_clean['功效'] = (df_clean['功效'].str.replace('，', '+')
                    .str.replace(' ', '')
                    .str.replace('＋', '+')
                    .str.strip('+'))

# 拆分功效为列表
df_clean['功效列表'] = df_clean['功效'].str.split('\+')

#全平台功效词库
# 获取所有唯一功效词
all_effects = set()
for effects in df_clean['功效列表']:
    all_effects.update(effects)

print(f"发现{len(all_effects)}种独特功效：")
print(sorted(all_effects))

#全平台矩阵
# 创建空矩阵
platforms = df_clean['platform'].unique()
effect_matrix = pd.DataFrame(0, index=platforms, columns=sorted(all_effects))

# 填充矩阵
for platform in platforms:
    platform_effects = []
    for effects in df_clean[df_clean['platform'] == platform]['功效列表']:
        platform_effects.extend(effects)

    counter = Counter(platform_effects)
    for effect, count in counter.items():
        effect_matrix.loc[platform, effect] = count

# 计算百分比
effect_matrix_pct = effect_matrix.div(effect_matrix.sum(axis=1), axis=0) * 100

plt.figure(figsize=(16, 12))

# 筛选Top20功效（按总频次）
top_effects = effect_matrix.sum(axis=0).sort_values(ascending=False).head(20).index

# 调整热力图参数
sns.heatmap(
    effect_matrix_pct[top_effects].T,  # 转置使功效在Y轴
    cmap="YlGnBu",
    annot=True,
    fmt=".1f",
    linewidths=0.3,
    cbar_kws={'label': '占比(%)', 'shrink': 0.5},
    annot_kws={'size': 9},
    vmax=30  # 统一颜色标尺
)

# 美化标签
plt.title('各平台Top20功效分布（优化版）', fontsize=14, pad=20)
plt.xlabel('平台', fontsize=12)
plt.ylabel('功效', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('optimized_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()



