# 🤖 Multi-Agent IT Support System

> **Enterprise-Grade AI Support** powered by LangGraph, Gemini 2.5, and MCP

A sophisticated multi-agent AI system demonstrating real-world IT support automation with sentiment-aware routing, RAG-powered knowledge retrieval, and standardized tool integration via Model Context Protocol (MCP).

---

## 🎯 Key Differentiators

| Feature | Our System | Traditional Chatbots |
|---------|------------|---------------------|
| **Architecture** | Multi-agent (5 specialized) | Monolithic |
| **Routing** | LLM + Sentiment + VIP aware | Rule-based |
| **Tools** | MCP standardized | Custom APIs |
| **Knowledge** | RAG + Hallucination check | Static FAQs |
| **Escalation** | Empathy Engine | Generic handoff |

---

## 🧠 Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER REQUEST                           │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              🎯 INTAKE AGENT                                │
│   Sentiment Analysis | Intent Classification | VIP Check   │
└────────────────────────┬────────────────────────────────────┘
          ┌──────────────┼──────────────┬───────────────┐
          ▼              ▼              ▼               ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
    │📚 KNOWLEDGE│  │⚙️ WORKFLOW │  │🚨 ESCALATION│  │🔍 SECURITY │
    │   (RAG)   │  │  (Tools)  │  │ (Empathy) │  │  (Logs)   │
    └───────────┘  └───────────┘  └───────────┘  └───────────┘
```

### 5 Specialized Agents

| Agent | Responsibility | Key Features |
|-------|---------------|--------------|
| **Intake** | First contact, routing | Sentiment analysis, entity extraction, VIP auto-escalation |
| **Knowledge** | Policy/info questions | RAG with ChromaDB, hallucination detection |
| **Workflow** | Automated actions | 11 MCP tools, LLM-driven selection |
| **Escalation** | Human handoff | Empathy engine, workarounds, resolution time estimates |
| **Log Analysis** | Security threats | Ransomware, phishing, data exfiltration detection |

---

## 🔌 MCP Integration

This project showcases **Model Context Protocol** for standardized tool access:

```bash
# Run MCP demo
python mcp_server.py      # Shows 6 IT tools with discovery
python mcp_client_demo.py # Compares MCP vs traditional APIs
```

**Why MCP?**
- ✅ Standardized discovery across all systems
- ✅ Uniform interface (same `call_tool()` for everything)
- ✅ Works with VS Code, Claude Desktop, custom apps
- ✅ Enterprise-ready governance

---

## 📊 Live Metrics Dashboard

The Streamlit UI includes real-time metrics:
- **Automation Rate**: % resolved without human
- **Response Time**: Average LLM latency
- **Agent Distribution**: Which agents handle traffic
- **Satisfaction**: User feedback (👍/👎)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestration | LangGraph |
| LLM | Gemini 2.5 Flash Lite |
| Vector DB | ChromaDB |
| UI | Streamlit |
| Protocol | MCP (Model Context Protocol) |

---

## 🚀 Quick Start

```bash
# 1. Clone & Install
git clone https://github.com/IAxiom/IT-Support-System.git
cd IT-Support-System
pip install -r requirements.txt

# 2. Set API Key
export GOOGLE_API_KEY="your_key"

# 3. Initialize Knowledge Base
python setup_rag.py

# 4. Run App
streamlit run app.py
```

---

## 🧪 Testing

**Debug Mode**: Toggle in sidebar to see agent routing, sentiment, and entities.

**Scenario Categories**:
- Identity & Access (MFA, onboarding, sudo)
- Hardware (laptop refresh, peripherals)
- Network (VPN, server reboot)
- Security (phishing, log analysis)
- Knowledge (policies, HR info)
- Escalation (frustrated users, VIPs)

**CLI Testing**:
```bash
python main.py           # Full test suite
python mcp_server.py     # MCP demo
python mcp_client_demo.py # MCP integration demo
```

---

## 📚 Documentation

- [Product Spec](./docs/PRODUCT_SPEC.md) - Personas, metrics, architecture
- [Competitive Analysis](./docs/COMPETITIVE_ANALYSIS.md) - vs Glean, ServiceNow, Moveworks

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Multi-agent orchestration with LangGraph
- ✅ RAG implementation with hallucination prevention
- ✅ MCP integration for standardized tool access
- ✅ Workflow automation (11 IT tasks)
- ✅ Product ownership (metrics, personas, positioning)

---

*Built with ❤️ by the Antigravity Team*
