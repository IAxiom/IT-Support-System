# IT Support System - Use Case Definitions

> Product Owner Documentation for Multi-Agent AI System

---

## Executive Summary

This document defines the core IT support use cases handled by our Multi-Agent AI System. Each use case follows the structured format: Actors, Triggers, Inputs, Process, Outputs, and Success Metrics.

---

## Use Case 1: Password Reset & Account Lockout

### Definition
Automated resolution of password resets and locked account situations.

| Element | Description |
|---------|-------------|
| **Actors** | End User, AI Intake Agent, AI Workflow Agent |
| **Triggers** | User locked out, forgot password, MFA issues |
| **Inputs** | User ID, authentication verification |
| **Process** | 1. User describes issue → 2. Intake classifies → 3. Workflow executes unlock/reset → 4. Confirmation |
| **Outputs** | Unlocked account, password reset link, MFA reset |

### Problem Space
| Issue | Impact |
|-------|--------|
| 40% of Tier 1 tickets are password resets | High volume, low complexity waste |
| Average 15-min wait for human response | User productivity loss |
| After-hours lockouts unaddressed | Business continuity risk |

### Success Metrics
- ✅ Resolution time: **< 2 minutes** (vs 15-min baseline)
- ✅ Automation rate: **95%** of password issues
- ✅ 24/7 availability
- ⏱️ MTTR reduction: **85%**

---

## Use Case 2: Software Installation & Troubleshooting

### Definition
Automated software provisioning, license management, and troubleshooting.

| Element | Description |
|---------|-------------|
| **Actors** | End User, Manager (approval), AI Workflow Agent |
| **Triggers** | New software request, license expired, app crashes |
| **Inputs** | Software name, user role, department |
| **Process** | 1. Request received → 2. License availability check → 3. Auto-provision or queue for approval → 4. Deploy |
| **Outputs** | Software installed, license key, troubleshooting steps |

### Problem Space
| Issue | Impact |
|-------|--------|
| License tracking is manual | Compliance risk, wasted spend |
| Approval chains delay onboarding | Productivity loss |
| Troubleshooting requires specialist | Bottleneck on Tier 2 |

### Success Metrics
- ✅ License provisioning: **< 5 minutes**
- ✅ Troubleshooting first-contact resolution: **70%**
- ✅ License utilization visibility: **100%**

---

## Use Case 3: Hardware Diagnostics & Refresh

### Definition
Automated hardware eligibility checks, peripheral ordering, and diagnostic guidance.

| Element | Description |
|---------|-------------|
| **Actors** | End User, AI Workflow Agent, Procurement |
| **Triggers** | Laptop slow, monitor broken, refresh request |
| **Inputs** | User ID, device type, purchase date |
| **Process** | 1. Intake classifies → 2. Check eligibility (3-year policy) → 3. Auto-order or guide troubleshooting → 4. Ticket for procurement |
| **Outputs** | Eligibility status, order confirmation, diagnostic steps |

### Problem Space
| Issue | Impact |
|-------|--------|
| Users don't know refresh eligibility | Unnecessary requests |
| Peripheral ordering is manual | Slow fulfillment |
| Hardware issues misdiagnosed | Multiple ticket reopens |

### Success Metrics
- ✅ Eligibility check: **Instant**
- ✅ Peripheral order to ship: **< 24 hours**
- ✅ Diagnostic accuracy: **80%** first-attempt

---

## Use Case 4: VPN & Network Connectivity

### Definition
Automated VPN troubleshooting and network issue resolution.

| Element | Description |
|---------|-------------|
| **Actors** | End User (remote), AI Knowledge Agent, AI Workflow Agent |
| **Triggers** | VPN won't connect, slow speeds, network unreachable |
| **Inputs** | User location, VPN client version, error codes |
| **Process** | 1. Knowledge retrieval (WiFi guide) → 2. Check VPN status → 3. Guided troubleshooting → 4. Escalate if unresolved |
| **Outputs** | Step-by-step fix, VPN gateway switch, escalation ticket |

### Problem Space
| Issue | Impact |
|-------|--------|
| Remote workers flood helpdesk | 30% of tickets are network-related |
| Troubleshooting steps not documented | Repeated questions |
| ISP vs corporate issue unclear | Misrouted tickets |

