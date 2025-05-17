import pandas as pd


def process_dataframe(df_raw):
    new_page_indices = df_raw.index[df_raw["text"] == "new page"].tolist()
    new_page_indices = [-1] + new_page_indices + [len(df_raw)]  # 添加边界

    # 初始化页码为 1
    page_num = 1
    # 用于存储最终结果的 DataFrame 列表
    all_pages = []

    # 遍历 new_page_indices 列表，根据边界划分页面
    for i in range(len(new_page_indices) - 1):
        # 当前页面的起始索引
        start = new_page_indices[i] + 1
        # 当前页面的结束索引
        end = new_page_indices[i + 1]

        # 获取当前页的数据
        current_page_df = df_raw.iloc[start:end].copy()
        # 为当前页的数据添加页码列
        current_page_df['page'] = page_num
        # 页码加 1，为下一页做准备
        page_num += 1
        # 将当前页的数据添加到 all_pages 列表中
        all_pages.append(current_page_df)

    # 将所有页面的数据合并为一个 DataFrame
    df_marked = pd.concat(all_pages, ignore_index=True)

    # 按照 page 列排序，再按照 location.y 列排序
    df_sorted = df_marked.sort_values(by=['page', 'location.y']).reset_index()

    return df_sorted
