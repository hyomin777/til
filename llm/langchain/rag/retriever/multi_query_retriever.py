import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from env import OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings


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

vectorstore = FAISS.from_documents(
    documents,
    embedding=embeddings_model,
    distance_strategy=DistanceStrategy.COSINE
)


from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever

question = '한일시멘트에 대해 알려줘.'

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
    max_tokens=500
)

retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Set logging for the queries
import logging
logging.basicConfig()
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

unique_docs = retriever_from_llm.get_relevant_documents(query=question)
print(len(unique_docs))
print(unique_docs[0])


# ----------------------------------------------------------------------------

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

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
chain = (
    {'context': retriever_from_llm | format_docs, 'question': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Run
response = chain.invoke('한일시멘트에 대해 간단히 요약해서 설명해주세요.')
print(response)

