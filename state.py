from typing import TypedDict, List, Any, Optional
from datetime import datetime

class AgentState(TypedDict, total=False):
    # Core state
    messages: List[dict]
    user_id: str
    next_agent: str
    
    # Routing & Analysis
    routing_path: List[str]
    entities: dict
    sentiment: str
    urgency: str
    
    # Advanced Features
    confidence: float                # 0.0-1.0 confidence in response
    confidence_reason: str           # Why this confidence level
    requires_approval: bool          # Human-in-the-loop flag
    approval_action: str             # Action awaiting approval
    conversation_summary: str        # Multi-turn context summary
    audit_log: List[dict]            # Action history
    
    # Legacy
    current_context: dict


class AuditLogger:
    """
    Centralized audit logging for all agent actions.
    Provides transparency and traceability.
    """
    
    @staticmethod
    def log(state: AgentState, agent: str, action: str, details: dict = None) -> List[dict]:
        """Add an entry to the audit log"""
        log = state.get("audit_log", [])
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "user_id": state.get("user_id", "unknown"),
            "details": details or {}
        }
        log.append(entry)
        return log


# Actions that require human approval
SENSITIVE_ACTIONS = [
    "offboard_user",
    "grant_temp_admin",
    "reboot_server",  # Only for prod
    "delete_account",
]

def requires_approval(action: str, args: dict = None) -> bool:
    """Check if an action requires human-in-the-loop approval"""
    if action in SENSITIVE_ACTIONS:
        # Production server reboots always need approval
        if action == "reboot_server" and args:
            if "prod" in str(args.get("server_id", "")).lower():
                return True
        return action != "reboot_server"  # Other sensitive actions need approval
    return False
