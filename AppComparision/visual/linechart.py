import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = 4 + 1 * np.sin(2 * x)
x2 = np.linspace(0, 10, 25)
y2 = 4 + 1 * np.sin(2 * x2)


#%%
fig, ax = plt.subplots()

    # 绘制数据
ax.plot(x2, y2 + 2.5, 'x', markeredgewidth=2)
ax.plot(x, y, linewidth=2.0)
ax.plot(x2, y2 - 2.5, 'o-', linewidth=2)

    # 设置图形范围和刻度
ax.set(xlim=(0, 8), xticks=np.arange(1, 8),ylim=(0, 8), yticks=np.arange(1, 8))

    # 显示图形
plt.show()

#%%
import matplotlib.pyplot as plt
import numpy as np


curves = [
    {'x': x2, 'y': y2 + 2.5, 'style': 'x', 'markeredgewidth': 2},
    {'x': x, 'y': y, 'style': '-', 'linewidth': 2.0},
    {'x': x2, 'y': y2 - 2.5, 'style': 'o-', 'linewidth': 2.0}
]


def plot_multiple_curves(curves, xlim=(0, 8), ylim=(0, 8), xticks=np.arange(1, 8), yticks=np.arange(1, 8)):
    """
    绘制多条曲线。

    参数:
    curves: list of dicts, 每个字典包含 'x', 'y', 'style' 等信息
    xlim: 图形的x轴范围
    ylim: 图形的y轴范围
    xticks: x轴的刻度
    yticks: y轴的刻度
    """
    fig, ax = plt.subplots()

    # 绘制每条曲线
    for curve in curves:
        ax.plot(curve['x'], curve['y'], curve['style'], linewidth=2.0)

    # 设置图形范围和刻度
    ax.set(xlim=xlim, xticks=xticks, ylim=ylim, yticks=yticks)

    # 显示图形
    plt.show()


# 创建数据
x = np.linspace(0, 10, 100)
y = 4 + 1 * np.sin(2 * x)
x2 = np.linspace(0, 10, 25)
y2 = 4 + 1 * np.sin(2 * x2)

# 定义多个曲线
curves = [
    {'x': x2, 'y': y2 + 2.5, 'style': 'x', 'markeredgewidth': 2},
    {'x': x, 'y': y, 'style': '-', 'linewidth': 2.0},
    {'x': x2, 'y': y2 - 2.5, 'style': 'o-', 'linewidth': 2.0}
]

# 调用函数绘制曲线
plot_multiple_curves(curves)

#%%

import matplotlib.pyplot as plt
import numpy as np


def plot_multiple_curves(curves, title="Multiple Curves", xlabel="X Axis", ylabel="Y Axis",
                         xlim=(0, 8), ylim=(0, 8), xticks=np.arange(1, 8), yticks=np.arange(1, 8)):
    """
    绘制多条曲线，并添加标题、坐标轴标签、标签、网格等。

    参数:
    curves: list of dicts, 每个字典包含 'x', 'y', 'style', 'label' 等信息
    title: 图表标题
    xlabel: x轴标签
    ylabel: y轴标签
    xlim: 图形的x轴范围
    ylim: 图形的y轴范围
    xticks: x轴的刻度
    yticks: y轴的刻度
    """
    fig, ax = plt.subplots()

    # 绘制每条曲线
    for curve in curves:
        ax.plot(curve['x'], curve['y'], curve['style'], label=curve.get('label', ''), linewidth=2.0)

    # 设置图形范围和刻度
    ax.set(xlim=xlim, xticks=xticks, ylim=ylim, yticks=yticks)

    # 添加标题和坐标轴标签
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # 添加图例
    ax.legend()

    # 启用网格
    ax.grid(True)

    # 显示图形
    plt.show()


# 创建数据
x = np.linspace(0, 10, 100)
y = 4 + 1 * np.sin(2 * x)
x2 = np.linspace(0, 10, 25)
y2 = 4 + 1 * np.sin(2 * x2)

# 定义多个曲线
curves = [
    {'x': x2, 'y': y2 + 2.5, 'style': 'x', 'label': 'Curve 1', 'markeredgewidth': 2},
    {'x': x, 'y': y, 'style': '-', 'label': 'Curve 2', 'linewidth': 2.0},
    {'x': x2, 'y': y2 - 2.5, 'style': 'o-', 'label': 'Curve 3', 'linewidth': 2.0}
]

# 调用函数绘制曲线
plot_multiple_curves(curves, title="Example of Multiple Curves", xlabel="Time", ylabel="Amplitude")

#%%
import matplotlib.pyplot as plt
import numpy as np


def plot_multiple_curves(curves, title="Multiple Curves", xlabel="X Axis", ylabel="Y Axis",
                         xlim=(0, 8), ylim=(0, 8), xticks=np.arange(1, 8), yticks=np.arange(1, 8)):
    """
    绘制多条曲线，并添加标题、坐标轴标签、标签、网格等，且将图例放置在图形外部。

    参数:
    curves: list of dicts, 每个字典包含 'x', 'y', 'style', 'label' 等信息
    title: 图表标题
    xlabel: x轴标签
    ylabel: y轴标签
    xlim: 图形的x轴范围
    ylim: 图形的y轴范围
    xticks: x轴的刻度
    yticks: y轴的刻度
    """
    fig, ax = plt.subplots(figsize=(8, 6))  # 调整图形大小

    # 绘制每条曲线
    for curve in curves:
        ax.plot(curve['x'], curve['y'], curve['style'], label=curve.get('label', ''), linewidth=2.0)

    # 设置图形范围和刻度
    ax.set(xlim=xlim, xticks=xticks, ylim=ylim, yticks=yticks)

    # 添加标题和坐标轴标签
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # 启用网格
    ax.grid(True)

    # 添加图例并放置在图形外部
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Curves")

    # 显示图形
    plt.tight_layout()  # 自动调整布局，防止图形被遮挡
    plt.show()


