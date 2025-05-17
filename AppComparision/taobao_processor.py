import os
import pandas as pd
os.chdir('/Users/mac/python_projects/src/platform_comparision/taobao')
import logging
import configparser
config = configparser.ConfigParser()
config.read('/Users/mac/python_projects/src/platform_comparision/taobao/config.ini')
#%%
keyword=input('产品类型')

extracted_data = f'/Users/mac/python_projects/src/platform_comparision/taobao/extracted_data/{keyword}.txt'
#从图片中提取的数据

cleaned_data1= f'/Users/mac/python_projects/src/platform_comparision/taobao/cleaned_data1/{keyword}.csv'
#去掉banneer 后的数据

cleaned_data2=f'/Users/mac/python_projects/src/platform_comparision/taobao/cleaned_data2/{keyword}.csv'
#人工清洗的数据

cleaned_data3=f'/Users/mac/python_projects/src/platform_comparision/taobao/cleaned_data3/{keyword}.csv'
#AI 清洗的数据

cleaned_data4=f'/Users/mac/python_projects/src/platform_comparision/taobao/ai_cleaned_data/{keyword}.csv'
#分析前的清洗
#%%
'''
-------extracted_data---------
(step1:图片按时间戳排序
step2: 提取图片中的文字) 上一步已完成
-------cleaned_data1----------
step3: 去除文本中的重复banner
step4: 在文本的第一行+ 店>
step5: 生成初步处理好的文本

'''
from utils.removebanner import clean_text

clean_text(extracted_data, cleaned_data1)


#%%
''' 
----------cleaned_data2----------------
人工清洗
step1: 分隔商品信息（连个店铺之间的就是某一个特定商品的信息）
step2: 在每个商品信息内查找价格信息
step3: 保留每个商品， 价格及价格之前的信息， 分别为商品信息和价格信息
'''

from utils import products_seperation

mannul_clean=products_seperation.products_seperation(cleaned_data1)
mannul_clean_df=pd.DataFrame(mannul_clean, columns=['product','price'])
mannul_clean_df.to_csv(cleaned_data2, index=False,encoding='utf-8')
#%%

'''
----------cleaned_data3---------------
AI 清洗
使用deepseek接口
'''

from utils.AI_cleanser import BeautyProductEnhancer  # 假设BeautyProductEnhancer类在your_module.py文件中

# 创建BeautyProductEnhancer实例
enhancer = BeautyProductEnhancer()

# 定义输入文件和输出文件路径
input_file = cleaned_data2
output_file = cleaned_data3

# 调用process_and_save方法进行处理和保存
enhancer.process_and_save(input_file, output_file)


#%%
'''-----ai_cleaned_data---------
将AI清洗后的数据进行进一步清洗， 方便分析使用

'''
# import pandas as pd
# import os
#
# folder_path = 'cleaned_data3'  # 替换为你的文件夹路径
# dataframes = {}  # 用字典存储数据框
#
# for file_name in os.listdir(folder_path):
#     if file_name.endswith('.csv'):
#         file_path = os.path.join(folder_path, file_name)
#         try:
#             df = pd.read_csv(file_path)
#             # 用文件名（去掉扩展名）作为键
#             key = os.path.splitext(file_name)[0]
#             dataframes[key] = df
#
#             # 打印基本信息
#             print(f"文件名: {file_name}")
#             print(f"形状: {df.shape}")
#             print(f"列名: {df.columns.tolist()}")
#             print(f"空值情况：\n{df.isnull().sum()}\n")
#         except Exception as e:
#             print(f"读取文件 {file_name} 时出错: {e}")

# 访问数据框示例
# print(dataframes['your_filename_without_extension'])
import pandas as pd
import os

folder_path = '/Users/mac/python_projects/src/platform_comparision/taobao/cleaned_data3'  # 替换为你的文件夹路径
dataframes = {}  # 用字典存储处理后的数据框
cleaned_data4=f'/Users/mac/python_projects/src/platform_comparision/taobao/ai_cleaned_data/{keyword}.csv'
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 删除 "产品全称" 列为空值的行
            df_cleaned = df.dropna()

            # 存储到字典（可选）
            key = os.path.splitext(file_name)[0]
            dataframes[key] = df_cleaned

            # 打印基本信息（可选）
            print(f"文件名: {file_name}")
            print(f"原始行数: {len(df)}")
            print(f"删除空值后行数: {len(df_cleaned)}")
            print(f"剩余列名: {df_cleaned.columns.tolist()}\n")
            print(f"空值情况{df_cleaned.isna().sum()}\n")

        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {e}")

