from langchain_ollama import ChatOllama

from config import LLM_MODEL


class LLM:

    def __init__(self):
        self.model = ChatOllama(
            model=LLM_MODEL,
            temperature=0
        )

    def generate(self, prompt):

        response = self.model.invoke(prompt)

        return response.content