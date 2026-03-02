import asyncio
from .agent_state import AgentState
from agent.tools.container_manager import restart_container, clear_cache
from agent.tools.slack_update import send_slack_message
from agent.tools.alert_update import add_alert
from agent.tools.incident_memory import store_incident


def restart_node(state: AgentState):
    restart_container()
    return state


def clear_cache_node(state: AgentState):
    clear_cache()
    restart_container()
    return state


def build_slack_message(summary: str) -> str:
    return f"""🚨 *CRITICAL ALERT*

    Service: Demo App
    Issue: {summary}
    Impact: External API calls failing

    #ops-alert"""


def slack_node(state: AgentState):
    print("Sending Slack message with summary:", state["summary"])
    message = build_slack_message(state["summary"])
    send_slack_message(message)
    return state


def alerts_node(state: AgentState):
    add_alert(state["summary"])
    return state


async def store_memory_node(state: AgentState):
    try:

        incident = {
            "title": state.get("title"),
            "error_type": state.get("error_type"),
            "service": state.get("service"),
            "root_cause": state.get("root_cause"),
            "resolution": state.get("resolution"),
            "prevention": state.get("prevention"),
        }

        incident_id = await store_incident(incident)

        print("Stored incident:", incident_id)

        return {**state, "incident_id": incident_id}

    except Exception as e:
        import traceback

        print("ERROR in store_memory_node:", str(e))
        traceback.print_exc()
        return state
