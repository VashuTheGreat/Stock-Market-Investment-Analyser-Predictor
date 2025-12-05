from pydantic.fields import Field
import json
from langchain.tools import tool

from langchain.chat_models import init_chat_model

from langchain.messages import AnyMessage,SystemMessage,ToolMessage,HumanMessage,AIMessage
from typing_extensions import TypedDict ,Annotated,Literal
from langgraph.graph import StateGraph,START,END
import operator
from analysis import analyze_multiple_stocks
from newsFetch import news_fetcher
from pydantic import BaseModel
import vconsoleprint
from dotenv import load_dotenv
load_dotenv()


class MessagesState(TypedDict):
    messages:Annotated[list[AnyMessage],operator.add]
    llm_calls:int

class structuredOutput(BaseModel):
    suggestions:str=Field(description="suggestion summary of all the stocks in human readable formate and suggest him to invest in this company top company ok")
    stocks:dict[str,dict[str,str]]=Field(description="stocks to invest in along with the reasion in human readable formate summary type")    

model = init_chat_model(
    "openai/gpt-oss-20b",
    model_provider="groq",
    temperature=0
)


@tool
def multiple_stock_analysis(companiesTickers: list[str])->json:
    """
    companiesTickers contains the tickers of the companies
    Args:
    companiesTickers: list of tickers
    """
    # indian_stocks = ["TCS.NS", "INFY.NS", "HDFCBANK.NS"] 
    indian_stocks = analyze_multiple_stocks(companiesTickers) 
    result = {k: v for k, v in indian_stocks.items() if 'error' not in v}
    return result


@tool
def sentiment_analysis(ticker:str)->list[str]:
    """
    ticker contains the ticker of the company
    Args:
    ticker: ticker of the company
    """
    news_content = news_fetcher(ticker)
    news_content = json.dumps(news_content)

    result=model.invoke([
        SystemMessage(
            content="You are a helpful assistent who can help users with their investment decisions. do only sentiment analysis of the news articles of the company."
        ),
        HumanMessage(content=news_content)
    ])
    return result.content





tools=[multiple_stock_analysis,sentiment_analysis]

tools_by_name={tool.name:tool for tool in tools}

model_with_tools=model.bind_tools(tools)



def llm_call(state:dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages":[
            
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="""You are a helpful assistent who can help users with their investment decisions.
                        use the tools provided to you to analysis and suggest user to at which stock he has to investe and kisme invest nahi karna 
                        you are given with two tools sentiment analyses and multiple stock analysis 
                        sentiment analysis will give you the sentiment of the news articles of the company
                        multiple stock analysis will give you the technical analysis of the company 
                        at the end also give top to bottom rank comapainies to invest along with the reason"""

                    )
                    
                ]
                +state['messages']
            ),
                    
                    ],
            "llm_calls":state.get('llm_calls',0)+1

    }



def tool_node(state:dict):
    """Performs the tool call"""

    result=[]
    for tool_call in state['messages'][-1].tool_calls:
        tool=tools_by_name[tool_call['name']]
        observation=tool.invoke(tool_call['args'])
        result.append(ToolMessage(content=str(observation),tool_call_id=tool_call['id']))
    return {"messages":result}
    




def responder(state:dict):
    """Generates structured output"""
    messages = state['messages']
    
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
    
    model_structured_only = model.with_structured_output(structuredOutput)
    response = model_structured_only.invoke(clean_messages)
    return {"messages":[AIMessage(content=response.model_dump_json())]}

def should_continue(state:MessagesState)->Literal["tool_node","responder"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages=state['messages']
    last_message=messages[-1]

    if last_message.tool_calls:
        return "tool_node"
    
    return "responder"




agent_builder=StateGraph(MessagesState)

agent_builder.add_node("llm_call",llm_call)
agent_builder.add_node("tool_node",tool_node)
agent_builder.add_node("responder",responder)

agent_builder.add_edge(START,"llm_call")
agent_builder.add_conditional_edges("llm_call",should_continue,['tool_node',"responder"])

agent_builder.add_edge("tool_node","llm_call")
agent_builder.add_edge("responder",END)


agent=agent_builder.compile()


# from IPython.display import Image,display

# display(Image(agent.get_graph(xray=True).draw_mermaid_png()))


def give_analysis(ticker_list:list=["AAPL", "MSFT", "GOOGL"]):
    messages=[HumanMessage(content=f"suggest me some stocks to buy of the following list: {ticker_list}")]
    messages=agent.invoke({"messages":messages})
    return messages['messages'][-1].content


if __name__=="__main__":
    result=give_analysis()
    print(type(result))
    print(result)
    

