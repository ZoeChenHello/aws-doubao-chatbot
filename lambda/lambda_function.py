import json
import os
import requests

API_KEY = os.environ.get("VOLCENGINE_API_KEY")
MODEL_ID = os.environ.get("VOLCENGINE_MODEL", "doubao-1.5-lite-32k")


def call_doubao(user_message: str) -> str:
    """
    调用火山方舟 doubao-1.5-lite-32k 模型的 Chat Completions 接口
    文档：POST https://ark.cn-beijing.volces.com/api/v3/chat/completions
    鉴权：Authorization: Bearer {API_KEY}
    """
    if not API_KEY:
        return "后端没有配置 VOLCENGINE_API_KEY，请先在 Lambda 环境变量里设置。"

    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "你是一个友好的中文云计算助手。"},
            {"role": "user", "content": user_message}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        # Ark Chat Completions 返回格式：choices[0].message.content
        return data.get("choices", [{}])[0].get("message", {}).get("content", "（模型没有返回内容）")
    except Exception as e:
        return f"调用火山方舟接口失败: {e}"


def lambda_handler(event, context):
    """
    适配 API Gateway HTTP API：
    - event["body"] 是 JSON 字符串：{"message": "..."}
    """
    body_str = event.get("body") or "{}"
    try:
        body = json.loads(body_str)
    except Exception:
        body = {}

    user_message = (body.get("message") or "").strip()

    if not user_message:
        reply = "请先输入要提问的内容。"
    else:
        reply = call_doubao(user_message)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"reply": reply}, ensure_ascii=False),
    }
