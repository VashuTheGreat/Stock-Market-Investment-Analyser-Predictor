
from langchain_core.messages import ToolMessage

async def tool_node(state:dict):
    """Performs the tool call"""

    result=[]
    for tool_call in state['messages'][-1].tool_calls:
        tool=state['tools_by_name'][tool_call['name']]
        observation=await tool.ainvoke(tool_call['args'])
        result.append(ToolMessage(content=str(observation),tool_call_id=tool_call['id']))
    return {"messages":result}
    