# 访问处理后的数据框（示例）
# print(dataframes['your_filename_without_extension'])


#%%
import pandas as pd
import os

folder_path = '/Users/mac/python_projects/src/platform_comparision/taobao/cleaned_data3'
output_folder = '/Users/mac/python_projects/src/platform_comparision/taobao/ai_cleaned_data'

os.makedirs(output_folder, exist_ok=True)

columns_to_keep = ['原始价格', '产品全称', '品牌', '产品线', '品类', '昵称', '功效', '参考价格', '品牌产地']

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # 读取CSV文件，并只选择需要的列
            df = pd.read_csv(file_path)

            # 只保留存在的列（防止列名错误）
            available_columns = [col for col in columns_to_keep if col in df.columns]
            df = df[available_columns]

            # 检查 "产品全称" 是否在选择的列中
            if '产品全称' in df.columns:
                df_cleaned = df.dropna(subset=['产品全称'])  # 仅删除 "产品全称" 为空的行
            else:
                print(f"警告：文件 {file_name} 没有 '产品全称' 列")
                df_cleaned = df.copy()  # 如果列名错误，保留原数据

            # 保存处理后的数据
            output_file_path = os.path.join(output_folder, file_name)
            df_cleaned.to_csv(output_file_path, index=False)

            # 打印基本信息
            print(f"文件名: {file_name}")
            print(
                f"原始行数: {len(pd.read_csv(file_path)) if '产品全称' in pd.read_csv(file_path).columns else 'N/A'}")  # 注意：这里可能不准确
            print(f"删除空值后行数: {len(df_cleaned)}")
            print(f"剩余列名: {df_cleaned.columns.tolist()}\n")
            print(f"空值情况:\n{df_cleaned.isna().sum()}\n")

        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {e}")




#%%

''''AI  清洗优化， 较为麻烦， 暂不优化'''




'''
@lru_cache(maxsize=500)
def cached_api_call(product: str, price: str) -> str:
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": COMMAND_TEMPLATE + "\n请严格按以下格式返回：产品全称,品牌,产品线,品类,昵称,功效,参考价格,品牌产地"
            },
            {
                "role": "user",
                "content": f"产品：{product} | 价格：{price}"
            }
        ],
        temperature=0.3
    )
    # token 监控
    print(f"本次消耗Token：{response.usage.total_tokens}")
    return response.choices[0].message.content


async def async_call(row: Dict[str, Any]) -> Dict[str, Any]:
    try:
        product = row['product']
        price = row['price']
        result = cached_api_call(product, price)
        csv_data = result.strip().split(',')
        if len(csv_data) != 8:
            raise ValueError("返回数据列数不正确")
        return {
            "原始产品名": product,
            "原始价格": price,
            "产品全称": csv_data[0],
            "品牌": csv_data[1],
            "产品线": csv_data[2],
            "品类": csv_data[3],
            "昵称": csv_data[4],
            "功效": csv_data[5],
            "参考价格": csv_data[6],
            "品牌产地": csv_data[7]
        }
    except Exception as e:
        print(f"处理失败: {product}，错误：{str(e)}")
        return {
            "原始产品名": product,
            "原始价格": price,
            "error": str(e)
        }


async def process_batch(batch):
    tasks = [async_call(row) for row in batch]
    return await asyncio.gather(*tasks)


def batch_processing(df: pd.DataFrame) -> pd.DataFrame:
    batch_size = 10  # 可根据实际情况调整批量大小
    results = []
    total = len(df)
    for i in range(0, total, batch_size):
        batch = df[i:i + batch_size].to_dict('records')
        loop = asyncio.get_event_loop()
        batch_results = loop.run_until_complete(process_batch(batch))
        results.extend(batch_results)
        # 进度显示
        current_idx = min(i + batch_size, total)
        print(f"进度: {current_idx}/{total} ({current_idx / total:.1%})")
    return pd.DataFrame(results)

# 执行处理
enhanced_df = batch_processing(df)

# 保存结果（保留原始列+新列）
enhanced_df.to_csv(final_path, index=False, encoding='utf_8_sig')  # 保证中文兼容性

# 生成处理报告
success_count = enhanced_df[enhanced_df['原始产品全称'].notna()].shape[0]
print(f"\n处理完成！成功率：{success_count}/{len(df)} ({success_count / len(df):.1%})")
print(f"结果文件已保存至：{final_path}")
'''