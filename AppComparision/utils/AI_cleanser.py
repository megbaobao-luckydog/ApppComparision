# 设置 API 密钥和基础 URL
import openai
from __init__ import *
import re
import pandas as pd
import os
import pandas as pd
import openai
import concurrent.futures
import time
from typing import Dict, Any

import openai
import pandas as pd
import concurrent.futures
from typing import Dict, Any


class BeautyProductEnhancer:
    def __init__(self):
        openai.api_key = "sk-78874d584e774f33acdf731ec55ce04a"
        openai.base_url = "https://api.deepseek.com"

        self.COMMAND_TEMPLATE = """
根据以下规则处理美妆产品数据：

【处理规则】
1. 产品全称：联想市场认可度最高的明星产品
   - 示例：玫瑰面霜 → 兰蔻菁纯玫瑰面霜
2. 品牌：提取官方品牌名称
3. 产品线：提取产品系列名称（如"菁纯"）
4. 品类：标准化品类名称（面霜/精华等）
5. 昵称：收集市场通用昵称
6. 功效：按官网描述提炼关键词（最多3个）
7. 参考价格：单位规格价格（格式：¥XXX/50ml）
8. 品牌产地：标注国家/地区

请按以下CSV格式返回结果（不要表头）：
{产品全称},{品牌},{产品线},{品类},{昵称},{功效},{参考价格},{品牌产地}

示例：
兰蔻菁纯玫瑰面霜,兰蔻,菁纯,面霜,菁纯面霜,抗老+滋润,¥895/50ml,法国
"""

    def enhance_product_data(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """增强单行数据"""
        try:
            # 动态生成prompt
            dynamic_prompt = f"{self.COMMAND_TEMPLATE}\n当前需要处理的词：{row['product']}（价格：{row['price']}）"

            response = openai.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是美妆行业数据分析专家，严格按照要求格式返回数据"},
                    {"role": "user", "content": dynamic_prompt}
                ],
                temperature=0.3
            )

            # 解析CSV格式响应
            csv_data = response.choices[0].message.content.strip().split(',')
            if len(csv_data) != 8:
                raise ValueError("返回数据列数不正确")

            return {
                "原始产品名": row['product'],
                "原始价格": row['price'],
                "产品全称": csv_data[0],
                "品牌": csv_data[1],
                "产品线": csv_data[2],
                "品类": csv_data[3],
                "昵称": csv_data[4],
                "功效": csv_data[5],
                "参考价格": csv_data[6],
                "品牌产地": csv_data[7]
            }
        except openai.AuthenticationError as e:
            print(f"认证失败，请检查 API Key 是否有效。错误信息：{str(e)}")
            raise
        except Exception as e:
            print(f"处理失败: {row['product']}，错误：{str(e)}")
            return {
                "原始产品名": row['product'],
                "原始价格": row['price'],
                "error": str(e)
            }

    def batch_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        """批量处理增强数据"""
        results = []
        total = len(df)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 提交任务到线程池
            future_to_row = {executor.submit(self.enhance_product_data, row.to_dict()): row for _, row in df.iterrows()}

            for idx, future in enumerate(concurrent.futures.as_completed(future_to_row), 1):
                row = future_to_row[future]
                try:
                    enhanced_row = future.result()
                    results.append(enhanced_row)

                    # 进度显示
                    print(f"进度: {idx}/{total} ({idx / total:.1%}) 当前处理: {row['product'][:20]}...")

                except openai.AuthenticationError:
                    print("由于认证失败，程序终止。")
                    return pd.DataFrame(results)
                except Exception as e:
                    print(f"行{idx}处理异常: {str(e)}")
                    results.append(row.to_dict())

        return pd.DataFrame(results)

    def process_and_save(self, input_file, output_file):
        # 读取原始数据（假设列名为product和price）
        df = pd.read_csv(input_file)

        # 执行处理
        enhanced_df = self.batch_processing(df)

        # 保存结果（保留原始列+新列）
        enhanced_df.to_csv(output_file,
                           index=False,
                           encoding='utf_8_sig')  # 保证中文兼容性

        # 生成处理报告
        success_count = enhanced_df[enhanced_df['产品全称'].notna()].shape[0]
        print(f"\n处理完成！成功率：{success_count}/{len(df)} ({success_count / len(df):.1%})")
        print(f"结果文件已保存至：{output_file}")

