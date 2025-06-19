import os
from env import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("You are an expert in astronomy. Answer the question. <Question>: {input}")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

print(chain.invoke({"input": "지구의 자전 주기는?"}))