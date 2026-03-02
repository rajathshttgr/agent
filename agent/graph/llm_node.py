import json
import re
from langchain_openai import ChatOpenAI
from .agent_state import AgentState
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def analyze_log(state: AgentState):
    print("NODE: analyze_log")
    log = state["log"]

    prompt = f"""
    You are an SRE incident classifier.

    Log:
    {log}

    Classify severity: INFO, WARNING, CRITICAL.

    CRITICAL if:
    - auth/API key failure
    - DB unavailable
    - unhandled exception/crash
    - state corruption
    - requires human fix or restart won't help

    WARNING if:
    - slow/timeout
    - memory growth
    - intermittent dependency issue

    INFO otherwise.

    If CRITICAL choose action:
    - restart_container (if restart fixes)
    - clear_cache_restart (cache/memory issue)
    - escalate_slack (if restart won't fix: bad config, invalid API key, code bug, DB down)

    Return JSON only:
    {{
    "severity": "...",
    "action": "... or null",
    "summary": "one short sentence"
    }}
    """

    response = llm.invoke(prompt)

    content = response.content.strip()

    content = re.sub(r"^```json|```$", "", content).strip()

    data = json.loads(content)
    # print("response ", data)

    return {
        "severity": data["severity"],
        "action": data.get("action"),
        "summary": data["summary"],
    }


def summarize_incident_node(state: AgentState):
    print("NODE: summarize_incident")

    prompt = f"""
    You are an SRE incident summarization agent.

    Log:
    {state['log']}

    Initial Summary:
    {state['summary']}

    Action Taken:
    {state['action']}

    Execution Status:
    {state.get('execution_status')}

    Create a structured incident report in JSON:

    {{
      "title": "...",
      "error_type": "...",
      "service": "...",
      "root_cause": "...",
      "resolution": "...",
      "prevention": "..."
    }}
    """

    response = llm.invoke(prompt)

    content = response.content.strip()
    content = content.replace("```json", "").replace("```", "").strip()

    data = json.loads(content)

    return {
        **state,
        "title": data["title"],
        "error_type": data["error_type"],
        "service": data["service"],
        "root_cause": data["root_cause"],
        "resolution": data["resolution"],
        "prevention": data["prevention"],
    }
