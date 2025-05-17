from ..themes.default_theme import Theme
from matplotlib import pyplot as plt

def plot_price_distribution(data, title=None):
    """
    绘制只显示单个比例的柱状图

    参数:
        data: [(区间名称, 价格范围, 数量, 占比), ...]
    """
    # 提取数据
    categories = [d[0] for d in data]
    price_ranges = [d[1] for d in data]
    counts = [d[2] for d in data]
    percentages = [d[3] for d in data]

    fig, ax = plt.subplots()

    # 使用预定义颜色
    colors = [Theme.COLOR_POSITIVE, Theme.COLOR_START_END,
              Theme.COLOR_TOTAL, Theme.COLOR_NEGATIVE][:len(data)]

    # 绘制柱状图
    bars = ax.bar(range(len(data)), counts,
                  color=colors,
                  width=Theme.AXES_BAR_WIDTH,
                  edgecolor='white')

    # 设置y轴范围
    max_count = max(counts)
    ax.set_ylim(0, max_count * 1.3)

    # 添加数据标签
    for i, (count, percent) in enumerate(zip(counts, percentages)):
        ax.text(i, count + max_count * 0.05,
                f"{count}款\n({percent}%)",
                ha='center', va='bottom',
                color=Theme.COLOR_TEXT,
                fontsize=Theme.BASE_FONT_SIZE)

    # 设置x轴标签（样式已全局配置）
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([f"{cat}\n({price})" for cat, price in zip(categories, price_ranges)])

    # 设置标题和坐标轴标签（样式已全局配置）
    ax.set_title(title)
    ax.set_ylabel("产品数量")

    plt.tight_layout()

    if Theme.DEMO_SAVE:
        plt.savefig(Theme.DEMO_SAVE_PATH, bbox_inches='tight')
    if Theme.DEMO_SHOW:
        plt.show()
    plt.close()


