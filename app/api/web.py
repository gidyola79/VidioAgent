from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.graph import app_graph
from langchain_core.messages import HumanMessage

router = APIRouter()

class AnalyzeRequest(BaseModel):
    name: str | None = None
    business_type: str | None = None
    text: str

class AnalyzeResponse(BaseModel):
    analysis: str

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text using the LangGraph agent for the web frontend.
    """
    try:
        # Prepare the state for the agent
        # We could inject user profile info into the state if the graph supports it
        # For now, we just pass the text message
        initial_state = {"messages": [HumanMessage(content=request.text)]}
        
        # Invoke the agent
        result = app_graph.invoke(initial_state)
        
        # Extract the final AI response
        ai_message = result["messages"][-1]
        response_text = ai_message.content
        
        return AnalyzeResponse(analysis=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
