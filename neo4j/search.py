import json
import random
import re
from jieba import analyse
import jieba
from fuzzywuzzy import process
from py2neo import Graph, DatabaseError, ConnectionUnavailable
from py2neo import NodeMatcher, RelationshipMatcher


# 建立neo4j对象，便于后续执行cyphere语句
graph = None
node_matcher = None
relationship_matcher = None

try:
    # 尝试连接Neo4j数据库
    graph = Graph("http://localhost:7474/browser/", auth=('root', '123456'))
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)

except ConnectionUnavailable  as e:
    print("未连接neo4j")
    pass


# 执行Cypher查询
def find_related_nodes(word):
    word = find_node_attach(word)
    node1 = node_matcher.match("attach").where(name=word).first()
    # print(word)
    relationship = list(relationship_matcher.match([node1], r_type='knowledgePoint'))
    # print(len(relationship))
    length = min(len(relationship), 5)
    result = ""
    for i in range(len(relationship)):
        rel = relationship.pop()
        relationship_string = str(rel)
        # 使用正则表达式提取括号中的文本
        match = re.search(r'->\(([^)]+)\)', relationship_string)
        if match:
            related_word = match.group(1)
            if related_word != word:
                result += (str(related_word + "\n"))
        else:
            print("未找到匹配的文本")
    # 将result中的值随机排列
    result_list = result.strip().split("\n")
    random.shuffle(result_list)
    result_shuffled = "\n".join(result_list[:length])
    # print(result_shuffled)
    return result_shuffled


def find_fuzzy_matching_node(sentence):
    # 模糊匹配字典中词语
    with open('知识图谱字典.json', 'r') as json_file:
        dict = json.load(json_file)
    # 分词
    jieba.load_userdict('知识图谱字典.json')
    words = jieba.lcut(sentence)
    # tfidf = analyse.extract_tags
    # keywords = tfidf(sentence)
    # 用户输入
    user_input = sentence
    print(user_input)
    # 选择最佳匹配
    best_match, score = process.extractOne(user_input, dict.keys())
    # 打印匹配结果
    print(f"最佳匹配词语: {best_match}")
    print(f"匹配度: {score}")
    if score <= 60:
        return False
    else:
        # 匹配度大于等于60则输出知识图谱匹配知识点
        return best_match


def search_relate(user_input):
    # 调用函数并获取结果
    word = find_fuzzy_matching_node(user_input)
    # print(word)
    results = False
    if word:
        results = find_related_nodes(word)
    return results


def find_node_value(word):
    # 返回结点values值
    node = list(node_matcher.match("knowledgePoint").where(name=word))
    # print(node[0]['values'])
    return node[0]['values']


def find_node_attach(word):
    # 返回结点values值
    node = list(node_matcher.match("knowledgePoint").where(name=word))
    # print(node[0]['values'])
    return node[0]['attach']


def connect_neo4j(neo4j):
    global graph,node_matcher,relationship_matcher
    if neo4j:
        try:
            # 尝试连接Neo4j数据库
            graph = Graph("http://localhost:7474/browser/", auth=('root', '123456'))
            node_matcher = NodeMatcher(graph)
            relationship_matcher = RelationshipMatcher(graph)
            print("已连接neo4j")
            return True

        except ConnectionUnavailable:
            print("连接neo4j失败")
            return False
    else:
        graph = None
        node_matcher = None
        relationship_matcher = None
        print("断开neo4j连接")
        return False
