from langchain_community.document_loaders import WebBaseLoader

url = 'https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EC%A0%95%EC%B1%85%EA%B3%BC_%EC%A7%80%EC%B9%A8'
loader = WebBaseLoader(url)

docs = loader.load()

if __name__ == '__main__':
    print(len(docs))
    print(len(docs[0].page_content))
    print(docs[0].page_content[5000:6000])

# Text Split (Documents -> small chunks: Documents)
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

if __name__ == '__main__':
    print(len(splits))
    print(splits[10])
    print(splits[10].page_content)

# Indexing (Texts -> Embedding -> Store)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import OPENAI_API_KEY
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

vectorstore = Chroma.from_documents(documents=splits,
                                    embedding=OpenAIEmbeddings())

if __name__ == '__main__':
    docs = vectorstore.similarity_search("격하 과정에 대해서 설명해주세요.")
    print(len(docs))
    print(docs[0].page_content)