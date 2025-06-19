pdf_filepath = '000660_SK_2023.pdf'

from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(pdf_filepath)
pages = loader.load()
print(len(pages))
print(pages[10])


from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader(pdf_filepath)
pages = loader.load()

print(len(pages))
print(pages[0].page_content)


from langchain_community.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader('./')
data = loader.load()

print(len(data))
print(data[0])
print(data[-1])