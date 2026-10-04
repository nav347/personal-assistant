import api_clients

def run_startup_checks():
    print("=============================================================")
    print("🔍 PERFORMING CORE GATEWAY STATUS CHECKS...                  ")
    print("=============================================================")
    
    test_prompt = [{"role": "user", "content": "hi"}]
    
    _, gemini_log = api_clients.call_gemini(test_prompt)
    gemini_log_str = str(gemini_log)
    gemini_status = "✔ ONLINE" if "Gemini" in gemini_log_str else f"❌ OFFLINE ({gemini_log_str})"
    print(f"📡 Tier 1 Gateway (Google Gemini): {gemini_status}")
    
    _, groq_log = api_clients.call_groq(test_prompt)
    groq_log_str = str(groq_log)
    groq_status = "✔ ONLINE" if groq_log and "Groq" in groq_log_str else f"❌ OFFLINE ({groq_log_str})"
    print(f"📡 Tier 2 Gateway (Groq Cluster): {groq_status}")
    print("=============================================================\n")
    
    return ("Gemini" in gemini_log_str), (groq_log is not None and "Groq" in groq_log_str)
