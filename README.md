## 简介

项目简介: 该系统是一个智能JAVA面试问答系统，支持用户外挂知识库以提供精确的答案和建议，还引入了neo4j图数据库构建知识图谱，提供知识点关联建议。
工作内容:
● 使用text2vec-base-chinese预训练模型对外挂知识库向量化，并使用向量数据库Chroma存储向量化的外挂知识库; 
● 对输入文本使用检索算法生成Prompt，并结合ChatGLM大语言模型生成回答; 
● 使用gradio库完成前端界面的设计与实现，确保用户交互体验流畅且直观; 
● 使用Neo4j构建知识图谱，提供知识点关联建议。

## 运行效果

neo4j
![image](https://github.com/P1uviophile/simple_RAG_with_LLMs_API/assets/95516646/5b73fef3-9ce9-4693-9c43-a577e59b2eab)

![image](https://github.com/P1uviophile/simple_RAG_with_LLMs_API/assets/95516646/0af5094f-a531-45d3-9aaa-daecb3bd21d6)

网页端

无知识图谱

![image](https://github.com/P1uviophile/simple_RAG_with_LLMs_API/assets/95516646/80fa8e0a-f6ae-4b90-a874-266cb6aa4f94)

![image](https://github.com/P1uviophile/simple_RAG_with_LLMs_API/assets/95516646/c650a6ea-9a63-4ff2-bfdd-8c9490910d55)


有知识图谱

![image](https://github.com/P1uviophile/simple_RAG_with_LLMs_API/assets/95516646/82082fe2-b638-4604-bada-fd0f582b0f67)

![image](https://github.com/P1uviophile/simple_RAG_with_LLMs_API/assets/95516646/721a5c6d-7e33-4d0c-a16b-60d94521faf7)


## 项目部署

neo4j版本:4.2.4

#### 0.注:关于以下1-2点: 用于其他外挂知识库的话neo4j的知识图谱相关代码可以不管或者自己重写相关API和代码,只是少了根据问题推荐相关知识点的功能,用LLM一样能实现且实现得更好...

1.安装并启动neo4j数据库并添加管理员角色:账号root 密码jk18889903808

​	(或将neo4j下的py文件中的 graph = Graph("http://localhost:7474/browser/", auth=('root', 'jk18889903808') 替换成你的neo4j数据库中的账号密码)

2.运行neo4j目录下 生成知识图谱.py 

3.下载所需库

4.更换ComChatGLMAPI.py内的ApiKEY(智谱AI开放平台),或重写自选的企业大模型API

5.运行 ComChatGLMAPI.py 和 main.py

6.浏览器打开 http://127.0.0.1:7860 即可使用

7.若想更换API为本地部署大模型请参照ComChatGLMAPI.py中API格式提供本地部署大模型的API
