from langchain_openai import ChatOpenAI
from src.core.config import settings


class LLMProvider:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_NAME,
        )

    def invoke(self, chain, payload):
        return chain.invoke(payload)