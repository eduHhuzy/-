# 分词

import textract
import jieba
import os
import glob

input_dir = '/Users/April_zy/PycharmProjects/Big model/应急知识整理01' # 原始文件所在的目录

output_dir = '/Users/April_zy/PycharmProjects/Big model/本地知识库（分词后）'# 新文件的保存路径


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file_path in glob.glob(os.path.join(input_dir, '*')):# 使用glob模块来遍历所有文件
    # 检查文件是否是文档、PPT或PDF文件（或其他你希望处理的文件类型）
    if os.path.isfile(file_path) and file_path.lower().endswith(('.docx', '.doc', '.pptx', '.ppt', '.pdf')):
        try:
            raw_text = textract.process(file_path)  # 注意：不是所有情况下raw_text都是bytes类型，所以可能需要额外的处理
            if isinstance(raw_text, bytes):
                text = raw_text.decode('utf-8')  # 确保文本是utf-8编码
            else:
                text = raw_text  # 如果不是bytes类型，直接使用

            print(f"Extracting text from: {file_path}")
            seg_list = jieba.cut(text, cut_all=False)  # 使用jieba进行分词
            words = " ".join(seg_list)

            base_name = os.path.splitext(os.path.basename(file_path))[0] # 构造新文件的名称（保持与原始文件相同的文件名但扩展名为.seg.txt）
            new_file_path = os.path.join(output_dir, f"{base_name}.seg.txt")

            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(words)# 将分词结果保存到新文件中

            print(f"Saved segmented text to: {new_file_path}")
            print("\n")  # 添加空行分隔不同文件的内容

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")