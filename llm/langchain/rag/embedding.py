from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

def cos_sim(A, B):
  return np.dot(A, B)/(np.linalg.norm(A)*np.linalg.norm(B))

embeddings_model = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sroberta-nli',
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True},
)

print(embeddings_model)

embeddings = embeddings_model.embed_documents(
    [
        '안녕하세요!',
        '어! 오랜만이에요',
        '이름이 어떻게 되세요?',
        '날씨가 추워요',
        'Hello LLM!'
    ]
)

print(len(embeddings), len(embeddings[0]))

embedded_query = embeddings_model.embed_query('첫인사를 하고 이름을 물어봤나요?')
for embedding in embeddings:
    print(cos_sim(embedding, embedded_query))