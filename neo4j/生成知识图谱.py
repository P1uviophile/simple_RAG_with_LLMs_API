## 相关模块导入
import pandas as pd
from py2neo import Graph, Node, Relationship

## 连接图形库，配置neo4j
graph = Graph("http://localhost:7474/browser/", auth=('root', 'jk18889903808'))
# 清空全部数据
graph.delete_all()
# 开启一个新的事务
graph.begin()

## csv源数据读取
storageData = pd.read_csv('documents/知识图谱表格.csv', encoding='utf-8')
# 获取所有列标签
columnLst = storageData.columns.tolist()
# 获取数据数量
num = len(storageData['knowledge'])

# KnowledgeGraph知识图谱构建
for i in range(num):

    dict = {}
    for column in columnLst:
        dict[column] = storageData[column][i]
    # print(dict)
    node1 = Node('knowledgePoint', name=storageData['knowledge'][i], **dict)
    graph.merge(node1, 'knowledgePoint', 'name')

    # 去除所有的title结点
    dict.pop('knowledge')
    ## 分界点以及关系
    for key, value in dict.items():
        ## 建立分结点
        node2 = Node(key, name=value)
        graph.merge(node2, key, 'name')
        ## 创建关系
        rel = Relationship(node1, key, node2)
        graph.merge(rel)
        if key == "attach":
            rel = Relationship(node2, "knowledgePoint", node1)
            graph.merge(rel)
