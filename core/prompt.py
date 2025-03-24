from langchain.prompts import ChatPromptTemplate
from core.my_prompts import user_prompt, system_prompt, summarize_prompt  # basic_prompt


class Prompts:

    def get_chat_template(self):
        prompt_template = ChatPromptTemplate.from_template(user_prompt)
        return prompt_template

    def get_summarize_template(self):
        prompt_template = ChatPromptTemplate.from_template(summarize_prompt)
        return prompt_template

    def get_system_prompt_template(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}")
            ]
        )

        return prompt
