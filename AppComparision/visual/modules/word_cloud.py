import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from ..themes.default_theme import Theme

def plot_word_cloud(word_series, title=None):
    """
    从Pandas Series生成词云（适用于已分词的词频数据）

    参数:
        word_series: Pandas Series，索引是词语，值是词频
        title: 图表标题
    """
    # 确保输入是Series格式
    if not isinstance(word_series, pd.Series):
        raise TypeError("输入必须是Pandas Series格式")

    # 转换为词频字典
    word_freq = word_series.to_dict()

    # 创建词云对象
    wc = WordCloud(
        font_path=Theme.FONT_FAMILY,  # 确保这是有效字体路径
        width=800,
        height=600,
        background_color=Theme.WORDCLOUD_BG_COLOR,
        max_words=Theme.WORDCLOUD_MAX_WORDS,
        colormap='viridis',
        contour_width=1,
        contour_color='steelblue'
    )

    # 直接从词频生成
    wc.generate_from_frequencies(word_freq)

    # 显示设置
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(
        title,
        fontsize=16,
        color=Theme.COLOR_TITLE,
        pad=20
    )
    plt.tight_layout()
    plt.show()