### Success Metrics
- ✅ Self-service resolution: **60%** of network issues
- ✅ Knowledge base coverage: **13 network docs**
- ✅ Misrouted tickets: **< 10%**

---

## Use Case 5: Ticket Classification & Triage

### Definition
AI-powered intent classification, sentiment analysis, and intelligent routing.

| Element | Description |
|---------|-------------|
| **Actors** | End User, AI Intake Agent, Escalation Agent |
| **Triggers** | Any support request |
| **Inputs** | Natural language message, user context |
| **Process** | 1. LLM analyzes intent, sentiment, urgency → 2. VIP detection → 3. Route to appropriate agent → 4. Auto-escalate if frustrated |
| **Outputs** | Routed request, priority assignment, sentiment flag |

### Problem Space
| Issue | Impact |
|-------|--------|
| Manual triage takes 5-10 min per ticket | Bottleneck |
| Sentiment not captured | Frustrated users ignored |
| VIPs not prioritized | Executive complaints |

### Success Metrics
- ✅ Classification accuracy: **90%+**
- ✅ Triage time: **< 3 seconds**
- ✅ VIP auto-escalation: **100%**
- ✅ Sentiment detection: **4 levels** (Positive/Neutral/Negative/Frustrated)

---

## Use Case 6: New User Onboarding & Provisioning

### Definition
Automated account creation, system access, and equipment provisioning.

| Element | Description |
|---------|-------------|
| **Actors** | HR, Manager, AI Workflow Agent |
| **Triggers** | New hire form submitted |
| **Inputs** | Name, department, role, start date |
| **Process** | 1. HR submits → 2. Create email & Slack → 3. Provision equipment → 4. Send welcome packet |
| **Outputs** | Active accounts, assigned hardware, onboarding ticket |

### Problem Space
| Issue | Impact |
|-------|--------|
| Onboarding takes 3+ days | New hire unproductive |
| Department-specific access missed | Security gaps |
| Manual checklist prone to errors | Incomplete provisioning |

### Success Metrics
- ✅ Onboarding time: **< 4 hours** (vs 3 days)
- ✅ Checklist completion: **100%** automated
- ✅ First-day readiness: **95%**

---

## Use Case 7: Security Incident Detection

### Definition
Automated log analysis for threats: phishing, ransomware, data exfiltration.

| Element | Description |
|---------|-------------|
| **Actors** | AI Log Analysis Agent, Security Team |
| **Triggers** | Suspicious activity, security alerts |
| **Inputs** | System logs, user behavior patterns |
| **Process** | 1. Fetch logs → 2. Pattern matching → 3. LLM analysis → 4. Auto-create security ticket |
| **Outputs** | Threat classification, severity, auto-ticket |

### Problem Space
| Issue | Impact |
|-------|--------|
| Log review is manual | Threats missed |
| Alert fatigue | Real issues buried |
| After-hours incidents undetected | Extended exposure |

### Success Metrics
- ✅ Threat patterns detected: **4 types** (ransomware, phishing, exfiltration, intrusion)
- ✅ Detection to ticket: **< 1 minute**
- ✅ 24/7 monitoring: **Automated**

---

## Cross-Cutting Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| **Automation Rate** | 80% | (Total - Escalated) / Total |
| **Avg Response Time** | < 3 seconds | LLM latency |
| **User Satisfaction** | ≥ 4.5/5 | Feedback buttons |
| **First Contact Resolution** | 70% | Resolved without escalation |
| **MTTR Reduction** | 50% | Before/after comparison |
| **Ticket Volume Reduction** | 40% | Self-service deflection |

---

## System Dependencies

| System | Integration | Status |
|--------|-------------|--------|
| Jira Cloud | Ticket creation | ✅ Live |
| Active Directory | Account operations | 🔧 Simulated |
| Slack | Notifications | 🔧 Simulated |
| ChromaDB | Knowledge base | ✅ Live |
| Gemini LLM | Analysis & generation | ✅ Live |

---

*Document Version: 2.0 | Last Updated: 2025-12-06*
