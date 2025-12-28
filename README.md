# Doubao Chatbot on AWS

一个基于 **AWS Serverless + 火山方舟豆包大模型** 的公网可访问聊天机器人 Demo。

## 架构说明

整体架构：

- 前端：静态网页托管在 **Amazon S3 Static Website Hosting**
- 网关：**API Gateway HTTP API** 暴露 `POST /chat` 接口
- 后端：**AWS Lambda (Python)** 接收请求，调用火山方舟豆包模型
- 大模型：火山方舟（Volcengine Ark）`doubao-1.5-lite-32k` 模型

调用链路：

1. 用户通过浏览器访问 S3 中的静态网页
2. 前端使用 `fetch` 调用 API Gateway 的 `/chat` 接口
3. API Gateway 将请求转发给 Lambda 函数
4. Lambda 使用火山方舟 API Key 调用 `https://ark.cn-beijing.volces.com/api/v3/chat/completions`
5. 将豆包模型返回的内容包装成 JSON，返回给前端展示

## 目录结构

```text
aws-doubao-chatbot/
├─ lambda/               # Lambda 后端代码
│   ├─ lambda_function.py
│   ├─ requirements.txt
├─ frontend/             # S3 静态网站前端
│   └─ index.html
├─ infra/                # 预留：后续可加入 Terraform/CDK
├─ .gitignore
└─ README.md
