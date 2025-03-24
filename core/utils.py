import os
import pickle
import re
import textwrap
import time
import sys
import os
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from torch.nn.functional import embedding
import json

from langchain_core.documents import Document
from tqdm import tqdm


def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text


def process_llm_response(llm_response, show_source=True):
    print(wrap_text_preserve_newlines(llm_response['result']))

    if show_source:
        print('\n\nSources:')
        for source in llm_response["source_documents"]:
            print(source.metadata['source'])


def stream_data(data, delay=0.02):
    for word in data.split():
        yield word + " "
        time.sleep(delay)


def stream_data_cmd(text, delay=0.02, words_per_line=15):
    words = text.split()
    count = 0

    for word in words:
        sys.stdout.write(word + " ")
        sys.stdout.flush()
        time.sleep(delay)

        count += 1
        if count % words_per_line == 0:  # Move to a new line after 'words_per_line' words
            sys.stdout.write("\n")

    print()


def split_book_chapter(text):
    if not isinstance(text, str):  # Ensure input is a string
        raise ValueError("Input must be a string")

    # Match cases where the book name can have numbers (like "1 John") followed by a chapter number
    match = re.match(r"(.+?)\s*(\d+)$", text.strip())

    if match:
        book_name = match.group(1).strip()  # Extract book name (including spaces)
        chapter = match.group(2)  # Extract chapter number
        return book_name, chapter
    else:
        return None, None


def save(directory, data):
    # ./ docs / bible_lagchain_document.pkl
    with open(directory, 'wb') as f:  # open a text file
        pickle.dump(data, f)


def load(directory):
    with open(directory, 'rb') as f:
        data = pickle.load(f)  # deserialize using load()
    return data  # print student names


def vectorize_bible_by_chapter(bible_directory,
                               persist_directory="./vector_stores/minilm_l6_v2_chapters_database",
                               model_name="sentence-transformers/all-MiniLM-L6-v2",
                               device="cuda:0"):
    embedding_model = HuggingFaceEmbeddings(model_name=model_name,
                                            model_kwargs={"trust_remote_code": True, "device": device})
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

    for book in tqdm(os.listdir(bible_directory)):
        for chapter in os.listdir(bible_directory + book):
            if chapter.endswith(".txt"):
                # Extract book name and chapter from filename (e.g., "genesis1.txt")
                x = chapter.split(".txt")
                bk, ch = split_book_chapter(x[0])

                ch = int(ch)  # Convert to integer

                # print(bk, ch)

                # Read the entire chapter text
                with open(bible_directory + book + "/" + chapter, "r", encoding="utf-8") as file:
                    text = file.read().strip()
                #
                # # Create a single document for the entire chapter
                doc = Document(page_content=text, metadata={"book": bk, "chapter": ch})
                vector_db.add_documents([doc])
                # print(f"added {bk} chapter {ch}")


def parse_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:  # Important to specify encoding.
        data = json.load(f)
    return data


def process_json_data(data_path):
    books_chapters = {}
    books = []
    json_data = parse_json(data_path)

    for row in json_data['books']:
        books.append(row['book'])
        books_chapters[row['book']] = row['chapters']

    return books, books_chapters


def generate_chapters(book, dictionary):
    chapters = dictionary[book]
    chapter_array = []

    for i in range(1, chapters + 1):
        chapter_array.append(i)

    return chapter_array


# if __name__ == "__main__":
#     import pipreqs
    # vectorize_bible_by_chapter("D:/chrome/bible-txt/",
    #                            persist_directory='./vector_stores/nomic_embed_text_v1.5_chapters_database',
    #                            model_name='nomic-ai/nomic-embed-text-v1.5')
