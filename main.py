import time
import os
import gradio as gr
from langchain.document_loaders import DirectoryLoader
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from neo4j import search

# 设置初始化是否使用知识图谱数据库搜索相关知识点
neo4j = False
if neo4j:
    neo4j_use = "知识图谱已启动"
else:
    neo4j_use = "知识图谱已关闭"


def load_documents(directory="documents"):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    text_spliter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)
    split_docs = text_spliter.split_documents(documents)
    return split_docs


def load_embedding_model(local_model_path):
    encode_kwargs = {"normalize_embeddings": False}
    # 使用cpu
    # model_kwargs = {"device": "cpu"}
    # cuda==11.8 pytorch==2.1.0 可用
    model_kwargs = {"device": "cuda:0"}
    return HuggingFaceEmbeddings(
        model_name=local_model_path,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


def store_chroma(docs, embeddings, persist_directory="VectorStore"):
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    db.persist()
    return db


def add_text(history, text):
    history += [(text, None)]
    print(history)
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    global qa
    directory = os.path.dirname(file.name)
    documents = load_documents(directory)
    db = store_chroma(documents, embeddings)
    retriever = db.as_retriever()
    qa.retriever = retriever
    history = history + [((file.name,), None)]
    return history


def bot(history):
    global neo4j, neo4j_use
    if not history:
        # history 列表为空的处理，可以返回一个默认值或者不执行任何操作
        return history
    message = history[-1][0]
    # print(message)
    search_ans = False
    if neo4j:
        search_ans = search.search_relate(message)
    extra = ""
    if search_ans:
        extra = "\n\n-------------------------------------------\n\n以下是根据你的提问推荐的知识点:\n" + search_ans
    if isinstance(message, tuple):
        response = "文件上传成功！！"
    elif (message == "打开知识图谱") or (message == "关闭知识图谱"):
        response = neo4j_use
    else:
        response = qa({"query": message})['result']
        response += extra
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.01)
        yield history


# 定义按钮点击事件处理函数
def btn_neo4j_click(history):
    global neo4j_use, neo4j
    if neo4j_use == "知识图谱已关闭":
        neo4j = True
        neo4j = search.connect_neo4j(neo4j)
    else:
        neo4j = False
        neo4j = search.connect_neo4j(neo4j)
    if neo4j:
        neo4j_use = "知识图谱已启动"
        neo4j__use = "打开知识图谱"
    else:
        neo4j_use = "知识图谱已关闭"  # 切换变量值
        neo4j__use = "关闭知识图谱"
    btn_neo4j.value = neo4j_use
    print("知识图谱状态:", neo4j_use)
    history += [(neo4j__use, None)]
    # print(history)
    return history


if __name__ == "__main__":
    # 加载本地嵌入模型
    embeddings = load_embedding_model(local_model_path='text2vec-base-chinese')
    # 加载向量数据库,若没有则读取documents下文件创建向量数据库
    if not os.path.exists('VectorStore'):
        documents = load_documents()
        db = store_chroma(documents, embeddings)
    else:
        db = Chroma(persist_directory='VectorStore', embedding_function=embeddings)
    # 使用本地api提供的大模型服务
    llm = ChatGLM(
        endpoint_url='http://127.0.0.1:8000',
        max_token=80000,
        top_p=0.9
    )
    # 创建qa问答链
    QA = PromptTemplate.from_template(
        """根据下面的上下文（context）内容回答问题。
    如果你不知道答案，就回答不知道，不要试图编造答案。
    答案最多400个字

    {context}

    问题：{question}

    """)
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        verbose=True,
        chain_type_kwargs={"prompt": QA}
    )
    # 设置前端交互页面
    with gr.Blocks() as demo:
        # 设置页面显示
        chatbot = gr.Chatbot(
            [],
            elem_id="AI助手",
            bubble_full_width=False,
            avatar_images=(None, (os.path.join(os.path.dirname(__file__), "bot.jpg"))),
        )
        # 设置输入
        with gr.Row():
            query = gr.Textbox(
                scale=4,
                show_label=False,
                placeholder="输入问题并按下回车键提交",
                container=False,
            )
            btn = gr.UploadButton("📁上传外挂数据库", file_types=['txt'])
            btn_neo4j = gr.Button(value="开关知识图谱")
        # 处理开关知识图谱逻辑
        neo4j_msg = btn_neo4j.click(btn_neo4j_click, [chatbot], [chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        # 处理输入输出数据
        query_msg = query.submit(add_text, [chatbot, query], [chatbot, query], queue=False).then(
            bot, chatbot, chatbot
        )
        query_msg.then(lambda: gr.update(interactive=True), None, [query], queue=False)
        file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
            bot, chatbot, chatbot
        )

    demo.queue()
    demo.launch()
