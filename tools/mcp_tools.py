import random

def check_vpn_status(user_id: str) -> str:
    """
    Simulates checking the VPN status for a user.
    """
    print(f"[MCP Tool] check_vpn_status called for user: {user_id}")
    if user_id == "user_locked":
        return "Account Locked"
    return "Connected"

def unlock_account(user_id: str) -> str:
    """
    Simulates unlocking a user account.
    """
    print(f"[MCP Tool] unlock_account called for user: {user_id}")
    return "Account Unlocked"

def fetch_recent_logs(user_id: str) -> str:
    """
    Simulates fetching recent system logs for a user/device.
    """
    print(f"[MCP Tool] fetch_recent_logs called for user: {user_id}")
    
    # Creative Log Scenarios based on User ID
    logs_db = {
        "user_hacker": """
        [2025-12-02 14:00:01] WARN: Multiple failed login attempts (IP: 192.168.1.666)
        [2025-12-02 14:00:05] WARN: Sudo access denied for user 'guest'
        [2025-12-02 14:00:10] CRITICAL: Port scanning detected on internal firewall.
        [2025-12-02 14:00:15] ALERT: Unauthorized data exfiltration attempt blocked.
        """,
        "user_dev": """
        [2025-12-02 10:00:01] INFO: Application started
        [2025-12-02 10:05:23] WARN: High memory usage detected (85%)
        [2025-12-02 10:06:00] ERROR: ConnectionRefusedError: Unable to connect to database at db.prod.internal:5432
        [2025-12-02 10:06:01] CRITICAL: Transaction rollback failed. Data inconsistency possible.
        """,
        "user_quantum": """
        [2025-12-02 09:00:00] INFO: Q-1000 System Online. Coherence: 99.9%
        [2025-12-02 09:15:00] WARN: Temporal drift detected in Sector 7.
        [2025-12-02 09:15:05] ERROR: Qubit decoherence event. Superposition collapse imminent.
        [2025-12-02 09:15:10] CRITICAL: Reality integrity compromised. Please reboot the universe.
        """,
        "user_ceo": """
        [2025-12-02 08:00:00] INFO: VIP Login. Welcome, CEO.
        [2025-12-02 08:05:00] ERROR: Email sync failed. Latency > 5ms.
        [2025-12-02 08:05:01] WARN: Coffee machine API not responding.
        """,
        "user_ransomware": """
        [2025-12-02 03:00:00] INFO: Backup service started.
        [2025-12-02 03:15:00] WARN: High disk write activity detected on /shared/finance.
        [2025-12-02 03:15:05] ALERT: File extension .crypt detected.
        [2025-12-02 03:15:10] CRITICAL: Ransomware signature matched (WannaCry_2025). Isolating host.
        [2025-12-02 03:15:15] ERROR: Encryption process active. 5000 files affected.
        """,
        "user_network": """
        [2025-12-02 11:00:00] INFO: Link status up. Speed: 1Gbps.
        [2025-12-02 11:05:00] WARN: High latency to gateway (500ms).
        [2025-12-02 11:05:30] ERROR: Packet loss > 15%. Voice call quality degraded.
        [2025-12-02 11:06:00] CRITICAL: BGP session flap detected. Rerouting traffic.
        """,
        "user_ssl": """
        [2025-12-02 09:00:00] INFO: Web server started (Apache/2.4).
        [2025-12-02 09:00:01] WARN: SSL Certificate for secure.company.com expires in 0 days.
        [2025-12-02 09:00:05] ERROR: Handshake failed: Certificate Expired.
        [2025-12-02 09:00:10] CRITICAL: Service outage. Clients cannot connect securely.
        """,
        "user_phishing": """
        [2025-12-02 10:00] INFO: Email received from 'ceo@company-update.com' (External).
        [2025-12-02 10:01] WARN: User clicked link 'http://login-company.com/reset'.
        [2025-12-02 10:02] ALERT: Credential harvest page detected.
        """,
        "user_compromised": """
        [2025-12-02 02:00] INFO: Login success for user123.
        [2025-12-02 02:00] WARN: Login location: Pyongyang, North Korea (GeoIP).
        [2025-12-02 02:01] ALERT: Impossible travel detected (Last login: NYC, 1 hour ago).
        """,
        "user_exfil": """
        [2025-12-02 15:00] INFO: User connected to 'Dropbox'.
        [2025-12-02 15:05] WARN: Upload started: 'customer_db.csv' (2.5 GB).
        [2025-12-02 15:10] CRITICAL: DLP Policy Violation. Sensitive data pattern matched.
        """
    }
    
    return logs_db.get(user_id, """
    [2025-12-02 12:00:00] INFO: System running normally.
    [2025-12-02 12:05:00] INFO: User logged in.
    [2025-12-02 12:10:00] INFO: File saved successfully.
    """)

