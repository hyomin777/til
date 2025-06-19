from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path='한국주택금융공사_주택금융관련_지수_20160101.csv', encoding='cp949')
data = loader.load()

print(len(data))
print(data[0])

loader = CSVLoader(file_path='한국주택금융공사_주택금융관련_지수_20160101.csv', encoding='cp949',
                   source_column='연도')

data = loader.load()

print(len(data))
print(data[0])