from state import AgentState, AuditLogger
from tools.mcp_tools import fetch_recent_logs, create_ticket
import random

class LogAnalysisAgent:
    def __init__(self):
        self.threat_patterns = {
            "ransomware": ["encrypt", ".crypt", "ransom", "bitcoin", "wannacry"],
            "phishing": ["phishing", "credential", "harvest", "suspicious link"],
            "exfiltration": ["exfil", "large upload", "dropbox", "sensitive data"],
            "intrusion": ["unauthorized", "port scan", "brute force", "failed login"],
        }

    def run(self, state: AgentState):
        print("--- Log Analysis Agent ---")
        user_id = state.get("user_id", "unknown_user")
        
        # Fetch logs
        logs = fetch_recent_logs(user_id)
        
        # Pattern detection
        detected_threats = []
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if pattern.lower() in logs.lower():
                    detected_threats.append(threat_type)
                    break
        
        # Determine severity
        severity = "Medium"
        confidence = 0.7
        
        if detected_threats:
            severity = "Critical"
            confidence = 0.9
            threat_str = ", ".join([f"**{t.upper()}**" for t in set(detected_threats)])
            diagnosis = f"Security threats detected: {threat_str}"
            fix = "Immediately isolate affected systems. Security team has been notified."
        elif "error" in logs.lower():
            severity = "High"
            confidence = 0.75
            diagnosis = "Error patterns detected in logs"
            fix = "Review error logs and address root cause. Consider restarting affected services."
        elif "warning" in logs.lower():
            severity = "Medium"
            diagnosis = "Warning patterns found in logs"
            fix = "Monitor closely and address if issues persist."
        else:
            severity = "Low"
            diagnosis = "No significant issues detected"
            fix = "System appears healthy. Continue monitoring."
        
        response_parts = []
        
        # Threat header
        if detected_threats:
            threat_icons = {"ransomware": "🔐", "phishing": "🎣", "exfiltration": "📤", "intrusion": "🚨"}
            threat_display = " ".join([f"{threat_icons.get(t, '⚠️')} {t.upper()}" for t in set(detected_threats)])
            response_parts.append(f"## 🚨 SECURITY ALERT\n{threat_display}\n")
        
        response_parts.append(f"""**📋 Log Analysis Results**

| Detail | Value |
|--------|-------|
| **Diagnosis** | {diagnosis} |
| **Severity** | {severity} |
| **Recommendation** | {fix} |

**Sample Logs:**
```
{logs[:200]}...
```""")
        
        # Auto-create ticket if critical
        if severity == "Critical" or detected_threats:
            ticket_result = create_ticket(
                title=f"[SECURITY] Alert for {user_id}",
                description=f"Detected: {diagnosis}",
                priority="Critical"
            )
            response_parts.append(f"\n**🎫 Security Ticket Created:** {ticket_result}")
        
        response_parts.append(f"\n{'🟢' if confidence > 0.7 else '🟡' if confidence > 0.4 else '🔴'} *Confidence: {confidence:.0%}*")
        
        response = "\n".join(response_parts)
        
        audit_log = AuditLogger.log(state, "LogAnalysisAgent", "logs_analyzed", {
            "threats": detected_threats,
            "severity": severity
        })
            
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": confidence,
            "audit_log": audit_log
        }
