import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import os


def generate_wordcloud(text, mask_path=None):
    """生成Solarize_Light2风格词云"""
    # 1. 设置Solarize_Light2样式
    plt.style.use('Solarize_Light2')

    # 2. 获取当前样式的背景色
    bg_color = plt.rcParams['axes.facecolor']  # 获取背景色

    # 3. 字体配置（macOS路径）
    font_path = '/System/Library/Fonts/STHeiti Light.ttc'
    if not os.path.exists(font_path):
        font_path = None

    # 4. 颜色配置（使用Solarize调色板）
    colormap = plt.cm.viridis  # 改用Solarize_Light2兼容配色

    # 5. 词云生成
    wc = WordCloud(
        width=1200,
        height=800,
        background_color=bg_color,  # 使用样式背景色
        mask=np.array(Image.open(mask_path)) if mask_path else None,
        colormap=colormap,
        contour_width=0.5,
        contour_color='gray',
        prefer_horizontal=0.8,
        font_path=font_path
    ).generate(text)

    # 6. 绘图设置
    plt.figure(figsize=(14, 8), facecolor=bg_color)  # 设置画布背景
    plt.imshow(wc, interpolation='bilinear')
    plt.title(
        "Solarize风格词云",
        fontsize=24,
        fontweight='bold',
        color=plt.rcParams['text.color']  # 使用样式文字色
    )
    plt.axis('off')

    # 7. 保存输出
    plt.savefig(
        'solar_wordcloud.png',
        dpi=300,
        bbox_inches='tight',
        facecolor=bg_color  # 保存时保持背景
    )
    plt.show()


# 测试数据
sample_text = """
Python 数据分析 机器学习 深度学习 可视化 
大数据 人工智能 神经网络 特征工程 模型训练 
预测分析 商业智能 数据挖掘 统计建模 
自然语言处理 计算机视觉 时间序列
"""

# 生成词云（可添加蒙版路径）
generate_wordcloud(sample_text)
#%%

def find_chinese_font():
    """自动查找系统中文字体路径"""
    # macOS 字体路径
    mac_fonts = [
        '/System/Library/Fonts/PingFang.ttc',  # 苹方
        '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体
        '/System/Library/Fonts/Supplemental/Songti.ttc'  # 宋体
    ]

    # Windows 字体路径
    win_fonts = [
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑
    ]

    # Linux 字体路径
    linux_fonts = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    ]

    # 遍历所有可能的字体路径
    for font in mac_fonts + win_fonts + linux_fonts:
        if os.path.exists(font):
            return font
    return None


# 测试中文文本
chinese_text = """
数据分析 机器学习 深度学习 人工智能 
自然语言处理 计算机视觉 大数据 云计算 
神经网络 推荐系统 知识图谱 物联网 
区块链 数字化转型 商业智能 用户画像
"""

# 生成词云
generate_chinese_wordcloud(chinese_text)


#%%
def find_chinese_font():
    """自动查找系统中文字体路径"""
    # macOS 字体路径
    mac_fonts = [
        '/System/Library/Fonts/PingFang.ttc',  # 苹方
        '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体
        '/System/Library/Fonts/Supplemental/Songti.ttc'  # 宋体
    ]

    # Windows 字体路径
    win_fonts = [
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑
    ]

    # Linux 字体路径
    linux_fonts = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    ]

    # 遍历所有可能的字体路径
    for font in mac_fonts + win_fonts + linux_fonts:
        if os.path.exists(font):
            return font
    return None