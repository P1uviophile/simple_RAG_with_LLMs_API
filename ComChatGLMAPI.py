import datetime
import json
import uvicorn
import zhipuai
from fastapi import FastAPI, Request

app = FastAPI()


# 选择的是https://open.bigmodel.cn/dev/api智谱清言的大模型API 可以换成本地部署的大模型api或其他平台的大模型api
@app.post("/")
async def create_item(request: Request):
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    zhipuai.api_key = "请于此处填入api_key"
    response = zhipuai.model_api.invoke(
        model="chatglm_6b",
        prompt=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )
    RESPONSE = response['data']['choices'][0]['content'].replace("\\n", "\n")
    answer = {
        "response": RESPONSE,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    return answer


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
