import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from env import OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever


loader = PyMuPDFLoader('data/300720_한일시멘트_2023.pdf')
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200,
    encoding_name='cl100k_base'
)

documents = text_splitter.split_documents(data)

embeddings_model = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sbert-nli',
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True},
)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings_model
)


# Base retriever
question = '한일시멘트의 주요 임원에 대해 알려줘.'

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
    max_tokens=500,
)

base_retriever = vectorstore.as_retriever(
                                search_type='mmr',
                                search_kwargs={'k':7, 'fetch_k': 20})

docs = base_retriever.get_relevant_documents(question)
print(len(docs))

# Contextual compression
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=base_retriever
)

compressed_docs = compression_retriever.get_relevant_documents(question)
print(len(compressed_docs))
print(compressed_docs)