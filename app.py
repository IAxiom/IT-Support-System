import streamlit as st
import os
import time
from collections import Counter

# Load secrets if running on Streamlit Cloud
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

from main import app as graph_app

st.set_page_config(
    page_title="IT Support Genius", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total_requests": 0,
        "automated": 0,
        "escalated": 0,
        "response_times": [],
        "agent_distribution": Counter(),
        "satisfaction_scores": []
    }

# --- Header with Branding ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🤖 IT Support Genius")
    st.caption("Multi-Agent AI System | Powered by LangGraph + Gemini")
with col2:
    st.markdown("""
    <div style='text-align: right; padding-top: 10px;'>
        <span style='font-size: 12px; color: #666;'>v2.0 | Demo Mode</span>
    </div>
    """, unsafe_allow_html=True)

# --- About This Demo (Collapsible) ---
with st.expander("ℹ️ About This Demo", expanded=False):
    st.markdown("""
    ### Multi-Agent Architecture
    
    This system uses **5 specialized AI agents** orchestrated by LangGraph:
    
    | Agent | Role |
    |-------|------|
    | 🎯 **Intake** | Sentiment analysis, intent classification, VIP detection |
    | 📚 **Knowledge** | RAG retrieval with hallucination checking |
    | ⚙️ **Workflow** | LLM-driven tool selection (11 automated actions) |
    | 🚨 **Escalation** | Empathy engine with workarounds |
    | 🔍 **Log Analysis** | Security threat detection (ransomware, phishing) |
    
    ### Key Features
    - **MCP Integration**: Standardized tool access via Model Context Protocol
    - **Real-time Metrics**: Automation rate, response time, satisfaction
    - **Debug Mode**: View agent routing and extracted entities
    """)
    
    # Visual Agent Graph (Mermaid-style)
    st.markdown("### Agent Flow Diagram")
    st.markdown("""
    ```
    ┌─────────────────────────────────────────┐
    │              USER REQUEST               │
    └────────────────┬────────────────────────┘
                     ▼
    ┌─────────────────────────────────────────┐
    │          🎯 INTAKE AGENT                │
    │   Sentiment | Intent | Entity Extract   │
    └────────────────┬────────────────────────┘
                     │
         ┌───────────┼───────────┬─────────────┐
         ▼           ▼           ▼             ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────┐
    │📚 KNOW- │ │⚙️ WORK- │ │🚨 ESCA- │ │🔍 LOG     │
    │  LEDGE  │ │  FLOW   │ │ LATION  │ │ ANALYSIS  │
    │  (RAG)  │ │ (Tools) │ │(Empathy)│ │(Security) │
    └────┬────┘ └────┬────┘ └────┬────┘ └─────┬─────┘
         │           │           │             │
         └───────────┴───────────┴─────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │               RESPONSE                  │
    └─────────────────────────────────────────┘
    ```
    """)

