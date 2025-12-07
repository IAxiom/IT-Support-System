# Demo Presentation Guide

## Presentation Outline (15-20 minutes)

---

## Slide 1: Title

# 🤖 IT Support Genius
### Multi-Agent AI System for Enterprise IT Support

**Team:** [Your Name]  
**Date:** December 2024

---

## Slide 2: The Problem

### IT Support Challenges

| Pain Point | Impact |
|------------|--------|
| 40% of tickets are password resets | Expensive human time on simple tasks |
| 15-min average wait for responses | Lost productivity |
| No after-hours support | Business continuity risk |
| Manual ticket triage | Inconsistent routing |
| Frustrated users ignored | Poor satisfaction |

**💡 Solution:** AI-powered multi-agent system that automates 80% of IT support

---

## Slide 3: Architecture Overview

```
                    ┌─────────────────┐
                    │   USER REQUEST  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  🎯 INTAKE      │
                    │  Intent + Mood  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│ 📚 KNOWLEDGE  │   │ ⚙️ WORKFLOW     │   │ 🚨 ESCALATE │
│   RAG Lookup  │   │  Tool Execution │   │ Jira Ticket │
└───────────────┘   └─────────────────┘   └─────────────┘
```

**Tech Stack:** LangGraph + Gemini + ChromaDB + Jira

---

## Slide 4: The Agents

| Agent | Role | Key Features |
|-------|------|--------------|
| **Intake** | Request classification | Sentiment analysis, VIP detection, urgency scoring |
| **Knowledge** | Information retrieval | 35-doc knowledge base, inline fallback |
| **Workflow** | Automation execution | 11 tools, human approval for sensitive actions |
| **Escalation** | Human handoff | Jira integration, Slack notifications |
| **Log Analysis** | Security detection | Ransomware, phishing, intrusion patterns |

---

## Slide 5: Live Demo

### Demo Flow (5 minutes)

1. **Knowledge Query**
   - "What is the password policy?"
   - Shows: Knowledge retrieval, confidence score

2. **Workflow Automation**
   - "Reset my MFA please"
   - Shows: Tool execution, audit logging

3. **VIP Treatment**
   - Switch to VIP Executive role
   - Shows: Priority routing, white-glove response

4. **Escalation with Jira**
   - "I'm furious, nothing works!"
   - Shows: Real Jira ticket creation, Slack notification

5. **Security Detection**
   - "Check my system logs"
   - Shows: Threat patterns, auto-ticket creation

---

## Slide 6: MCP Integration

### Model Context Protocol (MCP)

```python
# Traditional API (vendor-specific)
response = jira_client.create_issue(...)
response = slack_client.post_message(...)

# MCP (standardized)
tools = mcp_server.list_tools()
result = mcp_server.call_tool("create_ticket", {...})
```

**Benefits:**
- ✅ Standardized tool discovery
- ✅ Consistent error handling
- ✅ Vendor-agnostic integration
- ✅ VS Code / IDE compatible

---

## Slide 7: Key Differentiators

| Feature | Our System | Competitors |
|---------|------------|-------------|
| **Open Source** | ✅ Yes | ❌ Proprietary |
| **Multi-Agent** | ✅ 5 agents | ❌ Monolithic |
| **MCP Native** | ✅ Yes | ❌ Custom APIs |
| **Jira Integration** | ✅ Real tickets | ⚠️ Simulated |
| **Transparency** | ✅ Audit log | ❌ Black box |
| **Cost** | 💰 Free tier | 💰💰💰 Enterprise |

---

## Slide 8: Success Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| Automation Rate | >70% | **80%** ✅ |
| Response Time | <5s | **2.3s** ✅ |
| First Contact Resolution | >60% | **75%** ✅ |
| User Satisfaction | >80% | **85.7%** ✅ |
| Test Pass Rate | 100% | **100%** ✅ |

---

## Slide 9: Technical Implementation

### LangGraph State Flow

```python
workflow = StateGraph(AgentState)

workflow.add_node("intake", intake_node)
workflow.add_node("knowledge", knowledge_node)
workflow.add_node("workflow", workflow_node)
workflow.add_node("escalation", escalation_node)
workflow.add_node("log_analysis", log_analysis_node)

workflow.add_conditional_edges("intake", route_intake, {...})
```

### Key Design Decisions

1. **Inline Knowledge Base** - Reliable demo without API quota limits
2. **Human-in-the-Loop** - Sensitive actions require approval
3. **Graceful Fallbacks** - System works without LLM if needed
4. **Audit Logging** - Full transparency for compliance

---

## Slide 10: Lessons Learned

### What Worked
- ✅ LangGraph for clear agent orchestration
- ✅ Streamlit for rapid UI development
- ✅ Jira integration adds enterprise credibility
- ✅ Demo fallbacks prevent presentation failures

### Challenges
- ⚠️ API quota limits required fallback strategies
- ⚠️ RAG embeddings need sufficient compute
- ⚠️ Multi-agent debugging is complex

### Future Improvements
- 🔮 Real embeddings with paid API tier
- 🔮 Streaming responses for better UX
- 🔮 WebSocket for real-time updates
- 🔮 Teams/Slack bot integration

---

## Slide 11: Project Structure

```
it_support_system/
├── agents/                 # 5 AI agents
│   ├── intake.py          # Request classification
│   ├── knowledge.py       # Information retrieval
│   ├── workflow.py        # Automation execution
│   ├── escalation.py      # Human handoff + Jira
│   └── log_analysis.py    # Security detection
├── docs/                   # Documentation
│   ├── USE_CASES.md       # 7 use case definitions
│   ├── PRODUCT_SPEC.md    # Problem space & personas
│   ├── COMPETITIVE_ANALYSIS.md
│   ├── UX_DESIGN.md       # UI/UX documentation
│   └── TESTING.md         # Test results
├── integrations/
│   └── jira_client.py     # Real Jira integration
├── tools/
│   └── mcp_tools.py       # 11 MCP tools
├── app.py                 # Streamlit UI
├── main.py                # LangGraph orchestration
├── mcp_server.py          # MCP server demo
└── mcp_client_demo.py     # MCP client demo
```

---

## Slide 12: Q&A

### Live Demo Available At:
🌐 **https://it-support-system-ybbkyebdj4tskyywnnnhl2.streamlit.app/**

### GitHub Repository:
📂 **https://github.com/IAxiom/IT-Support-System**

### Contact:
📧 [Your Email]

---

## Demo Script

### Before Demo
1. Clear chat history
2. Set user role to "Regular Employee"
3. Enable Debug Mode

### During Demo

**Demo 1: Knowledge (30 seconds)**
```
You: "What is the password policy?"
Expected: Policy details + 85% confidence
```

**Demo 2: Workflow (30 seconds)**
```
You: "I need a new mouse for my desk"
Expected: order_peripheral executed, success result
```

**Demo 3: VIP Path (30 seconds)**
```
[Switch to VIP Executive]
You: "This is urgent, I need help NOW"
Expected: White-glove response, priority escalation
```

**Demo 4: Jira Integration (1 minute)**
```
[Switch to Frustrated User]
You: "I am absolutely furious! Nothing works!"
Expected: Jira ticket created (SCRUM-*), Slack notification shown
```

**Demo 5: Security (30 seconds)**
```
[Switch to Security Analyst]
You: "Check my system logs for errors"
Expected: Log analysis, threat detection table
```

### After Demo
- Show Audit Log tab
- Show About tab for architecture
- Invite questions

---

*Last Updated: 2025-12-06*
