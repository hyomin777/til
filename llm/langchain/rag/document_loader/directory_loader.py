import os
from glob import glob
from langchain_community.document_loaders import DirectoryLoader, TextLoader

files = glob(os.path.join('./', '*.txt'))
print(files)

loader = DirectoryLoader(path='./', glob='*.txt', loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
data = loader.load()
len(data)
print(data[0])
