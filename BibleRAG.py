from assistant import Assistant
from retriever import Retriever
import streamlit as st
from utils import stream_data, stream_data_cmd
from dotenv import load_dotenv
import os


def gui():
    llms = ['mistral', 'gemma3:4b', 'openai']
    embedding_models = ['sentence-transformers/all-MiniLM-L6-v2', 'nomic-ai/nomic-embed-text-v1.5']
    databases = ['minilm_l6_v2_database', 'nomic_embed_text_v1.5_database']

    st.set_page_config(page_title="Bible RAG", page_icon="b")
    st.subheader('Bible RAG Application')

    st.sidebar.header("Settings")
    llm = st.sidebar.selectbox("Select an LLM", llms)
    embedding_model = st.sidebar.selectbox("Select an embedding model", embedding_models)

    database = databases[0] if embedding_model == embedding_models[0] else databases[1]

    with st.spinner('Setting everything up ...'):
        a = Assistant(model=llm)  # "gemma3:4b" mistral
        rt = Retriever(database_directory="./vector_stores/" + database)

        llm = a.setup_model()
        retriever = rt.get_basic_retriever(embedding_model=embedding_model)
        chain = a.get_basic_chain(llm, retriever)
    # -----------------UI----------------------------------
    user_input = st.chat_input(placeholder='What can I help you with today? You can type bye to quit.')
    written_stream = ''

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Display prompt
    if user_input:  # = st.chat_input(placeholder="What can I help you with today?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message('user'):
            st.write(user_input)

        # Spinner
        with st.spinner('Thinking ...'):
            with st.chat_message('assistant'):
                res = a.ask(chain, user_input)
                written_stream = st.write_stream(stream_data(res))

    if len(written_stream.strip()) > 0:
        st.session_state.messages.append({"role": "assistant", "content": written_stream})


if __name__ == "__main__":
    gui()
