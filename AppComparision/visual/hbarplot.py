import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def plot_multiple_curves_with_dates(curves, title="Multiple Curves", xlabel="Date", ylabel="Hour",
                                    xlim=None, ylim=(0, 24), xticks=None, yticks=np.arange(0, 25, 1)):

    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, curve in enumerate(curves):
        ax.plot(curve['x'], curve['y'], curve['style'], label=curve.get('label', ''),
                linewidth=2.5)  # 选择 Pastel1 调色板中的颜色

    if xlim:
        ax.set(xlim=xlim)
    ax.set(ylim=ylim, yticks=yticks)

    ax.set_title(title, fontsize=16, fontweight='bold', color='darkblue')


    ax.set_xlabel(xlabel, fontsize=14, fontweight='bold', color='darkred')

    # 设置 x 轴主刻度间隔
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    # 设置 x 轴标签样式
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%A'))  # 格式化为日期和星期几回
    ax.xaxis.set_major_locator(mdates.DayLocator())  # 每天一个主刻度
    ax.tick_params(axis='x', rotation=45, labelsize=12)

    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_markersize(5)

    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', color='darkred')  # 设置 y 轴标签样式

    ax.legend(loc='lower left', bbox_to_anchor=(1, 1), title="Curves", fontsize=12, title_fontsize=14)
    ax.grid(True, linestyle='--', color='gray', alpha=0.7)

    # 关键点标注: 最大值和最小值

    for curve in curves:
        y = curve['y']
        x = curve['x']

        max_y = np.max(y)
        min_y = np.min(y)

        max_x = x[np.argmax(y)]
        min_x = x[np.argmin(y)]

        # 标注最大值
        ax.annotate(f'Max: ({max_x.strftime("%Y-%m-%d %A")}, {max_y})',
                    xy=(max_x, max_y),
                    xytext=(max_x + pd.Timedelta(days=1), max_y + 2),
                    arrowprops=dict(facecolor='red', shrink=0.05),  # 确保这里是字典
                    fontsize=8, color='red')

        # 标注最小值
        ax.annotate(f'Min: ({min_x.strftime("%Y-%m-%d %A")}, {min_y})',
                    xy=(min_x, min_y),
                    xytext=(min_x + pd.Timedelta(days=1), min_y - 2),
                    arrowprops=dict(facecolor='green', shrink=0.05),  # 确保这里是字典
                    fontsize=0, color='green')


    # 调整布局，确保不会遮挡标签
    plt.tight_layout()

    # 显示图形
    plt.show()


# 创建示例数据
date_rng = pd.date_range(start='2024-11-01', periods=10, freq='D')  # 生成10天的日期数据
x = date_rng  # x 轴为日期

# 假设每个日期有小时数据，y 轴是小时
y1 = np.random.randint(0, 24, size=len(x))  # 随机小时数据
y2 = np.random.randint(0, 24, size=len(x))

# 定义多个曲线
curves = [
    {'x': x, 'y': y1, 'style': 'o-', 'label': 'Curve 1'},
    {'x': x, 'y': y2, 'style': 's-', 'label': 'Curve 2'}
]

# 调用函数绘制曲线
plot_multiple_curves_with_dates(curves, title="Example of Date vs Hour", xlabel="Date", ylabel="Hour")

#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def plot_multiple_curves_with_dates(curves, title="Multiple Curves", xlabel="Date", ylabel="Hour",
                                    xlim=None, ylim=(0, 24), xticks=None, yticks=np.arange(0, 25, 1)):

    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, curve in enumerate(curves):
        ax.plot(curve['x'], curve['y'], curve['style'], label=curve.get('label', ''),
                linewidth=2.5)  # Choose color from pastel palette

    if xlim:
        ax.set(xlim=xlim)
    ax.set(ylim=ylim, yticks=yticks)

    ax.set_title(title, fontsize=16, fontweight='bold', color='darkblue')

    ax.set_xlabel(xlabel, fontsize=14, fontweight='bold', color='darkred')

    # Set x axis main tick interval
    ax.xaxis.set_major_locator(mdates.DayLocator())  # One tick per day
    ax.tick_params(axis='x', rotation=45, labelsize=12)

    # Hide x-axis tick labels
    ax.set_xticklabels([])

    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_markersize(5)

    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', color='darkred')

    # Position the legend within the plot area, closer to the top-right
    ax.legend(loc='upper right', fontsize=12, title="Curves", title_fontsize=14)

    ax.grid(True, linestyle='--', color='gray', alpha=0.7)

    # Key points annotation: Max and Min values
    for curve in curves:
        y = curve['y']
        x = curve['x']

        max_y = np.max(y)
        min_y = np.min(y)

        max_x = x[np.argmax(y)]
        min_x = x[np.argmin(y)]

        # Annotate maximum value
        ax.annotate(f'Max: ({max_x.strftime("%Y-%m-%d %A")}, {max_y})',
                    xy=(max_x, max_y),
                    xytext=(max_x + pd.Timedelta(days=1), max_y + 2),
                    arrowprops=dict(facecolor='red', shrink=0.05),
                    fontsize=9, color='red', ha='left')

        # Annotate minimum value (ensure the text stays within the plot area)
        ax.annotate(f'Min: ({min_x.strftime("%Y-%m-%d %A")}, {min_y})',
                    xy=(min_x, min_y),
                    xytext=(min_x + pd.Timedelta(days=1), min_y - 2),

                    )

    # Adjust layout to ensure labels do not overlap
    plt.tight_layout()

    # Display the plot
    plt.show()


# Create example data
date_rng = pd.date_range(start='2024-11-01', periods=10, freq='D')  # 10 days of data
x = date_rng  # x-axis is date

# Random hourly data for each day
y1 = np.random.randint(0, 24, size=len(x))
y2 = np.random.randint(0, 24, size=len(x))

# Define multiple curves
curves = [
    {'x': x, 'y': y1, 'style': 'o-', 'label': 'Curve 1'},
    {'x': x, 'y': y2, 'style': 's-', 'label': 'Curve 2'}
]

# Call function to plot the curves
plot_multiple_curves_with_dates(curves, title="Example of Date vs Hour", xlabel="Date", ylabel="Hour")

