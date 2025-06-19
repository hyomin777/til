import os
from env import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

prompt = ChatPromptTemplate.from_template("지구과학에서 {topic}에 대해 간단히 설명해주세요.")
model = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

# invoke method
result = chain.invoke({"topic": "지구 자전"})
print("invoke result:", result)

# batch method
topics = ["지구 공전", "화산 활동", "대륙 이동"]
results = chain.batch([{"topic": t} for t in topics])
for topic, result in zip(topics, results):
    print(f"{topic} 설명: {result[:50]}...")

# stream method
stream = chain.stream({"topic": "지진"})
print("stream 결과:")
for chunk in stream:
    print(chunk, end="", flush=True)
print()

import asyncio
async def run_async():
    result = await chain.ainvoke({"topic": "해류"})
    print("ainvoke 결과:", result[:50], "...")

asyncio.run(run_async())