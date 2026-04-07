from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.core.config import settings
import json


llm = ChatOpenAI(
    temperature=0,
    openai_api_key=settings.OPENAI_API_KEY,
    model=settings.MODEL_NAME,
)

prompt = ChatPromptTemplate.from_template("""
Extract structured search filters from the user query.

Return JSON with:
- query
- max_price
- brand
- vehicle

User Query: {input}
""")


def parse_query(user_query: str) -> dict:
    chain = prompt | llm
    response = chain.invoke({"input": user_query})

    try:
        return json.loads(response.content)
    except Exception:
        return {"query": user_query}