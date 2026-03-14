

from langchain.chat_models import init_chat_model
from src.Stock_Market.constants import MODEL_NAME,MODEL_PROVIDER_NAME
llm = init_chat_model(
    MODEL_NAME,
    model_provider=MODEL_PROVIDER_NAME,
    temperature=0
)
