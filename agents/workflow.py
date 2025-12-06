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
        # Define the Registry of Capabilities (The 20 Tasks)
        self.TOOL_REGISTRY = {
            "check_vpn_status": {"func": check_vpn_status, "desc": "Check VPN connection status. Args: user_id", "sensitive": False},
            "unlock_account": {"func": unlock_account, "desc": "Unlock a user account. Args: user_id", "sensitive": False},
            "provision_license": {"func": provision_license, "desc": "Provision software license. Args: user_id, software_name", "sensitive": False},
            "reset_mfa": {"func": reset_mfa, "desc": "Reset Multi-Factor Authentication (MFA/2FA). Args: user_id", "sensitive": False},
            "onboard_user": {"func": onboard_user, "desc": "Onboard a new employee. Args: name, department", "sensitive": False},
            "offboard_user": {"func": offboard_user, "desc": "Offboard/Disable a user. Args: user_id", "sensitive": True},
            "grant_temp_admin": {"func": grant_temp_admin, "desc": "Grant temporary admin/sudo access. Args: user_id, duration_hours", "sensitive": True},
            "check_hardware_eligibility": {"func": check_hardware_eligibility, "desc": "Check if user is eligible for laptop refresh. Args: user_id", "sensitive": False},
            "order_peripheral": {"func": order_peripheral, "desc": "Order hardware peripherals (monitor, mouse, keyboard). Args: user_id, item", "sensitive": False},
            "reboot_server": {"func": reboot_server, "desc": "Reboot a server. Args: server_id", "sensitive": True},
            "submit_facility_request": {"func": submit_facility_request, "desc": "Report facility issues (meeting rooms, printers). Args: location, issue", "sensitive": False}
        }

    def run(self, state: AgentState):
        print("--- Workflow Agent (Creative/Dynamic) ---")
        user_id = state.get("user_id", "unknown_user")
        messages = state['messages']
        last_message = messages[-1]['content']
        
        # Check for conversation context
        conversation_summary = state.get("conversation_summary", "")
        context_aware_message = last_message
        if conversation_summary:
            context_aware_message = f"Previous context: {conversation_summary}\n\nCurrent request: {last_message}"
        
        # 1. Construct Tool Descriptions for the LLM
        tools_desc = "\n".join([f"- {name}: {meta['desc']}" for name, meta in self.TOOL_REGISTRY.items()])
        
        # 2. Ask LLM to Select a Tool
        selection = select_tool(context_aware_message, tools_desc)
        tool_name = selection.get("tool_name")
        args = selection.get("arguments", {})
        reasoning = selection.get("reasoning", "")
        
        print(f"LLM Selection: {tool_name} | Reason: {reasoning}")
        
        response_steps = []
        confidence = 0.85  # Workflow actions are high confidence when tool matches
        requires_human_approval = False
        
        if tool_name in self.TOOL_REGISTRY:
            tool = self.TOOL_REGISTRY[tool_name]
            func = tool["func"]
            is_sensitive = tool.get("sensitive", False)
            
            # Inject user_id if missing and required
            if "user_id" not in args and "user_id" in tool["desc"]:
                args["user_id"] = user_id
            
            # Check if this action requires human approval
            if is_sensitive or requires_approval(tool_name, args):
                requires_human_approval = True
                response_steps.append(f"⚠️ **Approval Required**")
                response_steps.append(f"The action `{tool_name}` requires human approval.")
                response_steps.append(f"**Parameters:** {json.dumps(args, indent=2)}")
                response_steps.append(f"**Reason:** {reasoning}")
                response_steps.append("")
                response_steps.append("🔔 *A notification has been sent to IT Security for approval.*")
                response_steps.append("*You will be notified once approved.*")
                confidence = 0.95  # High confidence in the routing decision
                
                # Log the pending approval
                audit_log = AuditLogger.log(state, "WorkflowAgent", "approval_requested", {
                    "tool": tool_name,
                    "args": args,
                    "reason": reasoning
                })
            else:
                try:
                    # 3. Execute the Tool
                    response_steps.append(f"🔧 Executing: `{tool_name}`...")
                    result = func(**args)
                    response_steps.append(f"✅ **Result**: {result}")
                    
                    # Special handling for VPN locked accounts (Chained Workflow)
                    if tool_name == "check_vpn_status" and result == "Account Locked":
                        response_steps.append("")
                        response_steps.append("🔄 Detected locked account. Auto-remediating...")
                        unlock_res = unlock_account(user_id)
                        response_steps.append(f"✅ Follow-up: {unlock_res}")
                    
                    # Log successful execution
                    audit_log = AuditLogger.log(state, "WorkflowAgent", "tool_executed", {
                        "tool": tool_name,
                        "args": args,
                        "result": str(result)[:200]
                    })
                        
                except Exception as e:
                    response_steps.append(f"❌ Error executing tool: {e}")
                    confidence = 0.3
                    audit_log = AuditLogger.log(state, "WorkflowAgent", "tool_error", {
                        "tool": tool_name,
                        "error": str(e)
                    })
        else:
            response_steps.append("🤔 I couldn't match your request to a specific workflow tool.")
            response_steps.append("I've noted this for the engineering team.")
            confidence = 0.4
            audit_log = AuditLogger.log(state, "WorkflowAgent", "no_tool_match", {
                "query": last_message[:100]
            })
        
        # Add confidence indicator
        confidence_emoji = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
        response_steps.append(f"\n{confidence_emoji} *Confidence: {confidence:.0%}*")

        return {
            "messages": [{"role": "assistant", "content": "\n".join(response_steps)}],
            "next_agent": "END",
            "confidence": confidence,
            "requires_approval": requires_human_approval,
            "approval_action": tool_name if requires_human_approval else None,
            "audit_log": audit_log if 'audit_log' in dir() else state.get("audit_log", [])
        }
