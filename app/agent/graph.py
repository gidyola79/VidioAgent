from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from app.services.llm import get_llm
import operator

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next_step: str

# 2. Define Nodes
def call_model(state: AgentState):
    """
    Invokes the Llama 3 model with the current history.
    """
    messages = state["messages"]
    llm = get_llm()
    
    # Simple system prompt for now
    system_prompt = SystemMessage(content="You are VidioAgent, a helpful assistant for Nigerian MSMEs.")
    
    # Prepend system prompt if not present (simplified logic)
    if not isinstance(messages[0], SystemMessage):
        messages = [system_prompt] + messages
        
    response = llm.invoke(messages)
    return {"messages": [response]}

# 3. Define Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# 4. Compile
app_graph = workflow.compile()
