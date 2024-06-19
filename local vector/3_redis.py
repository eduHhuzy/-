import os
import redis
import re

# Redis连接配置
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

# 连接到Redis
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# 文件目录
directory = '/Users/April_zy/PycharmProjects/Big model/词嵌入embeddings/'

# 使用glob模块匹配指定模式的文件,所有符合后缀名称的全部进行遍历
for filename in os.listdir(directory):
    if filename.endswith('.seg.embeddings.txt'):
        # 构建完整的文件路径
        file_path = os.path.join(directory, filename)

        # 用于存储embedding的变量
        embedding = []

        # 标记是否正在解析embedding列表
        parsing_embedding = False

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 去除行尾的空白和换行符
                line = line.strip()

                # 检查是否开始解析embedding列表
                if '"embedding": [' in line:
                    parsing_embedding = True
                    # 提取并去除开头的字符串，并尝试提取浮点数
                    numbers = re.findall(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?', line[len('"embedding": ['):])
                    embedding.extend(float(num) for num in numbers if num.strip())
                    continue
                if parsing_embedding:
                    # 检查行是否以逗号或方括号结尾，这表示可能是embedding列表的一部分
                    if line.endswith(',') or line.endswith(']'):
                        numbers = re.findall(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?', line.strip(','))
                        embedding.extend(float(num) for num in numbers if num.strip())
                        # 如果行以方括号结尾，则表示embedding列表结束
                        if line.endswith(']'):
                            parsing_embedding = False
                            # 将embedding转换为字符串并存储到Redis中
        #我们使用文件名作为key
        file_name_without_ext = os.path.splitext(filename)[0]
        redis_key = f'embedding:{file_name_without_ext}'
        r.set(redis_key, ' '.join(map(str, embedding)))

        print(f"Embedding from {filename} has been stored in Redis with key: {redis_key}")