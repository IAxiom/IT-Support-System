from state import AgentState, AuditLogger, requires_approval
from tools.mcp_tools import (
    check_vpn_status, unlock_account, check_license_availability, provision_license,
    reset_mfa, onboard_user, offboard_user, grant_temp_admin,
    check_hardware_eligibility, order_peripheral, reboot_server, submit_facility_request
)
from utils.llm import select_tool
import json

class WorkflowAgent:
    def __init__(self):
        self.TOOL_REGISTRY = {
            "check_vpn_status": {"func": check_vpn_status, "desc": "Check VPN connection status", "sensitive": False},
            "unlock_account": {"func": unlock_account, "desc": "Unlock a user account", "sensitive": False},
            "provision_license": {"func": provision_license, "desc": "Provision software license", "sensitive": False},
            "reset_mfa": {"func": reset_mfa, "desc": "Reset MFA/2FA", "sensitive": False},
            "onboard_user": {"func": onboard_user, "desc": "Onboard new employee", "sensitive": False},
            "offboard_user": {"func": offboard_user, "desc": "Offboard/disable user", "sensitive": True},
            "grant_temp_admin": {"func": grant_temp_admin, "desc": "Grant temporary admin access", "sensitive": True},
            "check_hardware_eligibility": {"func": check_hardware_eligibility, "desc": "Check laptop refresh eligibility", "sensitive": False},
            "order_peripheral": {"func": order_peripheral, "desc": "Order hardware (mouse, keyboard, monitor)", "sensitive": False},
            "reboot_server": {"func": reboot_server, "desc": "Reboot a server", "sensitive": True},
            "submit_facility_request": {"func": submit_facility_request, "desc": "Report facility issues", "sensitive": False}
        }

    def run(self, state: AgentState):
        print("--- Workflow Agent ---")
        user_id = state.get("user_id", "unknown_user")
        messages = state['messages']
        last_message = messages[-1]['content']
        
        # Tool descriptions for LLM
        tools_desc = "\n".join([f"- {name}: {meta['desc']}" for name, meta in self.TOOL_REGISTRY.items()])
        
        # Select tool
        selection = select_tool(last_message, tools_desc)
        tool_name = selection.get("tool_name", "None")
        args = selection.get("arguments", {})
        reasoning = selection.get("reasoning", "")
        
        print(f"Selected: {tool_name} | Reason: {reasoning}")
        
        confidence = 0.85
        requires_human_approval = False
        
        if tool_name in self.TOOL_REGISTRY:
            tool = self.TOOL_REGISTRY[tool_name]
            func = tool["func"]
            is_sensitive = tool.get("sensitive", False)
            
            if "user_id" not in args:
                args["user_id"] = user_id
            
            if is_sensitive or requires_approval(tool_name, args):
                requires_human_approval = True
                response = f"""⚠️ **Approval Required**

The action `{tool_name}` requires human approval before execution.

| Parameter | Value |
|-----------|-------|
| **Action** | {tool_name} |
| **User** | {user_id} |
| **Reason** | {reasoning} |

🔔 *A notification has been sent to IT Security for approval.*

You will be notified once approved.

🟢 *Confidence: 95%*"""
                confidence = 0.95
                
                audit_log = AuditLogger.log(state, "WorkflowAgent", "approval_requested", {
                    "tool": tool_name, "args": args
                })
            else:
                try:
                    result = func(**args)
                    response = f"""🔧 **Executing:** `{tool_name}`

✅ **Result:** {result}"""
                    
                    # VPN locked account auto-remediation
                    if tool_name == "check_vpn_status" and result == "Account Locked":
                        unlock_res = unlock_account(user_id)
                        response += f"\n\n🔄 Detected locked account. Auto-remediating...\n✅ **Follow-up:** {unlock_res}"
                    
                    response += f"\n\n🟢 *Confidence: {confidence:.0%}*"
                    
                    audit_log = AuditLogger.log(state, "WorkflowAgent", "tool_executed", {
                        "tool": tool_name, "result": str(result)[:100]
                    })
                        
                except Exception as e:
                    response = f"❌ **Error:** {e}\n\n🔴 *Confidence: 30%*"
                    confidence = 0.3
                    audit_log = AuditLogger.log(state, "WorkflowAgent", "tool_error", {"error": str(e)})
        else:
            response = f"""I couldn't match your request to a specific tool. 

Let me help you manually or connect you with IT support.

📞 **IT Support:** (555) 123-4567

🟡 *Confidence: 40%*"""
            confidence = 0.4
            audit_log = AuditLogger.log(state, "WorkflowAgent", "no_match", {"query": last_message[:50]})

        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": confidence,
            "requires_approval": requires_human_approval,
            "approval_action": tool_name if requires_human_approval else None,
            "audit_log": audit_log
        }
