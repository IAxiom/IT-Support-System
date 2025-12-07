# UX Design Documentation

## Design Philosophy

Our IT Support Genius system follows these core UX principles:

### 1. Conversational First
Users interact naturally through chat, not forms or menus.

### 2. Transparency
- Debug mode shows agent routing
- Confidence scores indicate AI certainty
- Audit log provides full action history

### 3. Progressive Disclosure
- Simple chat interface by default
- Advanced features in sidebar/tabs
- Technical details available on demand

---

## User Interface Architecture

```
┌─────────────────────────────────────────────────────────┐
│  🤖 IT Support Genius                    [User Role ▼]  │
├──────────────┬──────────────────────────────────────────┤
│   SIDEBAR    │              MAIN AREA                   │
│              │  ┌────────────────────────────────────┐  │
│ 🛠️ Controls  │  │  💬 Chat  │ 📋 Audit │ ℹ️ About   │  │
│ □ Debug Mode │  ├────────────────────────────────────┤  │
│ □ Confidence │  │                                    │  │
│              │  │  👤 User: What is the password...  │  │
│ 🎮 Scenarios │  │                                    │  │
│ [Category ▼] │  │  🤖 Based on our IT documentation: │  │
│ [Scenario ▼] │  │     Password Policy: Minimum 12... │  │
│ [Run] [Rand] │  │     🟢 Confidence: 85%             │  │
│              │  │                                    │  │
│ 📊 Metrics   │  │  [👍] [👎]                         │  │
│ Auto: 80%    │  │                                    │  │
│ Time: 2.3s   │  └────────────────────────────────────┘  │
│ Conf: 85%    │  ┌────────────────────────────────────┐  │
│              │  │ How can I help you?            [>] │  │
└──────────────┴──────────────────────────────────────────┘
```

---

## Component Design

### Chat Interface
| Element | Purpose | Design Decision |
|---------|---------|-----------------|
| User messages | Show user input | Orange/red background, right-aligned intent |
| AI responses | Show agent output | Dark background, markdown support |
| Confidence badge | Trust indicator | 🟢🟡🔴 color-coded percentages |
| Feedback buttons | Satisfaction tracking | 👍👎 below each response |

### Sidebar Controls
| Element | Purpose | Design Decision |
|---------|---------|-----------------|
| Debug Mode | Developer visibility | Toggle shows routing path |
| Test Scenarios | Easy testing | Categorized dropdowns |
| Live Metrics | System health | Real-time counters |
| Pending Approvals | Human-in-the-loop | Alert badges for action |

### Tab Navigation
| Tab | Content | Purpose |
|-----|---------|---------|
| 💬 Chat | Main conversation | Primary interaction |
| 📋 Audit Log | Action history | Transparency & compliance |
| ℹ️ About | Architecture diagram | Education & context |

---

## User Flows

### Flow 1: Knowledge Query
```
User asks question
    ↓
Intake Agent classifies → "KnowledgeAgent"
    ↓
Knowledge Agent searches inline KB
    ↓
Response with confidence score
    ↓
User provides feedback (👍/👎)
```

### Flow 2: Workflow Automation
```
User requests action (e.g., "Reset my MFA")
    ↓
Intake Agent classifies → "WorkflowAgent"
    ↓
Workflow Agent selects tool
    ↓
[If sensitive] → Approval queue in sidebar
[If safe] → Execute immediately
    ↓
Show result with tool name
```

### Flow 3: Escalation with Jira
```
User is frustrated/VIP/complex issue
    ↓
Intake Agent → "EscalationAgent"
    ↓
Escalation Agent creates Jira ticket
    ↓
Slack notification simulation shown
    ↓
Ticket link displayed to user
```

---

## Accessibility Considerations

| Feature | Implementation |
|---------|----------------|
| Color contrast | WCAG AA compliant dark theme |
| Keyboard navigation | Tab through interactive elements |
| Screen reader | Semantic HTML, ARIA labels |
| Text size | Scalable with browser zoom |

---

## Responsive Design

| Viewport | Layout |
|----------|--------|
| Desktop (>1200px) | Full sidebar + main area |
| Tablet (768-1200px) | Collapsible sidebar |
| Mobile (<768px) | Hidden sidebar, hamburger menu |

---

## Design Iterations

### v1.0 - Basic Chat
- Simple input/output
- No debug information

### v2.0 - Added Transparency
- Debug mode toggle
- Routing path display
- Confidence scores

### v3.0 - Enterprise Features (Current)
- User role switching
- Audit log tab
- Jira integration display
- Pending approvals sidebar
- Live metrics dashboard

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Streamlit | Rapid UI development |
| Streamlit Components | Chat interface |
| CSS Custom | Dark theme styling |
| Markdown | Rich text rendering |

---

*Last Updated: 2025-12-06*
