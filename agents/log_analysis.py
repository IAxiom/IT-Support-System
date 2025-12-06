from state import AgentState, AuditLogger
from tools.mcp_tools import fetch_recent_logs, create_ticket
from utils.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
        
        # 1. Fetch Logs
        logs = fetch_recent_logs(user_id)
        
        # 2. Pattern-based threat detection
        detected_threats = []
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if pattern.lower() in logs.lower():
                    detected_threats.append(threat_type)
                    break
        
        # 3. Analyze with LLM
        llm = get_llm()
        template = """
        You are a Senior Site Reliability Engineer analyzing system logs.
        
        Logs:
        {logs}
        
        Provide:
        1. Root cause diagnosis (1-2 sentences)
        2. Severity (Low/Medium/High/Critical)
        3. Recommended fix
        4. Confidence score (0.0-1.0)
        
        Format: DIAGNOSIS|SEVERITY|FIX|CONFIDENCE
        Example: Database connection timeout due to network latency|High|Check network routes and increase connection timeout|0.85
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()
        
        confidence = 0.7
        severity = "Medium"
        
        try:
            result = chain.invoke({"logs": logs})
            parts = result.split("|")
            if len(parts) >= 4:
                diagnosis = parts[0].strip()
                severity = parts[1].strip()
                fix = parts[2].strip()
                try:
                    confidence = float(parts[3].strip())
                except:
                    confidence = 0.7
            else:
                diagnosis = result
                fix = "Please investigate further."
                
        except Exception as e:
            diagnosis = f"Error analyzing logs: {e}"
            fix = "Manual investigation required."
            confidence = 0.3
        
        # Build response
        response_parts = []
        
        # Threat detection header
        if detected_threats:
            unique_threats = list(set(detected_threats))
            threat_emojis = {
                "ransomware": "🔐",
                "phishing": "🎣",
                "exfiltration": "📤",
                "intrusion": "🚨"
            }
            threat_str = ", ".join([f"{threat_emojis.get(t, '⚠️')} {t.upper()}" for t in unique_threats])
            response_parts.append(f"**🚨 SECURITY ALERT:** {threat_str}\n")
            severity = "Critical"
            confidence = 0.9
        
        response_parts.append(f"**📋 Log Analysis Results:**\n")
        response_parts.append(f"**Diagnosis:** {diagnosis}")
        response_parts.append(f"**Severity:** {severity}")
        response_parts.append(f"**Recommendation:** {fix}")
        
        # Auto-create ticket if critical
        if "CRITICAL" in logs.upper() or severity == "Critical" or detected_threats:
            ticket_result = create_ticket(
                title=f"[AUTO] Security Alert: {user_id}",
                description=f"Detected: {', '.join(detected_threats) if detected_threats else diagnosis}",
                priority="Critical"
            )
            response_parts.append(f"\n**🎫 Auto-Created Ticket:** {ticket_result}")
            response_parts.append("Security team has been notified.")
        
        # Confidence indicator
        confidence_emoji = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
        response_parts.append(f"\n{confidence_emoji} *Confidence: {confidence:.0%}*")
        
        response = "\n".join(response_parts)
        
        # Log the analysis
        audit_log = AuditLogger.log(state, "LogAnalysisAgent", "logs_analyzed", {
            "user_id": user_id,
            "threats_detected": detected_threats,
            "severity": severity,
            "confidence": confidence
        })
            
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": confidence,
            "audit_log": audit_log
        }
