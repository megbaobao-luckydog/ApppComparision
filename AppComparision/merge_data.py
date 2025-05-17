import pandas as pd
import os
import re

#%%
'''合并lotion和cream'''
import os
import glob
import pandas as pd
'''
# 基础路径（使用通配符*匹配所有平台）
base_path = '/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data'
ai_dirs = glob.glob(os.path.join(base_path, '*/ai_cleaned_data'))

for ai_dir in ai_dirs:
    try:
        # 提取平台名称（从路径中获取父目录名）
        platform = os.path.basename(os.path.dirname(ai_dir))

        # 构建文件路径
        cream_path = os.path.join(ai_dir, 'cream.csv')
        lotion_path = os.path.join(ai_dir, 'lotion.csv')
        output_path = os.path.join(ai_dir, 'lotionncream.csv')

        # 检查文件是否存在
        if not (os.path.exists(cream_path) and os.path.exists(lotion_path)):
            print(f'[{platform}] 缺少 cream.csv 或 lotion.csv，跳过')
            continue

        # 读取并合并文件
        cream_df = pd.read_csv(cream_path)
        lotion_df = pd.read_csv(lotion_path)
        merged_df = pd.concat([cream_df, lotion_df], ignore_index=True)

        # 保存结果
        merged_df.to_csv(output_path, index=False)
        print(f'[{platform}] 成功合并 -> lotionncream.csv（{len(merged_df)}行）')

    except Exception as e:
        print(f'[{platform}] 处理失败: {str(e)}')

print(f'处理完成！共处理 {len(ai_dirs)} 个平台')
'''


# 基础路径配置
BASE_DIR = "/Users/mac/PycharmProjects/AppComparision/pythonProject2/processed_data"
AI_CLEANED_DIR = "ai_cleaned_data"

# 平台配置
PLATFORM_CONFIGS = [
    {
        'name': 'amazon',
        'files': {
            'mask': {'filename': 'mask.csv', 'nrows': 500},
            'serum': {'filename': 'serum.csv', 'nrows': 500},
            'lotionncream':{'filename':'lotionncream.csv','nrows':1000}
        }
    },
    {
        'name': 'douyin',
        'files': {
            'mask': {'filename': 'mask.csv', 'nrows': 500},
            'serum': {'filename': 'serum.csv', 'nrows': 500},
            'lotionncream': {'filename': 'lotionncream.csv', 'nrows': 1000}
        }
    },
    {
        'name': 'pinduoduo',
        'files': {
            'mask': {'filename': 'mask.csv', 'nrows': 500},
            'serum': {'filename': 'serum.csv', 'nrows': 500}
        }
    },
    {
        'name': 'JD',
        'files': {
            'mask': {'filename': 'mask.csv', 'nrows': 500},
            'serum': {'filename': 'serum.csv', 'nrows': 500},
            'lotionncream': {'filename': 'lotionncream.csv', 'nrows': 1000}
        }
    },
    {
        'name': 'taobao',
        'files': {
            'mask': {'filename': 'mask.csv', 'nrows': 500},
            'serum': {'filename': 'serum.csv', 'nrows': 500},
            'lotionncream': {'filename': 'lotionncream.csv', 'nrows': 1000}
        }
    },
{
        'name': 'red',
        'files': {
            'mask': {'filename': 'mask.csv', 'nrows': 500},
            'serum': {'filename': 'serum.csv', 'nrows': 500},
            'lotionncream': {'filename': 'lotionncream.csv', 'nrows': 1000}
        }
    },

]


class DataMerger:
    """多平台数据合并处理器"""

    @staticmethod
    def get_file_path(platform: str, filename: str) -> str:
        """构建完整文件路径"""
        return os.path.join(BASE_DIR, platform, AI_CLEANED_DIR, filename)

    @staticmethod
    def load_and_merge_data() -> pd.DataFrame:
        """加载并合并所有平台数据"""
        data_frames = []

        for platform_config in PLATFORM_CONFIGS:
            platform = platform_config['name']

            for category, file_config in platform_config['files'].items():
                file_path = DataMerger.get_file_path(platform, file_config['filename'])
                try:
                    # 读取CSV文件
                    df = pd.read_csv(file_path, nrows=file_config['nrows'])
                    # 添加平台和类别标记
                    df['platform'] = platform
                    df['category'] = category
                    data_frames.append(df)

                    print(f"成功加载 {platform}/{category} 数据")
                except Exception as e:
                    print(f"加载 {platform}/{category} 数据失败: {str(e)}")

        # 合并所有DataFrame
        if data_frames:
            return pd.concat(data_frames, ignore_index=True)
        return pd.DataFrame()

