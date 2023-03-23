import openai
import os


# 将您的 OpenAI API 密钥设置为环境变量，或者在这里直接输入
openai.api_key = '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'

# 调用 OpenAI GPT-3 API 发送请求
response = openai.Completion.create(
    engine="davinci",
    prompt="Hello, I'm ChatGPT. How can I help you today?",
    max_tokens=60
)

print(response["choices"][0]["text"])
