import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from typing import ClassVar

from wordcloud import WordCloud


class Theme:
    """Matplotlib 全局主题配置类"""

    # 1. 字体配置
    FONT_FAMILY = 'Hiragino Sans GB'
    FONT_WEIGHT = 'bold'
    BASE_FONT_SIZE = 12

    # 2. 颜色配置
    COLOR_TITLE = '#073642'
    COLOR_AXIS = '#dc322f'
    COLOR_GRID = '#839496'
    COLOR_TEXT = '#002b36'
    COLOR_POSITIVE = '#859900'  # 经济型-绿色
    COLOR_START_END = '#268bd2'  # 中端-蓝色
    COLOR_TOTAL = '#6c71c4'  # 高端-紫色
    COLOR_NEGATIVE = '#d33682'  # 豪华-粉色
    COLOR_TICK = '#586e75'
    COLOR_CONNECTOR = '#93a1a1'

    # 3. 图表尺寸
    FIGURE_SIZE = (12, 6)
    FIGURE_DPI = 100

    # 4. 坐标轴样式
    AXES_TITLE_PAD = 20
    AXES_LABEL_PAD = 10
    AXES_TICK_ROTATION = 45
    AXES_TICK_HA = 'right'
    AXES_BAR_WIDTH = 0.6
    AXES_CONNECTOR_STYLE = '--'
    AXES_CONNECTOR_WIDTH = 1.5
    AXES_SPINE_VISIBLE = {'top': False, 'right': False}  # 新增边框可见性设置

    # 5. 演示配置
    DEMO_SHOW = True
    DEMO_SAVE = False
    DEMO_SAVE_PATH = './output.png'

    # 6. 词云配置 (新增)
    WORDCLOUD_WIDTH = 800
    WORDCLOUD_HEIGHT = 400
    WORDCLOUD_BG_COLOR = '#fdf6e3'  # 浅米色背景
    WORDCLOUD_COLORS = ['#859900', '#268bd2', '#6c71c4', '#d33682']  # 主题色系
    # 新增中文词云专用配置
    WORDCLOUD_CHINESE_FONT = 'SimHei'  # 推荐使用系统自带的中文字体
    WORDCLOUD_MAX_WORDS = 200


    @classmethod
    def configure(cls):
        """应用全局绘图配置"""
        plt.style.use('Solarize_Light2')

        config = {
            # 字体系统
            'font.sans-serif': [cls.FONT_FAMILY, 'Microsoft YaHei', 'Arial'],
            'font.weight': cls.FONT_WEIGHT,
            'axes.unicode_minus': False,
            'mathtext.fontset': 'stix',

            # 文本大小
            'axes.titlesize': cls.BASE_FONT_SIZE + 4,
            'axes.labelsize': cls.BASE_FONT_SIZE + 2,
            'xtick.labelsize': cls.BASE_FONT_SIZE,
            'ytick.labelsize': cls.BASE_FONT_SIZE,
            'legend.fontsize': cls.BASE_FONT_SIZE,

            # 颜色
            'axes.titlecolor': cls.COLOR_TITLE,
            'axes.labelcolor': cls.COLOR_AXIS,
            'xtick.color': cls.COLOR_TICK,
            'ytick.color': cls.COLOR_TICK,
            'text.color': cls.COLOR_TEXT,

            # 坐标轴
            'axes.titleweight': cls.FONT_WEIGHT,
            'axes.labelweight': cls.FONT_WEIGHT,
            'axes.titlepad': cls.AXES_TITLE_PAD,
            'axes.labelpad': cls.AXES_LABEL_PAD,

            # 网格
            'axes.grid': True,
            'grid.linestyle': cls.AXES_CONNECTOR_STYLE,
            'grid.color': cls.COLOR_GRID,
            'grid.alpha': 0.7,
            'grid.linewidth': cls.AXES_CONNECTOR_WIDTH,

            # 图表尺寸
            'figure.figsize': cls.FIGURE_SIZE,
            'figure.dpi': cls.FIGURE_DPI,
            'savefig.dpi': cls.FIGURE_DPI,

            # 条形图
            'hist.bins': 'auto',
            'patch.force_edgecolor': True,

            # 边框设置 (使用正确的参数名)
            'axes.spines.top': cls.AXES_SPINE_VISIBLE['top'],
            'axes.spines.right': cls.AXES_SPINE_VISIBLE['right'],

            # 刻度标签设置 (使用正确的参数名)
            'xtick.major.pad': 10,

        }

        rcParams.update(config)

# 自动应用全局配置
Theme.configure()



