from utils.rag import add_documents

def main():
    print("Initializing Knowledge Base...")
    
    documents = [
        # --- 1. Identity & Access ---
        "MFA Reset: To reset your Multi-Factor Authentication, visit id.company.com/reset. You will need your backup codes. If lost, contact the Service Desk.",
        "New Hire Onboarding: Managers must submit the 'New Hire Form' in Workday 3 days prior to start date. IT will provision email, Slack, and laptop.",
        "Offboarding Policy: Access is revoked at 5:00 PM on the last day. Managers must collect badges and laptops. Data is retained for 30 days.",
        "Admin Access Policy: Temporary Admin Access (sudo) is granted for 1-hour windows. Request via the 'Elevate' tool. All commands are logged.",

        # --- 2. Hardware & Devices ---
        "Laptop Refresh Policy: Engineering gets MacBook Pro M4s every 3 years. Sales gets MacBook Airs every 3 years. Early refresh requires VP approval.",
        "Peripheral Catalog: Standard issue includes 1x 27-inch monitor, mouse, and keyboard. 4K monitors require 'Creative' job role.",
        "Mobile Device Management (MDM): To enroll your iPhone, install the 'Company Portal' app and sign in. This creates a work profile separate from personal data.",

        # --- 3. Network & Infrastructure ---
        "Wi-Fi Troubleshooting: Weak signal? Try forgetting the network and re-joining. 'CompanyGuest' is for visitors only. 'CompanyInternal' requires a certificate.",
        "Server Reboot Protocol: Production servers can only be rebooted during the maintenance window (Sunday 2am-4am). Dev servers can be rebooted anytime via the portal.",
        "DNS Issues: If internal sites are unreachable, try flushing your DNS cache (`ipconfig /flushdns` or `sudo killall -HUP mDNSResponder`).",

        # --- 4. Security ---
        "Phishing Analysis: Suspicious emails often have urgent language, mismatched URLs, or unexpected attachments. Forward to phishing@company.com.",
        "Suspicious Login: If you receive a login alert from an unknown location, change your password immediately and contact Security.",
        "Data Exfiltration: Uploading >1GB to personal cloud storage triggers an automatic block and HR review.",

        # --- 5. General Support ---
        "Meeting Room Support: For broken projectors or audio, use the room's iPad to report an issue or call x5555. Mention the Room Name.",
        "Expense Policy: Client dinners are capped at $75/person. Alcohol is reimbursable only with VP approval. Submit via Concur.",
        "Printer Configuration: Map printers using the 'PrintDeploy' agent in your system tray. The color printer on 3rd floor is named 'US-NYC-FL3-Color'.",
        "Guest Wi-Fi Password: The current password for 'CompanyGuest' is 'Innovation2025!'. It rotates every Monday.",
        "Holiday Calendar: The office is closed for New Year's, Memorial Day, July 4th, Labor Day, Thanksgiving (2 days), and Christmas.",
        "Benefits - Dental: We use Delta Dental PPO. Preventative care is covered 100%. Orthodontia has a lifetime max of $2000.",
        "Emergency Protocol: In case of fire, evacuate via the nearest stairwell. Do not use elevators. Rally point is the park across the street.",
        
        # --- Advanced/Futuristic (Creative) ---
        "Quantum Workstation Access: Access to Q-1000 workstations is restricted to Level 5 personnel. Do NOT operate the Q-1000 without wearing anti-static temporal shielding.",
        "Holographic Meeting Etiquette: When joining a Holo-Call, ensure your avatar is set to 'Professional'. Anime avatars are only permitted on Fridays.",
        "Time Loop Protocol: If you experience a localized time loop, contact Temporal Ops. Do not reply to the recurring emails."
    ]
    
    add_documents(documents)
    print(f"Added {len(documents)} documents to the knowledge base.")

if __name__ == "__main__":
    main()
