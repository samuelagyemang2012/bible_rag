import os

# from prompt import Prompts
from core.vectorizer import Vectorizer
from langchain.retrievers.multi_query import MultiQueryRetriever


# from my_prompts import user_prompt
# from langchain.chains.combine_documents import create_stuff_documents_chain


class Retriever:
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

    def __init__(self, database_directory):
        self.database_directory = database_directory

    def get_multiquery_retriever(self, llm, embedding_model):
        v = Vectorizer(embedding_model)

        vector_db = v.load_embeddings(self.database_directory)

        retriever = MultiQueryRetriever.from_llm(
            vector_db.as_retriever(),
            llm
        )

        return retriever

    def get_basic_retriever(self, embedding_model):
        v = Vectorizer(embedding_model)
        vector_db = v.load_embeddings(self.database_directory)
        retriever = vector_db.as_retriever()

        return retriever

    def get_summary_retriever(self, book, chapter, embedding_model):
        v = Vectorizer(embedding_model)
        vector_db = v.load_embeddings(self.database_directory)
        retriever = vector_db.as_retriever(
            search_kwargs={"filter": {"$and": [{"book": book}, {"chapter": chapter}]}})

        return retriever

    def retrieve(self, ret, query):
        docs = ret.invoke(query)
        return docs


# if __name__ == "__main__":
#     # nomic-ai/nomic-embed-text-v1.5
#     # sentence-transformers/all-MiniLM-L6-v2
#
#     rt = Retriever(database_directory='./vector_stores/minilm_l6_v2_chapters_database')
#     retriever = rt.get_summary_retriever(embedding_model='sentence-transformers/all-MiniLM-L6-v2',
#                                          book='John',
#                                          chapter=3)

    # rt.test(retriever)

    # print("fetching documents")
    # documents = retriever.get_relevant_documents("")
    # #
    # for i in range(len(documents)):
    #     print(documents[i].page_content)
    #     print("-----------------------------------------------------")
