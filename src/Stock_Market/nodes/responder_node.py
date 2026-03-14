from utils.asyncHandler import asyncHandler

from langchain_core.messages import HumanMessage,ToolMessage,SystemMessage,AIMessage

from src.Stock_Market.llm.llm_loader import llm
from src.Stock_Market.models.structure_output import structuredOutput
@asyncHandler
async def responder(state:dict):
    """Generates structured output"""
    messages = state['messages']+state['news_']
    
    user_request = None
    for msg in messages:
        if isinstance(msg, HumanMessage):
            user_request = msg.content
            break
    
    tool_results = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            tool_results.append(msg.content)
    
    clean_messages = [
        SystemMessage(content="""You are a helpful assistant who provides investment recommendations.
        Based on the technical analysis and sentiment analysis provided, give structured investment advice."""),
        HumanMessage(content=f"""Original request: {user_request}
        
Analysis results:
{chr(10).join(tool_results)}

Please provide your investment recommendations in a structured format with:
1. A suggestions field with an overall summary
2. A stocks field with each stock ticker as a key and a nested dict containing the reason for your recommendation""")
    ]
    
    model_structured_only = llm.with_structured_output(structuredOutput)
    response = model_structured_only.invoke(clean_messages)
    return {"messages":[AIMessage(content=response.model_dump_json())]}
