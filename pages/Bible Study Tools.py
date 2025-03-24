import os
from assistant import Assistant
from retriever import Retriever
import streamlit as st
from utils import stream_data

import utils

llms = ['mistral', 'gemma3:4b', 'openai']
embedding_models = ['sentence-transformers/all-MiniLM-L6-v2', 'nomic-ai/nomic-embed-text-v1.5']
databases = ['minilm_l6_v2_chapters_database', 'nomic_embed_text_v1.5_chapters_database']

# Load JSON data
data_file = os.path.join(os.path.dirname(__file__), "../data/bible_books.json")
data_file_path = os.path.abspath(data_file)
books, dictionary = utils.process_json_data(data_file_path)

# Sidebar for system settings
st.sidebar.header("Settings")
llm = st.sidebar.selectbox("Select an LLM", llms)
embedding_model = st.sidebar.selectbox("Select an embedding model", embedding_models)
database = databases[0] if embedding_model == embedding_models[0] else databases[1]

# Book selection
st.sidebar.header("Select a Book")
book = st.sidebar.selectbox("Books", books)
chapters = utils.generate_chapters(book, dictionary)
chapter = st.sidebar.selectbox("Chapters", chapters)
btn = st.sidebar.button('Generate', type="primary")

# Heading
st.subheader('Summaries and Question Generation')

with st.spinner('Setting everything up ...'):
    a = Assistant(model=llm)  # "gemma3:4b" mistral
    rt = Retriever(database_directory="./vector_stores/" + database)

    llm = a.setup_model()
    retriever = rt.get_summary_retriever(embedding_model=embedding_model, book=book, chapter=chapter)
    summary_data = a.get_summary_data(retriever)

user_input = book + " " + str(chapter)
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

if btn:

    # Display prompt
    if len(user_input) > 0:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message('user'):
            st.write(user_input)

    # Spinner

    with st.spinner('Thinking ...'):
        with st.chat_message('assistant'):
            res = a.summarize(summary_data, llm)
            st.write(res)
            # written_stream = st.write_stream(stream_data(res))

        if len(res.strip()) > 0:
            st.session_state.messages.append({"role": "assistant", "content": res})
