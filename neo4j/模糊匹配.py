import json
from fuzzywuzzy import process

with open('知识图谱字典.json', 'r') as json_file:
    dict = json.load(json_file)

# 用户输入
user_input = input("请输入句子：")

# 分词
user_words = user_input.split()

# 选择最佳匹配
best_match, score = process.extractOne(user_input, dict.keys())

# 打印匹配结果
print(f"最佳匹配词语: {best_match}")
print(f"匹配度: {score}")
