import re


def clean_text(extracted_data, cleaned_data1):
    try:
        with open(extracted_data, 'r', encoding='utf-8') as f:
            text = f.read()

        # 去掉重复内容
        pattern = r'文件名.*?百亿加补.*?\n'
        new_text = re.sub(pattern, '', text, flags=re.DOTALL)

        # 去除多余的空行
        new_text = re.sub(r'\n+', '\n', new_text).strip()

        new_text = "店>\n" + new_text

        # 使用 with 语句将处理后的内容写入新文件
        with open(cleaned_data1, 'w', encoding='utf-8') as output_file:
            output_file.write(new_text)

        print(f"文本处理完成，结果已保存到 {cleaned_data1}")

    except FileNotFoundError:
        print(f"文件 {extracted_data} 不存在，请检查路径是否正确。")
    except Exception as e:
        print(f"发生了一个错误: {str(e)}")
