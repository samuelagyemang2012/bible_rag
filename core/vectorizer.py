import os
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from torch.nn.functional import embedding


class Vectorizer:
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

    def __init__(self, embedding_model):
        # self.type = type
        self.embedding_model = embedding_model

    def get_embedding_model(self):

        model = HuggingFaceEmbeddings(model_name=self.embedding_model, model_kwargs={"trust_remote_code": True,
                                                                                     "device": "cuda:0"})  # , model_kwargs={"device": "cuda:0"})
        return model

        # elif self.type == 'ollama':
        #     embeddings = OllamaEmbeddings(model=self.embedding_model, base_url="http://localhost:11434/api/embeddings/")
        #     return embeddings
        # else:
        #     return "Invalid argument given for model. Must be 'huggingface' or 'ollama'"

    def load_embeddings(self, persist_directory="./vector_stores/minilm_l6_v2_database/"):
        embeddings = self.get_embedding_model()
        vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        return vector_db

    def vectorize_documents(self, data_directory, persist_directory="./vector_stores/minilm_l6_v2_database/", document_type=".pdf",
                            multithreading=True, chunk_size=500, chunk_overlap=200):
        loader = None

        if document_type == ".pdf":
            loader = DirectoryLoader(data_directory, glob="./*" + document_type, loader_cls=PyPDFLoader,
                                     use_multithreading=multithreading)

        if document_type == ".txt":
            loader = DirectoryLoader(data_directory, glob="./*" + document_type, loader_cls=TextLoader,
                                     use_multithreading=multithreading)

        if document_type == ".csv":
            loader = DirectoryLoader(data_directory, glob="./*" + document_type, loader_cls=CSVLoader,
                                     use_multithreading=multithreading)

        print('loading documents')
        documents = loader.load()
        print(f"{len(documents)} loaded")

        # Splitting the text into chunks
        print('splitting documents')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(documents)

        # Embeddings
        print('loading embedding model')
        emb_model = self.get_embedding_model()

        print("embedding data")
        Chroma.from_documents(documents=texts,
                              embedding=emb_model,
                              persist_directory=persist_directory)


# if __name__ == "__main__":
#     model = 'nomic-ai/nomic-embed-text-v1.5'  # 'sentence-transformers/all-MiniLM-L6-v2'# 'nomic-ai/nomic-embed-text-v1.5'  # 'sentence-transformers/all-MiniLM-L6-v2'
#
#     v = Vectorizer(embedding_model=model)
#     v.vectorize_documents(data_directory="./data/", persist_directory='./vector_stores/nomic_embed_text_v1.5_database/')
