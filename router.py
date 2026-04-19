def route_prompt(prompt):
    prompt_lower = prompt.lower()

    # Very basic rule-based routing (temporary)
    if "code" in prompt_lower or "python" in prompt_lower:
        return {
            "model": "gemini-1.5-flash",
            "category": "CODE",
            "complexity": "Easy"
        }

    elif "image" in prompt_lower:
        return {
            "model": "gemini-1.5-flash",
            "category": "IMAGE",
            "complexity": "Medium"
        }

    else:
        return {
            "model": "gemini-1.5-flash",
            "category": "GENERAL_CHAT",
            "complexity": "Easy"
        }