from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA, LLMChain
from langchain_community.llms import OpenAI
from langchain_core.runnables import RunnablePassthrough
from utils import wrap_text_preserve_newlines
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import ConversationalRetrievalChain
from prompt import Prompts
import os


class Assistant:
    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

    def __init__(self, model='gemma3:4b'):
        self.model = model

    def setup_model(self):

        if self.model == 'openai':
            llm = OpenAI()
            return llm
        else:
            llm = ChatOllama(model=self.model, base_url="http://localhost:11434")
            return llm

    def get_multiquery_chain(self, llm, retriever):
        p = Prompts()
        chain = (
                {"context": retriever,
                 "question": lambda x: x["question"]
                 }
                | p.get_system_prompt_template()
                | llm
                | StrOutputParser()
        )

        return chain

    def get_basic_chain(self, llm, retriever):
        p = Prompts()
        chain = (
                {"context": retriever,
                 "question": RunnablePassthrough()
                 }
                | p.get_chat_template()
                | llm
                | StrOutputParser()
        )
        return chain

    def get_summary_data(self, retriever):
        docs = retriever.invoke("")
        book = retriever.search_kwargs['filter']['$and'][0]['book']
        chapter = retriever.search_kwargs['filter']['$and'][1]['chapter']

        p = Prompts()
        prompt = p.get_summarize_template().format(book=book, chapter=chapter, context=docs)

        return prompt

    # def get_summarize_chain(self, llm, retriever):
    #
    #     p = Prompts()
    #     chain = (
    #             {"context": retriever, "book": lambda x: x["book"], "chapter": lambda x: x["chapter"]}
    #             | p.get_summarize_template()
    #             | llm
    #     )
    #     return chain
    # #
    def ask(self, chain, question):
        try:
            result = chain.invoke(question)
            return result
        except Exception as e:
            print(e)

    def summarize(self, summary_data, llm):

        response = llm.invoke(summary_data)
        return response.content
