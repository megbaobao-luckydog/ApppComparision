# plot_theme.py
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler


def set_solarize_light2():
    """Solarize_Light2主题的完整配置"""
    # 1. 激活主题
    plt.style.use('Solarize_Light2')

    # 2. 字体配置（保留您指定的字体）
    plt.rc('font', ** {
        'family': 'Hiragino Sans GB',
        'weight': 'bold',
        'size': 12
    })

    # 3. 颜色系统（从主题中提取关键色）
    COLORS = {
        'initial': plt.rcParams['axes.prop_cycle'].by_key()['color'][0],  # 主题色1
        'positive': '#55a868',  # 保持您的绿色
        'negative': '#c44e52',  # 保持您的红色
        'total': '#4c72b0',  # 保持您的蓝色
        'text': '#333333',  # 深灰文字
        'grid': '#d3d3d3'  # 浅灰网格
    }

    # 4. 全局样式覆盖
    plt.rc('axes',  ** {
        'unicode_minus': False,  # 保留您的负数修复
        'prop_cycle': cycler('color', [  # 自定义柱状图色序
            COLORS['initial'],
            COLORS['positive'],
            COLORS['negative'],
            COLORS['total']
        ]),
        'grid': True  # 默认显示网格
    })

    # 5. 网格线样式
    plt.rc('grid',** {
        'linestyle': '--',
        'linewidth': 0.8,
        'alpha': 0.4,
        'color': COLORS['grid']
    })

    # 6. 坐标轴样式
    plt.rc('axes.spines', ** {
        'top': False,
        'right': False
    })

    return COLORS


# 初始化主题
COLORS = set_solarize_light2()

