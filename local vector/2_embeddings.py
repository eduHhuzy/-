# 词嵌入

import requests
import json
import os
import glob

api_key = 'sk-9dBouZqE3XFJTSkVC5Bf6bE4BdFb417fAe7dB226Aa297e92'
url = 'https://api.bianxieai.com/v1/embeddings'
input_folder = '/Users/April_zy/PycharmProjects/Big model/本地知识库（分词后）/'
output_folder = '/Users/April_zy/PycharmProjects/Big model/词嵌入embeddings/'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 使用glob模块来遍历所有.seg.txt文件
input_files = glob.glob(os.path.join(input_folder, '*.seg.txt'))

for input_file_path in input_files:
    # 移除文件扩展名来生成输出文件名（可选）
    base_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = os.path.join(output_folder, f"{base_filename}.embeddings.txt")

    with open(input_file_path, 'r', encoding='utf-8') as file:
        text_content = file.read().strip()

    data = {
        "input": text_content,
        "model": "text-embedding-3-large",
        "encoding_format": "float"
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        embeddings_json = response.json()

        # 使用json.dump()将JSON对象保存到文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(embeddings_json, output_file, ensure_ascii=False, indent=4)  # indent=4使输出更易读
        print(f"Embeddings for {base_filename} have been saved to: {output_file_path}")
    else:
        print(f"Request for {base_filename} failed: {response.status_code} - {response.text}")