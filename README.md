## 简介

该系统允许求职者直接提问关于Java面试的问题，通过自然语言处理和机器学习技术，结合大量的Java面试资料和经验数据，为其提供精确且全面的答案和建议。系统还提供友好直观的用户界面，方便求职者获取所需信息，进一步提高效率。

实现功能包括用户输入处理、数据库检索及Prompt生成、回答生成、知识关联、前端实现和前后端通道。使用text2vec-base-chinese预训练模型进行文本嵌入，Chroma数据库存储向量，使用检索算法生成Prompt，结合ChatGLM大语言模型生成回答。引入neo4j图数据库构建知识图谱，提供知识点关联建议。前端实现简单的问答网页，通过前后端通道进行数据通信。

主要技术包括文本嵌入模型、数据库检索及Prompt生成、回答生成、前端实现、前后端通道、知识库管理和知识图谱创建。系统将text2vec-base-chinese模型、Chroma数据库、ChatGLM模型、前端框架、知识库和知识图谱进行整合，为用户提供全面而个性化的面试准备支持。



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
