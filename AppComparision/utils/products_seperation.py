
#%%
'''这段代码应该在处理完banner之后， 得到**rbanner之后运行'''
import re


def extract_text(text):
    '''
    读取整个文本
    找到两个店铺之间的商品信息
    返回segment（list)
    list 中的每一个元素是一个商品块'''
    lines = text.split('\n')
    shop_indices = []

    # 查找所有包含“店”相关关键词的行的索引
    for i, line in enumerate(lines):
        if '旗舰店 >' in line.strip() or '回头客' in line.strip() or '进店' in line.strip() or '店 >' in line.strip():
            shop_indices.append(i)

    segments = []
    for i in range(len(shop_indices) - 1):
        start_index = shop_indices[i]
        end_index = shop_indices[i + 1]
        shop_name = lines[start_index].strip()
        # 截取两个店之间的文本片段
        segment = lines[start_index + 1:end_index]
        combined_text = ' '.join(segment)
        segments.append(combined_text)

    return segments


def products_seperation(remove_banner):
    try:
        with open(remove_banner, 'r', encoding='utf-8') as f:
            content = f.read()

        # 初始化全局变量result
        global result
        result = []

        # 获取提取的段落
        extracted_segments = extract_text(content)# 调用分隔商品块的函数

        # 定义价格匹配的正则表达式
        price_pattern = re.compile(r'((¥|Y)\d+(\.\d+)?|\d+(\.\d+)?元)')

        for segment in extracted_segments:
            all_prices = price_pattern.findall(segment)
            if all_prices:
                max_price = None
                max_price_str = ""
                for price_match in all_prices:
                    price_str = price_match[0]
                    # 去除货币符号和单位，转换为数值
                    if price_str.startswith('¥') or price_str.startswith('Y'):
                        price_num = float(price_str[1:])
                    elif price_str.endswith('元'):
                        price_num = float(price_str[:-1])
                    if max_price is None or price_num > max_price:
                        max_price = price_num
                        max_price_str = price_str
                index = segment.find(max_price_str)
                price_before = segment[:index].strip()
                result.append((price_before, max_price_str))
            else:
                result.append((segment, ""))

        # 打印存储的结果
        for item in result:
            print(f"价格前文本: {item[0]}")
            print(f"价格: {item[1]}")
            print("-" * 50)
        return result
    except FileNotFoundError:
        print(f"错误：未找到文件 {remove_banner}。")
    except Exception as e:
        print(f"发生未知错误：{e}")

