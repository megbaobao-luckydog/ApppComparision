import matplotlib.font_manager as fm
import os

# 获取所有已安装的中文字体
font_paths = []
for root, _, files in os.walk('/System/Library/Fonts'):
    for file in files:
        if file.lower().endswith(('.ttf', '.ttc', '.otf')):
            path = os.path.join(root, file)
            try:
                font = fm.FontProperties(fname=path)
                if any(char in font.get_name() for char in ['PingFang', 'Hei', 'Song', 'Kai', 'ST']):
                    font_paths.append((font.get_name(), path))
            except:
                continue

# 打印找到的中文字体
print("Mac系统可用的中文字体：")
for name, path in sorted(font_paths, key=lambda x: x[0]):
    print(f"{name: <25} {path}")

