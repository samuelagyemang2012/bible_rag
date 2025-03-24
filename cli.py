import os
import argparse
import streamlit as st
from core.assistant import Assistant
from core.retriever import Retriever
from core.utils import stream_data_cmd
from dotenv import load_dotenv

load_dotenv()
os.environ["OPEN_AI_KEY"] = os.getenv("OPEN_AI_KEY")


def loop_cmd(llm, database, embedding_model):
    a = Assistant(model=llm)
    rt = Retriever(database_directory=database)

    model = a.setup_model()
    retriever = rt.get_basic_retriever(embedding_model=embedding_model)
    chain = a.get_basic_chain(model, retriever)

    while True:
        query = input("What can I help you with today?\n")

        if query.lower() == "bye":
            break

        res = a.ask(chain, query)

        print("")
        print("Response:")
        stream_data_cmd(res)
        print("")


if __name__ == "__main__":

    modes = ['cli', 'gui']
    llms = ['mistral', 'gemma3:4b', 'openai']
    embedding_models = ['sentence-transformers/all-MiniLM-L6-v2', 'nomic-ai/nomic-embed-text-v1.5']
    databases = ['./vector_stores/minilm_l6_v2_database', './vector_stores/nomic_embed_text_v1.5_database']

    parser = argparse.ArgumentParser(description='Bible RAG application.')

    parser.add_argument('-m', '--mode',
                        default='cli',
                        choices=modes,
                        help='Run the application in the cli or use a gui.')

    parser.add_argument('-l', '--llm',
                        default='mistral',
                        choices=llms,
                        help='The LLM to use')

    parser.add_argument('-e', "--embedding_model",
                        default='sentence-transformers/all-MiniLM-L6-v2',
                        choices=embedding_models,
                        help='The embedding model to use.')
    args = parser.parse_args()

    database = databases[0] if args.embedding_model == embedding_models[0] else databases[1]

    if args.mode == 'cli':
        database = databases[0] if args.embedding_model == embedding_models[0] else databases[1]

        loop_cmd(llm=args.llm,
                 database=database,
                 embedding_model=args.embedding_model)
    else:
        os.system("streamlit run gui.py")

# import requests
#
# session = requests.Session()
# session.trust_env = False
#
# url = 'http://localhost:11434/api/generate'
# data = {'model': 'gemma3:4b', 'prompt': 'Why is the sky blue?'}
#
# response = session.post(url, json=data)
#
# print(response.text)
