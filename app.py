import streamlit as st
import os
import time
from datetime import datetime
from collections import Counter

# Load secrets if running on Streamlit Cloud
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Load Jira credentials
if "JIRA_DOMAIN" in st.secrets:
    os.environ["JIRA_DOMAIN"] = st.secrets["JIRA_DOMAIN"]
if "JIRA_EMAIL" in st.secrets:
    os.environ["JIRA_EMAIL"] = st.secrets["JIRA_EMAIL"]
if "JIRA_API_TOKEN" in st.secrets:
    os.environ["JIRA_API_TOKEN"] = st.secrets["JIRA_API_TOKEN"]

from main import app as graph_app

# Import Jira client for status display
try:
    from integrations.jira_client import get_jira_client, is_demo_mode, reset_jira_client
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False


st.set_page_config(
    page_title="IT Support Genius", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# User profiles for role switching
USER_PROFILES = {
    "Regular Employee": {"id": "user123", "icon": "👤", "desc": "Standard IT support access"},
    "Developer": {"id": "user_dev", "icon": "💻", "desc": "Engineering team member"},
    "VIP Executive": {"id": "user_ceo", "icon": "👔", "desc": "White-glove treatment"},
    "Security Analyst": {"id": "user_hacker", "icon": "🔐", "desc": "View security logs"},
    "Frustrated User": {"id": "user_angry", "icon": "😤", "desc": "Tests empathy engine"},
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = "Regular Employee"
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total_requests": 0,
        "automated": 0,
        "escalated": 0,
        "approvals_pending": 0,
        "response_times": [],
        "agent_distribution": Counter(),
        "satisfaction_scores": [],
        "confidence_scores": []
    }
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "pending_approvals" not in st.session_state:
    st.session_state.pending_approvals = []

# --- Header ---
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("🤖 IT Support Genius")
    st.caption("Multi-Agent AI System | LangGraph + Gemini + MCP")
with col2:
    # User role selector
    selected_profile = st.selectbox(
        "👤 User Role",
        options=list(USER_PROFILES.keys()),
        index=list(USER_PROFILES.keys()).index(st.session_state.user_profile),
        help="Switch between different user personas"
    )
    if selected_profile != st.session_state.user_profile:
        st.session_state.user_profile = selected_profile
        st.rerun()
with col3:
    profile = USER_PROFILES[st.session_state.user_profile]
    st.markdown(f"### {profile['icon']} {st.session_state.user_profile}")
    st.caption(profile['desc'])

# --- Tabs for main content ---
tab_chat, tab_audit, tab_about = st.tabs(["💬 Chat", "📋 Audit Log", "ℹ️ About"])

with tab_about:
    st.markdown("""
    ### Multi-Agent Architecture
    
    ```
    ┌─────────────────────────────────────────┐
    │              USER REQUEST               │
    └────────────────┬────────────────────────┘
                     ▼
    ┌─────────────────────────────────────────┐
    │          🎯 INTAKE AGENT                │
    │   Sentiment | Intent | Memory           │
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
    │         RESPONSE + CONFIDENCE           │
    └─────────────────────────────────────────┘
    ```
    
    ### ✨ Advanced Features
    
    | Feature | Description |
    |---------|-------------|
    | 🧠 **Multi-Turn Memory** | Remembers conversation context |
    | 📊 **Confidence Scores** | Shows AI certainty level |
    | 👤 **Human-in-the-Loop** | Sensitive actions need approval |
    | 📲 **Slack Simulation** | Shows notification when escalating |
    | 📋 **Audit Log** | Full transparency of all actions |
    | 👔 **Role Switching** | Test different user personas |
    """)

with tab_audit:
    st.subheader("📋 Action Audit Log")
    
    if st.session_state.audit_log:
        for entry in reversed(st.session_state.audit_log[-20:]):  # Last 20 entries
            with st.expander(f"{entry['timestamp'][:19]} | {entry['agent']} → {entry['action']}", expanded=False):
                st.json(entry)
    else:
        st.info("No actions logged yet. Start a conversation to see the audit trail.")

with tab_chat:
    # --- Sidebar ---
    with st.sidebar:
        st.header("🛠️ Controls")
        
        # Debug Mode Toggle
        debug_mode = st.toggle("🐛 Debug Mode", value=True)
        show_confidence = st.toggle("📊 Show Confidence", value=True)
        
        st.divider()
        
        # Test Scenarios
        st.subheader("🎮 Test Scenarios")
        
        scenarios = {
            "Knowledge (RAG)": [
                "What is the password policy?",
                "What's the guest Wi-Fi password?",
                "How do I expense a client dinner?",
            ],
            "Workflow (Tools)": [
                "I need a new mouse for my desk.",
                "Reset my MFA please.",
                "Check if I can upgrade my laptop.",
            ],
            "Sensitive Actions": [
                "Grant me admin access for 2 hours.",
                "Offboard user john.doe immediately.",
                "Reboot the production server.",
            ],
            "Security": [
                "Something weird is happening with my account.",
                "Check my system logs for errors.",
            ],
            "Escalation": [
                "I am absolutely furious! Nothing works!",
                "This is critical, I need help NOW!",
            ],
        }
        
        scenario_cat = st.selectbox("Category", list(scenarios.keys()))
        scenario_choice = st.selectbox("Scenario", scenarios[scenario_cat])
        
        if st.button("▶️ Run Scenario", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": scenario_choice})
            st.session_state.needs_response = True
            st.rerun()
        
        if st.button("🎲 Random", use_container_width=True):
            import random
            all_scenarios = [s for cat in scenarios.values() for s in cat]
            st.session_state.messages.append({"role": "user", "content": random.choice(all_scenarios)})
            st.session_state.needs_response = True
            st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.session_state.last_result = None
                st.rerun()
        with col2:
            if st.button("📊 Reset", use_container_width=True):
                st.session_state.metrics = {
                    "total_requests": 0,
                    "automated": 0,
                    "escalated": 0,
                    "approvals_pending": 0,
                    "response_times": [],
                    "agent_distribution": Counter(),
                    "satisfaction_scores": [],
                    "confidence_scores": []
                }
                st.session_state.audit_log = []
                st.rerun()
        
        st.divider()
        
        # --- Pending Approvals ---
        if st.session_state.pending_approvals:
            st.subheader("⚠️ Pending Approvals")
            for i, approval in enumerate(st.session_state.pending_approvals):
                with st.expander(f"🔒 {approval['action']}", expanded=True):
                    st.write(f"**Requested by:** {approval['user']}")
                    st.write(f"**Details:** {approval['details']}")
                    col1, col2 = st.columns(2)
                    if col1.button("✅ Approve", key=f"approve_{i}"):
                        st.toast(f"✅ {approval['action']} approved!")
                        st.session_state.pending_approvals.pop(i)
                        st.rerun()
                    if col2.button("❌ Deny", key=f"deny_{i}"):
                        st.toast(f"❌ {approval['action']} denied")
                        st.session_state.pending_approvals.pop(i)
                        st.rerun()
        
        st.divider()
        
        # --- Live Metrics ---
        st.subheader("📊 Live Metrics")
        
        metrics = st.session_state.metrics
        total = metrics["total_requests"]
        
        if total > 0:
            auto_rate = ((total - metrics["escalated"]) / total) * 100
            avg_time = sum(metrics["response_times"]) / len(metrics["response_times"]) if metrics["response_times"] else 0
            avg_conf = sum(metrics["confidence_scores"]) / len(metrics["confidence_scores"]) if metrics["confidence_scores"] else 0
        else:
            auto_rate = 0
            avg_time = 0
            avg_conf = 0
        
        col1, col2 = st.columns(2)
        col1.metric("Automation", f"{auto_rate:.0f}%")
        col2.metric("Avg Time", f"{avg_time:.1f}s")
        
        col3, col4 = st.columns(2)
        col3.metric("Requests", total)
        col4.metric("Avg Conf.", f"{avg_conf:.0%}")
        
        # Agent Distribution
        if metrics["agent_distribution"]:
            st.markdown("**Agent Usage:**")
            for agent, count in metrics["agent_distribution"].most_common():
                pct = (count / total) * 100 if total > 0 else 0
                st.progress(pct / 100, text=f"{agent}: {count}")
        
        # Debug Panel
        if debug_mode and st.session_state.last_result:
            st.divider()
            st.subheader("🔍 Debug")
            result = st.session_state.last_result
            
            routing_path = result.get("routing_path", [])
            if routing_path:
                st.code(" → ".join(routing_path) + " → END")
            
            col1, col2 = st.columns(2)
            sentiment = result.get("sentiment", "N/A")
            urgency = result.get("urgency", "N/A")
            col1.markdown(f"**Mood:** {sentiment}")
            col2.markdown(f"**Urgency:** {urgency}")
    
    # --- Main Chat Area ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.needs_response = True
        st.rerun()
    
    # Process AI response only if pending
    if st.session_state.get("needs_response", False):
        st.session_state.needs_response = False
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            status_placeholder = st.empty()
            
            # Animated status
            with status_placeholder:
                with st.status("🧠 Processing...", expanded=True) as status:
                    st.write("🎯 Intake Agent analyzing request...")
                    time.sleep(0.3)
                    st.write("🔀 Routing to specialist agent...")
                    time.sleep(0.3)
                    st.write("⚡ Executing...")
                    
                    start_time = time.time()
                    
                    profile = USER_PROFILES[st.session_state.user_profile]
                    initial_state = {
                        "messages": st.session_state.messages, 
                        "user_id": profile["id"],
                        "routing_path": [],
                        "audit_log": st.session_state.audit_log
                    }
                    
                    try:
                        result = graph_app.invoke(initial_state)
                        response = result['messages'][-1]['content']
                        duration = time.time() - start_time
                        
                        st.write("✅ Complete!")
                        status.update(label="✅ Done!", state="complete")
                        
                    except Exception as e:
                        response = f"❌ Error: {str(e)}"
                        duration = time.time() - start_time
                        status.update(label="❌ Error", state="error")
                        result = {"routing_path": [], "confidence": 0}
            
            status_placeholder.empty()
            
            # Update metrics
            st.session_state.metrics["total_requests"] += 1
            st.session_state.metrics["response_times"].append(duration)
            
            routing_path = result.get("routing_path", [])
            for agent in routing_path:
                st.session_state.metrics["agent_distribution"][agent] += 1
            
            if "Escalation" in routing_path:
                st.session_state.metrics["escalated"] += 1
            
            confidence = result.get("confidence", 0.5)
            st.session_state.metrics["confidence_scores"].append(confidence)
            
            # Check for pending approvals
            if result.get("requires_approval"):
                st.session_state.pending_approvals.append({
                    "action": result.get("approval_action", "Unknown"),
                    "user": profile["id"],
                    "details": st.session_state.messages[-1]["content"][:100],
                    "timestamp": datetime.now().isoformat()
                })
                st.session_state.metrics["approvals_pending"] += 1
            
            # Update audit log
            if result.get("audit_log"):
                st.session_state.audit_log = result["audit_log"]
            
            st.session_state.last_result = result
            
            # Display response
            message_placeholder.markdown(response)
            
            # Show routing if debug mode
            if debug_mode and routing_path:
                st.caption(f"🔀 {' → '.join(routing_path)} → END")
            
            st.caption(f"⏱️ {duration:.2f}s | 🤖 Gemini 2.5 Flash Lite")
            
            # Feedback buttons
            col1, col2, col3 = st.columns([1, 1, 8])
            with col1:
                if st.button("👍", key=f"up_{len(st.session_state.messages)}"):
                    st.session_state.metrics["satisfaction_scores"].append(1)
                    st.toast("Thanks! 👍")
            with col2:
                if st.button("👎", key=f"down_{len(st.session_state.messages)}"):
                    st.session_state.metrics["satisfaction_scores"].append(0)
                    st.toast("We'll improve! 👎")
            
            st.session_state.messages.append({"role": "assistant", "content": response})