# --- Sidebar ---
with st.sidebar:
    st.header("🛠️ Controls")
    
    # Debug Mode Toggle
    debug_mode = st.toggle("🐛 Debug Mode", value=False, help="Show agent routing and extracted entities")
    
    st.divider()
    
    # Test Scenarios
    st.subheader("🎮 Test Scenarios")
    
    scenario_category = st.selectbox(
        "Category",
        ["All", "Identity & Access", "Hardware", "Network", "Security", "Knowledge", "Escalation"]
    )
    
    scenarios = {
        "Identity & Access": [
            {"text": "I lost my phone, reset my 2FA.", "user": "user1"},
            {"text": "Create account for new engineer John Doe.", "user": "manager1"},
            {"text": "I need sudo access for 1 hour.", "user": "dev1"},
        ],
        "Hardware": [
            {"text": "My laptop is 4 years old, can I upgrade?", "user": "user2"},
            {"text": "I need a new mouse for my desk.", "user": "designer1"},
        ],
        "Network": [
            {"text": "Reboot the dev server.", "user": "dev2"},
            {"text": "I can't connect to the VPN.", "user": "user_vpn"},
        ],
        "Security": [
            {"text": "Is this email from ceo@company-update.com safe?", "user": "user_phishing"},
            {"text": "Something weird is happening with my account.", "user": "user_hacker"},
        ],
        "Knowledge": [
            {"text": "What is the password policy?", "user": "user5"},
            {"text": "What's the guest Wi-Fi password?", "user": "visitor1"},
            {"text": "How do I expense a client dinner?", "user": "sales1"},
        ],
        "Escalation": [
            {"text": "I am absolutely furious! Nothing is working!", "user": "user_angry"},
            {"text": "My email is down and I need it NOW!", "user": "user_ceo"},
        ]
    }
    
    if st.button("🎲 Run Random", use_container_width=True):
        import random
        if scenario_category == "All":
            all_scenarios = [s for cat in scenarios.values() for s in cat]
        else:
            all_scenarios = scenarios.get(scenario_category, [])
        if all_scenarios:
            selected = random.choice(all_scenarios)
            st.session_state.messages.append({"role": "user", "content": selected["text"]})
            st.session_state.user_id = selected["user"]
            st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.rerun()
    
    if st.button("📊 Reset Metrics", use_container_width=True):
        st.session_state.metrics = {
            "total_requests": 0,
            "automated": 0,
            "escalated": 0,
            "response_times": [],
            "agent_distribution": Counter(),
            "satisfaction_scores": []
        }
        st.rerun()
    
    st.divider()
    
    # --- Metrics Dashboard ---
    st.subheader("📊 Live Metrics")
    
    metrics = st.session_state.metrics
    
    # Automation Rate
    total = metrics["total_requests"]
    if total > 0:
        auto_rate = ((total - metrics["escalated"]) / total) * 100
        avg_time = sum(metrics["response_times"]) / len(metrics["response_times"]) if metrics["response_times"] else 0
    else:
        auto_rate = 0
        avg_time = 0
    
    col1, col2 = st.columns(2)
    col1.metric("Automation", f"{auto_rate:.0f}%", help="Requests resolved without escalation")
    col2.metric("Avg Time", f"{avg_time:.1f}s", help="Average response time")
    
    col3, col4 = st.columns(2)
    col3.metric("Total", total, help="Total requests processed")
    col4.metric("Escalated", metrics["escalated"], help="Requests sent to humans")
    
    # Agent Distribution
    if metrics["agent_distribution"]:
        st.markdown("**Agent Usage:**")
        for agent, count in metrics["agent_distribution"].most_common():
            pct = (count / total) * 100 if total > 0 else 0
            st.progress(pct / 100, text=f"{agent}: {count} ({pct:.0f}%)")
    
    st.divider()
    
    # Debug Panel
    if debug_mode and st.session_state.last_result:
        st.subheader("🔍 Debug Info")
        result = st.session_state.last_result
        
        # Routing Path
        routing_path = result.get("routing_path", [])
        if routing_path:
            route_str = " → ".join(routing_path) + " → END"
            st.code(route_str, language=None)
        
        # Sentiment & Urgency
        sentiment = result.get("sentiment", "N/A")
        urgency = result.get("urgency", "N/A")
        
        sentiment_emoji = {"Positive": "😊", "Neutral": "😐", "Negative": "😕", "Frustrated": "😤"}.get(sentiment, "❓")
        urgency_color = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(urgency, "⚪")
        
        c1, c2 = st.columns(2)
        c1.markdown(f"**Sentiment:** {sentiment_emoji}")
        c2.markdown(f"**Urgency:** {urgency_color}")
        
        # Entities
        entities = result.get("entities", {})
        if entities:
            st.markdown("**Entities:**")
            st.json(entities)

# --- Main Chat Area ---
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_id = "user123"
    st.rerun()

# Process AI response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Animated thinking message
        with st.spinner("🧠 Thinking..."):
            start_time = time.time()
            
            initial_state = {
                "messages": st.session_state.messages, 
                "user_id": st.session_state.user_id,
                "routing_path": []
            }
            
            try:
                result = graph_app.invoke(initial_state)
                response = result['messages'][-1]['content']
                duration = time.time() - start_time
                
                # Update metrics
                st.session_state.metrics["total_requests"] += 1
                st.session_state.metrics["response_times"].append(duration)
                
                routing_path = result.get("routing_path", [])
                for agent in routing_path:
                    st.session_state.metrics["agent_distribution"][agent] += 1
                
                if "Escalation" in routing_path:
                    st.session_state.metrics["escalated"] += 1
                
                st.session_state.last_result = result
                
                # Display response
                message_placeholder.markdown(response)
                
                # Show routing if debug mode
                if debug_mode and routing_path:
                    route_str = " → ".join(routing_path) + " → END"
                    st.caption(f"🔀 Route: {route_str}")
                
                st.caption(f"⏱️ {duration:.2f}s | 🤖 Gemini 2.5 Flash Lite")
                
                # Feedback buttons
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("👍", key="thumbs_up"):
                        st.session_state.metrics["satisfaction_scores"].append(1)
                        st.toast("Thanks for the feedback!")
                with col2:
                    if st.button("👎", key="thumbs_down"):
                        st.session_state.metrics["satisfaction_scores"].append(0)
                        st.toast("We'll work on improving!")
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
