import os


def sort_images_by_timestamp(folder_name):
    # 拼接完整的文件夹路径
    BASE_PATH = '/Users/mac/python_projects/src/platform_comparision/taobao/screenshot/'
    folder_path = os.path.join(BASE_PATH, folder_name)
    image_paths = []
    # 遍历文件夹
    for filename in os.listdir(folder_path):
        # 检查是否为图片文件，可根据实际情况添加更多图片扩展名
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            try:
                # 提取文件名中的时间戳部分
                timestamp_str = filename.split("_")[1] + filename.split("_")[2]
                timestamp = int(timestamp_str)
                image_paths.append((timestamp, image_path))
            except (ValueError, IndexError):
                print(f"文件名 {filename} 不是有效的时间戳格式，将被忽略。")

    # 按照时间戳对图片路径进行排序
    image_paths.sort(key=lambda x: x[0])
    # 只保留图片路径
    sorted_paths = [path for _, path in image_paths]
    return sorted_paths

#%%
