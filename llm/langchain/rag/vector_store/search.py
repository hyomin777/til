# maximum marginal relevance search
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
len(documents)

# Embedding -> Upload to Vectorstore
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sroberta-nli',
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True},
)
db = Chroma.from_documents(
    documents, 
    embeddings_model,
    collection_name = 'esg',
    persist_directory = './db/chromadb',
    collection_metadata = {'hnsw:space': 'cosine'}, # l2 is the default
)

# similarity search
query = '한일 시멘트 CEO는 누구야?'
docs = db.similarity_search(query)
print('Similarity Search: \n')
print(len(docs))
print(docs[0].page_content)

# mmr search
mmr_docs = db.max_marginal_relevance_search(query, k=4, fetch_k=10)
print('MMR Search: \n')
print(len(mmr_docs))
print(mmr_docs[0].page_content)