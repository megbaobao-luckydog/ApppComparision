# matplotlib_config.py
import matplotlib.pyplot as plt

# 使用 'bmh' 风格
plt.style.use('bmh')

# 设置 Pastel1 调色板全局颜色
pastel_colors = plt.cm.Pastel1.colors  # 获取 Pastel1 调色板颜色
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=pastel_colors)  # 设置颜色循环

# 你可以在这里添加更多的全局配置
# 比如字体大小、网格线样式等
plt.rcParams['font.size'] = 12
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5

ax.set_aspect('auto')

# Configuration file for plot styles

PLOT_STYLE = {
    'title': {
        'fontsize': 16,
        'fontweight': 'bold',
        'color': 'darkblue'
    },
    'xlabel': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': 'darkred'
    },
    'ylabel': {
        'fontsize': 14,
        'fontweight': 'bold',
        'color': 'darkred'
    },
    'legend': {
        'loc': 'upper left',
        'bbox_to_anchor': (1, 1),
        'title': '',
        'fontsize': 12,
        'title_fontsize': 14
    },
    'grid': {
        'enabled': True,
        'linestyle': '--',
        'color': 'gray',
        'alpha': 0.7
    }
}
