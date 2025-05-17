import os

os.chdir('/Users/mac/python_projects/src/platform_comparision/taobao')

print(os.getcwd())


#%%
sorted_path=None

#%%

""""
梳理图片顺序
"""
from utils import sort_files


# 只传入具体的文件夹名称
folder_name = "serum"
sorted_paths = sort_files.sort_images_by_timestamp(folder_name)



#%%
"""
OCR
"""
from utils import ocr


output_file = "/Users/mac/python_projects/src/platform_comparision/taobao/processed_data/serum.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for snapshot_path in sorted_paths:
        try:
            result = ocr.process_image_and_ocr(snapshot_path)
            filename = os.path.basename(snapshot_path)
            f.write(f"文件名: {filename}\n识别结果:\n{result}\n\n")
        except Exception as e:
            f.write(f"文件名: {os.path.basename(snapshot_path)}\n处理失败: {str(e)}\n\n")

print(f"识别结果已保存到 {output_file}")


#%%
import os
os.chdir('/Users/mac/python_projects/src/platform_comparision/taobao')
print(os.getcwd())

sorted_path = None
"""
梳理图片顺序
"""
from utils import sort_files
# 只传入具体的文件夹名称
folder_name = "serum"
sorted_paths = sort_files.sort_images_by_timestamp(folder_name)

"""
OCR
"""
from utils import ocr
output_file = "/Users/mac/python_projects/src/platform_comparision/taobao/processed_data/serum.txt"

# 创建目录（如果不存在）
directory = os.path.dirname(output_file)
if not os.path.exists(directory):
    os.makedirs(directory)

with open(output_file, "w", encoding="utf-8") as f:
    for snapshot_path in sorted_paths:
        try:
            result = ocr.process_image_and_ocr(snapshot_path)
            filename = os.path.basename(snapshot_path)
            f.write(f"文件名: {filename}\n识别结果:\n{result}\n\n")
        except Exception as e:
            f.write(f"文件名: {os.path.basename(snapshot_path)}\n处理失败: {str(e)}\n\n")
print(f"识别结果已保存到 {output_file}")