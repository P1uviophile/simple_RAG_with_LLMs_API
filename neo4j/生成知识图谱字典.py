import pandas as pd
import json

# 读取 CSV 文件
df = pd.read_csv('documents/知识图谱表格.csv')

# 将某列的值转为字典
column_to_dict = dict(zip(df['knowledge'],df['knowledge']))

# 将字典保存到文件中（这里使用 JSON 格式）
with open('知识图谱字典.json', 'w') as json_file:
    json.dump(column_to_dict, json_file)
