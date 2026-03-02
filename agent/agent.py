from langgraph.graph import StateGraph, END
from agent.graph.agent_state import AgentState
from agent.graph.llm_node import analyze_log, summarize_incident_node
from agent.graph.tool_nodes import (
    restart_node,
    clear_cache_node,
    slack_node,
    alerts_node,
    store_memory_node,
)
from agent.graph.action_node import route_action

builder = StateGraph(AgentState)

builder.add_node("analyze", analyze_log)
builder.add_node("restart_node", restart_node)
builder.add_node("clear_cache_node", clear_cache_node)
builder.add_node("slack_node", slack_node)
builder.add_node("alerts_node", alerts_node)
builder.add_node("store_memory", store_memory_node)
builder.add_node("summarize_incident", summarize_incident_node)

builder.set_entry_point("analyze")

builder.add_conditional_edges("analyze", route_action)

builder.add_edge("restart_node", "summarize_incident")
builder.add_edge("clear_cache_node", "summarize_incident")
builder.add_edge("slack_node", "summarize_incident")
builder.add_edge("alerts_node", "summarize_incident")
builder.add_edge("summarize_incident", "store_memory")

builder.add_edge("store_memory", END)

graph = builder.compile()


## dummy agent for testing tools
async def ops_agent(event: str):
    print("🤖 Agent triggered for event:")
    print(event[:200])