def create_ticket(title: str, description: str, priority: str = "Medium") -> str:
    """
    Simulates creating a Jira/ServiceNow ticket via MCP.
    """
    import random
    ticket_id = f"INC-{random.randint(1000, 9999)}"
    print(f"[MCP Tool] create_ticket called: {ticket_id} | Priority: {priority}")
    return ticket_id

def check_license_availability(software_name: str) -> bool:
    """
    Simulates checking if a software license is available in the pool.
    """
    print(f"[MCP Tool] check_license_availability called for: {software_name}")
    # Mock logic: "Pro" versions are scarce
    if "pro" in software_name.lower():
        return False
    return True

def provision_license(user_id: str, software_name: str) -> str:
    """
    Simulates provisioning a software license to a user.
    """
    print(f"[MCP Tool] provision_license called for user: {user_id} | Software: {software_name}")
    import random
    license_key = f"{software_name[:3].upper()}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    return license_key

# --- Identity Tools ---
def reset_mfa(user_id: str) -> str:
    print(f"[MCP Tool] reset_mfa called for user: {user_id}")
    return "MFA Reset Link sent to backup email."

def onboard_user(name: str, department: str) -> str:
    print(f"[MCP Tool] onboard_user called for: {name} ({department})")
    return f"User {name} created. Email: {name.lower().replace(' ', '.')}@company.com"

def offboard_user(user_id: str) -> str:
    print(f"[MCP Tool] offboard_user called for user: {user_id}")
    return f"User {user_id} disabled. Access revoked."

def grant_temp_admin(user_id: str, duration_hours: int) -> str:
    print(f"[MCP Tool] grant_temp_admin called for user: {user_id} | Duration: {duration_hours}h")
    return f"Sudo access granted to {user_id} for {duration_hours} hours."

# --- Hardware Tools ---
def check_hardware_eligibility(user_id: str) -> str:
    print(f"[MCP Tool] check_hardware_eligibility called for user: {user_id}")
    return "Eligible for upgrade (Last refresh: 4 years ago)"

def order_peripheral(user_id: str, item: str) -> str:
    print(f"[MCP Tool] order_peripheral called for user: {user_id} | Item: {item}")
    return f"Order #ORD-{random.randint(10000,99999)} placed for {item}."

# --- Network Tools ---
def reboot_server(server_id: str) -> str:
    print(f"[MCP Tool] reboot_server called for: {server_id}")
    if "prod" in server_id.lower():
        return "DENIED: Production server reboot requires approval."
    return f"Server {server_id} rebooting..."

def submit_facility_request(location: str, issue: str) -> str:
    print(f"[MCP Tool] submit_facility_request called: {location} - {issue}")
    return f"Facility Ticket #FAC-{random.randint(100,999)} created."

def get_user_context(user_id: str) -> dict:
    """
    Simulates fetching user profile/context from an HR or IT database.
    """
    context = {
        "role": "Employee",
        "location": "New York (HQ)",
        "department": "Engineering",
        "vip": False
    }
    
    if "vip" in user_id or "ceo" in user_id:
        context["role"] = "Executive"
        context["vip"] = True
    elif "dev" in user_id:
        context["role"] = "Developer"
    elif "sales" in user_id:
        context["location"] = "London (Remote)"
        context["department"] = "Sales"
        
    print(f"[Context] Fetched profile for {user_id}: {context}")
    return context
