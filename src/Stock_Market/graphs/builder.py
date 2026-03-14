from langgraph.graph import START,END,StateGraph
from src.Stock_Market.models.state_model import State
from src.Stock_Market.nodes import (
 decider_node,
 llm_node,
 responder_node,
 sentiment_analyser_node,
 tool_node   
)

agent_builder=StateGraph(State)

agent_builder.add_node("llm_call",llm_node.llm_call)
agent_builder.add_node("tool_node",tool_node.tool_node)
agent_builder.add_node("responder",responder_node.responder)

agent_builder.add_edge(START,"llm_call")
agent_builder.add_conditional_edges("llm_call",decider_node.should_continue,['tool_node',"responder"])

agent_builder.add_edge("tool_node","llm_call")
agent_builder.add_edge("responder",END)


agent=agent_builder.compile()


try:
    with open("graph.png","wb") as f:
        f.write(agent.get_graph().draw_mermaid_png())
except Exception as e:
    print(f"Graph rendering failed: {e}")