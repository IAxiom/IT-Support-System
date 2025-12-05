from main import app
import time

# Test Case 14: Dynamic Workflow (LLM Tool Selection)
print("\n--- Test Case 14: Dynamic Workflow (LLM Tool Selection) ---")
initial_state = {"messages": [{"role": "user", "content": "I need a new mouse for my desk."}], "user_id": "user_dev"}
result = app.invoke(initial_state)
print("Final Result:", result['messages'][-1]['content'])
time.sleep(2)

# Test Case 15: Creative Intake (VIP Auto-Escalation)
print("\n--- Test Case 15: Creative Intake (VIP Auto-Escalation) ---")
initial_state = {"messages": [{"role": "user", "content": "My email is down and it is critical!"}], "user_id": "user_ceo"}
result = app.invoke(initial_state)
print("Final Result:", result['messages'][-1]['content'])
time.sleep(2)

# Test Case 16: Empathy Engine
print("\n--- Test Case 16: Empathy Engine ---")
initial_state = {"messages": [{"role": "user", "content": "I hate this system! It never works!"}], "user_id": "user_angry"}
result = app.invoke(initial_state)
print("Final Result:", result['messages'][-1]['content'])
