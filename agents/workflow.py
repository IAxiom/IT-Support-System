from state import AgentState
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
            "check_vpn_status": {"func": check_vpn_status, "desc": "Check VPN connection status. Args: user_id"},
            "unlock_account": {"func": unlock_account, "desc": "Unlock a user account. Args: user_id"},
            "provision_license": {"func": provision_license, "desc": "Provision software license. Args: user_id, software_name"},
            "reset_mfa": {"func": reset_mfa, "desc": "Reset Multi-Factor Authentication (MFA/2FA). Args: user_id"},
            "onboard_user": {"func": onboard_user, "desc": "Onboard a new employee. Args: name, department"},
            "offboard_user": {"func": offboard_user, "desc": "Offboard/Disable a user. Args: user_id"},
            "grant_temp_admin": {"func": grant_temp_admin, "desc": "Grant temporary admin/sudo access. Args: user_id, duration_hours"},
            "check_hardware_eligibility": {"func": check_hardware_eligibility, "desc": "Check if user is eligible for laptop refresh. Args: user_id"},
            "order_peripheral": {"func": order_peripheral, "desc": "Order hardware peripherals (monitor, mouse, keyboard). Args: user_id, item"},
            "reboot_server": {"func": reboot_server, "desc": "Reboot a server. Args: server_id"},
            "submit_facility_request": {"func": submit_facility_request, "desc": "Report facility issues (meeting rooms, printers). Args: location, issue"}
        }

    def run(self, state: AgentState):
        print("--- Workflow Agent (Creative/Dynamic) ---")
        user_id = state.get("user_id", "unknown_user")
        messages = state['messages']
        last_message = messages[-1]['content']
        
        # 1. Construct Tool Descriptions for the LLM
        tools_desc = "\n".join([f"- {name}: {meta['desc']}" for name, meta in self.TOOL_REGISTRY.items()])
        
        # 2. Ask LLM to Select a Tool
        selection = select_tool(last_message, tools_desc)
        tool_name = selection.get("tool_name")
        args = selection.get("arguments", {})
        reasoning = selection.get("reasoning", "")
        
        print(f"LLM Selection: {tool_name} | Reason: {reasoning}")
        
        response_steps = []
        
        if tool_name in self.TOOL_REGISTRY:
            tool = self.TOOL_REGISTRY[tool_name]
            func = tool["func"]
            
            # Inject user_id if missing and required
            if "user_id" not in args and "user_id" in tool["desc"]:
                args["user_id"] = user_id
                
            try:
                # 3. Execute the Tool
                response_steps.append(f"Executing: `{tool_name}`...")
                result = func(**args)
                response_steps.append(f"**Result**: {result}")
                
                # Special handling for VPN locked accounts (Chained Workflow)
                if tool_name == "check_vpn_status" and result == "Account Locked":
                    response_steps.append("Detected locked account. Auto-remediating...")
                    unlock_res = unlock_account(user_id)
                    response_steps.append(f"Follow-up: {unlock_res}")
                    
            except Exception as e:
                response_steps.append(f"Error executing tool: {e}")
        else:
            response_steps.append("I couldn't match your request to a specific workflow tool. I've noted this for the engineering team.")

        return {
            "messages": [{"role": "assistant", "content": "\n".join(response_steps)}],
            "next_agent": "END"
        }
