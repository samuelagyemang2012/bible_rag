import os
import re
from dotenv import load_dotenv
from tqdm import tqdm
from langchain.schema import Document
import pickle
from langchain_community.vectorstores import Chroma
from utils import parse_json, stream_data_cmd
from assistant import Assistant
from retriever import Retriever

load_dotenv()

if __name__ == "__main__":

    bible_path = "data/bible_books.json"


    def run_basic():
        a = Assistant(model="gemma3:4b")
        rt = Retriever(database_directory='./minilm_l6_v2_chapters_database')

        llm = a.setup_model()
        retriever = rt.get_summary_retriever(embedding_model='sentence-transformers/all-MiniLM-L6-v2',
                                             book='Mark',
                                             chapter=3)

        summary_docs = a.get_summary_docs(retriever=retriever)
        res = a.summarize(summary_docs=summary_docs, llm=llm)

        stream_data_cmd(res)

    run_basic()

    #pipreqs --ignore ".venv"
    # def process_json_data():
    #     books_chapters = {}
    #     json_data = parse_json(bible_path)
    #
    #     for row in json_data['books']:
    #         books_chapters[row['book']] = row['chapters']
    #
    #     return books_chapters
    #
    #
    # def generate_chapters(book, dictionary):
    #     chapters = dictionary[book]
    #     chapter_array = []
    #
    #     for i in range(1, chapters + 1):
    #         chapter_array.append(i)
    #
    #     return chapter_array
    #
    #
    # arr = generate_chapters('Mark', books_chapters)
    # print(arr)
    # def split_book_chapter(text):
    #     if not isinstance(text, str):  # Ensure input is a string
    #         raise ValueError("Input must be a string")
    #
    #         # Match cases where the book name can have numbers (like "1 John") followed by a chapter number
    #     match = re.match(r"(.+?)\s*(\d+)$", text.strip())
    #
    #     if match:
    #         book_name = match.group(1).strip()  # Extract book name (including spaces)
    #         chapter = match.group(2)  # Extract chapter number
    #         return book_name, chapter
    #     else:
    #         return None, None
    #
    #
    #         # Example Usage:
    # texts = ["genesis1", "genesis10", "1 John2", "Song of Sam1"]

    # a = "genesis1"
    # b = "genesis10"
    # c = "1 John2"
    # d = "Song of Solomon1"
    #
    # print(split_book_chapter(a))
    # print(split_book_chapter(b))
    # print(split_book_chapter(c))
    # print(split_book_chapter(d))

    # pass
    # print(os.getenv("OPEN_AI_KEY"))
    # def print_slowly(text, delay=0.02):
    #     words = text.split()
    #     for word in words:
    #         sys.stdout.write(word + " ")
    #         sys.stdout.flush()
    #         time.sleep(delay)
    #     print()  # Move to the next line after completion
    #
    #
    # # Example Usage
    # response = "This is an example of printing one word at a time like an LLM response."
    # print_slowly(response, delay=0.1)  # Adjust delay as needed
    # if torch.cuda.is_available():
    #     print('cuda')
    # else:
    #     print('cpu')
    # import requests
    #
    # url = "http://localhost:11434/api/embeddings"
    # data = {
    #     "model": "nomic-embed-text",
    #     "prompt": "Test embedding"
    # }

    # response = requests.post(url, json=data)
    # print(response.status_code, response.text)

    # from ollama import Client
    #
    # client = Client()
    # response = client.embed("nomic-embed-text", ["This is a test sentence."])
    # print(response)
