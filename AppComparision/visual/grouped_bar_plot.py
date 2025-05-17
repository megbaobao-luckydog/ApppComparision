import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# 1. 配置中文字体（自动查找系统字体）
def get_chinese_font():
    try:
        # 尝试获取苹方或黑体（Mac）
        font_path = '/System/Library/Fonts/STHeiti Light.ttc'
    except:
        #  fallback到默认字体
        font_path = None
    return font_path


# 2. 准备数据
categories = ['第一季度', '第二季度', '第三季度', '第四季度']
groups = ['产品A', '产品B', '产品C']

# 示例数据（3个产品在4个季度的销售额）
data = np.array([
    [120, 150, 180, 90],  # 产品A
    [80, 110, 95, 120],  # 产品B
    [60, 70, 130, 150]  # 产品C
])

# 3. 绘图配置
plt.style.use('Solarize_Light2')  # 保持与之前一致的风格
fig, ax = plt.subplots(figsize=(12, 7))

# 设置颜色（使用Solarize_Light2的配色）
colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(groups)))

# 4. 绘制分组柱状图
bar_width = 0.25  # 每个柱子的宽度
x = np.arange(len(categories))  # X轴位置

for i, (group, sales) in enumerate(zip(groups, data)):
    offset = bar_width * i  # 每组的位置偏移
    bars = ax.bar(
        x + offset,
        sales,
        width=bar_width,
        label=group,
        color=colors[i],
        edgecolor='gray',
        linewidth=0.8,
        alpha=0.9
    )

    # 在柱子上方添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height + 5,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10
        )

# 5. 图表美化
# 设置中文字体
chinese_font = get_chinese_font()
if chinese_font:
    plt.rcParams['font.family'] = fm.FontProperties(fname=chinese_font).get_name()

# 标题和坐标轴
ax.set_title('2023年产品季度销售额对比',
             fontsize=16,
             fontweight='bold',
             pad=20)
ax.set_xlabel('季度', fontsize=12, labelpad=10)
ax.set_ylabel('销售额（万元）', fontsize=12, labelpad=10)

# X轴刻度
ax.set_xticks(x + bar_width * (len(groups) - 1) / 2)
ax.set_xticklabels(categories)

# 网格线和边框
ax.yaxis.grid(True, linestyle='--', alpha=0.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 图例
ax.legend(
    title='产品分类',
    frameon=False,
    bbox_to_anchor=(1, 1),
    borderaxespad=0
)

# 调整布局
plt.tight_layout()

# 6. 保存和显示
plt.savefig('grouped_bar_chart.png', dpi=300, bbox_inches='tight')
plt.show()

