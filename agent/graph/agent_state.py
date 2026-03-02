from typing import TypedDict, Optional


class AgentState(TypedDict):
    log: str
    severity: str
    action: str
    summary: str

    # incident details for memory
    service: str
    error_type: str
    resolution: str
    root_cause: str
    prevention: str
    execution_status: str
