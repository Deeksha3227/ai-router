def route_prompt(prompt):
    prompt_lower = prompt.lower()

    if "code" in prompt_lower or "python" in prompt_lower:
        return {
            "model": "llama3-70b-8192",
            "category": "CODE",
            "complexity": "Easy"
        }

    elif "explain" in prompt_lower or "analysis" in prompt_lower:
        return {
            "model": "gemini-1.5-flash",
            "category": "ANALYSIS",
            "complexity": "Medium"
        }

    else:
        return {
            "model": "gemini-1.5-flash",
            "category": "GENERAL_CHAT",
            "complexity": "Easy"
        }