# 创建数据
x = np.linspace(0, 10, 100)
y = 4 + 1 * np.sin(2 * x)
x2 = np.linspace(0, 10, 25)
y2 = 4 + 1 * np.sin(2 * x2)

# 定义多个曲线
curves = [
    {'x': x2, 'y': y2 + 2.5, 'style': 'x', 'label': 'Curve 1', 'markeredgewidth': 2},
    {'x': x, 'y': y, 'style': '-', 'label': 'Curve 2', 'linewidth': 2.0},
    {'x': x2, 'y': y2 - 2.5, 'style': 'o-', 'label': 'Curve 3', 'linewidth': 2.0}
]

# 调用函数绘制曲线
plot_multiple_curves(curves, title="Example of Multiple Curves", xlabel="Time", ylabel="Amplitude")


#%%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates


def plot_multiple_curves_with_dates(curves, title="Multiple Curves", xlabel="Date", ylabel="Hour",
                                    xlim=None, ylim=(0, 24), xticks=None, yticks=np.arange(0, 25, 1)):
    """
    绘制多条曲线，x轴为日期，y轴为小时，并添加标题、坐标轴标签、标签、网格等，且将图例放置在图形外部。

    参数:
    curves: list of dicts, 每个字典包含 'x'（日期数据），'y'（小时数据），'style'（曲线样式），'label'（图例标签）等信息
    title: 图表标题
    xlabel: x轴标签
    ylabel: y轴标签
    xlim: 图形的x轴范围
    ylim: 图形的y轴范围
    xticks: x轴的刻度
    yticks: y轴的刻度
    """
    fig, ax = plt.subplots(figsize=(10, 6))  # 调整图形大小

    # 绘制每条曲线
    for curve in curves:
        ax.plot(curve['x'], curve['y'], curve['style'], label=curve.get('label', ''), linewidth=2.0)

    # 设置图形范围和刻度
    if xlim:
        ax.set(xlim=xlim)
    ax.set(ylim=ylim, yticks=yticks)

    # 添加标题和坐标轴标签
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # 添加图例并放置在图形外部
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Curves")

    # 启用网格
    ax.grid(True)

    # 设置日期格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # 格式化日期
    ax.xaxis.set_major_locator(mdates.DayLocator())  # 每天一个主刻度
    plt.xticks(rotation=45, ha='right')  # 旋转日期标签以防重叠

    # 调整布局
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
    {'x': x, 'y': y1, 'style': 'x-', 'label': 'Curve 1'},
    {'x': x, 'y': y2, 'style': 'o-', 'label': 'Curve 2'}
]

# 调用函数绘制曲线
plot_multiple_curves_with_dates(curves, title="Example of Date vs Hour", xlabel="Date", ylabel="Hour")

#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates


def plot_multiple_curves_with_dates(curves, title="Multiple Curves", xlabel="Date", ylabel="Hour",
                                    xlim=None, ylim=(0, 24), xticks=None, yticks=np.arange(0, 25, 1)):
    """
    绘制多条曲线，x轴为日期，y轴为小时，并添加标题、坐标轴标签、标签、网格等，且将图例放置在图形外部。

    参数:
    curves: list of dicts, 每个字典包含 'x'（日期数据），'y'（小时数据），'style'（曲线样式），'label'（图例标签）等信息
    title: 图表标题
    xlabel: x轴标签
    ylabel: y轴标签
    xlim: 图形的x轴范围
    ylim: 图形的y轴范围
    xticks: x轴的刻度
    yticks: y轴的刻度
    """
    # 创建图形和坐标轴
    fig, ax = plt.subplots(figsize=(12, 6))  # 调整图形大小

    # 设置图表风格
    plt.style.use('seaborn-whitegrid')  # 使用 seaborn 风格的白色网格背景

    # 绘制每条曲线
    for curve in curves:
        ax.plot(curve['x'], curve['y'], curve['style'], label=curve.get('label', ''), linewidth=2.5)

    # 设置图形范围和刻度
    if xlim:
        ax.set(xlim=xlim)
    ax.set(ylim=ylim, yticks=yticks)

    # 添加标题和坐标轴标签
    ax.set_title(title, fontsize=16, fontweight='bold', color='darkblue')  # 设置标题样式
    ax.set_xlabel(xlabel, fontsize=14, fontweight='bold', color='darkred')  # 设置 x 轴标签样式
    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', color='darkred')  # 设置 y 轴标签样式

    # 添加图例并放置在图形外部
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Curves", fontsize=12, title_fontsize=14)

    # 启用网格，设置网格线透明度
    ax.grid(True, linestyle='--', color='gray', alpha=0.7)

    # 设置日期格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # 格式化日期
    ax.xaxis.set_major_locator(mdates.DayLocator())  # 每天一个主刻度
    plt.xticks(rotation=45, ha='right', fontsize=12)  # 旋转日期标签并设置字体大小

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
