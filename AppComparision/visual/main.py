import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 使用fivethirtyeight样式
plt.style.use('fivethirtyeight')





#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D





# 示例调用：



# plot_top_products(df_top10_views, df_top10_purchases)  # 绘制两个图
# plot_top_products(df_top10_views, df_top10_purchases, num_plots=1)  # 绘制一个图


# 创建格式化字典
numberformat = {
    "millions": lambda x, pos: f'${x * 1e-6:1.1f}M',  # 格式化百万
    "thousands": lambda x, pos: f'${x * 1e-3:1.0f}K',  # 格式化千
    "billion": lambda x, pos: f'${x * 1e-9:1.2f}B'  # 格式化十亿
}

# 示例数据
money = [1.5e5, 2.5e6, 5.5e6, 2.0e7]

# 创建图形和坐标轴
fig, ax = plt.subplots()

# 使用字典中的格式化器


formatter = numberformat["millions"]
ax.yaxis.set_major_formatter(FuncFormatter(formatter))

# 绘制条形图
ax.bar(['Bill', 'Fred', 'Mary', 'Sue'], money)

# 显示图形
plt.show()
