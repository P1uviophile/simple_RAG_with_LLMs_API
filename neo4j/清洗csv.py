import csv

import numpy as np
import pandas as pd

df = pd.read_csv('documents/知识图谱表格root.csv', encoding='utf-8')

# 显示每一列中的缺失值数量
print(df.isnull().sum())

df.dropna(subset=['values'], inplace = True)

print(df.isnull().sum())
df.to_csv('documents/知识图谱表格.csv',index=False)