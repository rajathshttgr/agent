from .agent_state import AgentState


def route_action(state: AgentState):
    severity = state.get("severity")
    action = state.get("action")

    if severity == "WARNING":
        return "alerts_node"

    if severity == "CRITICAL":

        if action == "restart_container":
            return "restart_node"

        if action == "clear_cache_restart":
            return "clear_cache_node"

        return "slack_node"

    return "store_memory"
