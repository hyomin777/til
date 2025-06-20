from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load data -> Text split
loader = PyMuPDFLoader('data/300720_한일시멘트_2023.pdf')
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200,
    encoding_name='cl100k_base'
)

documents = text_splitter.split_documents(data)
print(len(documents))

# Store embedding in vector store
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sbert-nli',
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True},
)

vectorstore = FAISS.from_documents(
    documents,
    embedding=embeddings_model,
    distance_strategy=DistanceStrategy.COSINE
)

query = '한일시멘트의 CEO가 누구인지 알려줘'

# Extract only one sentence with the highest similarity
retriever = vectorstore.as_retriever(search_kwargs={'k': 1})
docs = retriever.get_relevant_documents(query)
print(len(docs))
print(docs[0])

# MMR - Consideration of diversity (lambda_mult=0.5, lambda_mult smaller, more diversely extracted)
retriever = vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={'k': 5, 'fetch_k': 50, 'lambda_mult': 0.5}
)
docs = retriever.get_relevant_documents(query)
print(len(docs))
print(docs[0])


# Similarity score threshold
retriever = vectorstore.as_retriever(
    search_type='similarity_score_threshold',
    search_kwargs={'score_threshold': 0.1}
)

docs = retriever.get_relevant_documents(query)
print(len(docs))
print(docs[0])


# Metadata filtering
retriever = vectorstore.as_retriever(
    search_kwargs={'filter': {'format':'PDF 1.6'}}
)

docs = retriever.get_relevant_documents(query)
print(len(docs))
print(docs[0])


# -----------------------------------------------------------------------


# Generation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from env import OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Retrieval
retriever = vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={'k': 5, 'lambda_mult': 0.15}
)
docs = retriever.get_relevant_documents(query)

# Prompt
template = '''
Answer the question based only on the following context:
{context}

Question: {question}
'''

prompt = ChatPromptTemplate.from_template(template)

# Model
llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
    max_tokens=500
)

def format_docs(docs):
    return '\n\n'.join([d.page_content for d in docs])

# Chain
chain = prompt | llm | StrOutputParser()

# Run
response = chain.invoke({'context': (format_docs(docs)), 'question': query})
print(response)