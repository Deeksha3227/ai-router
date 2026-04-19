MODEL_COST = {
    "gemini-1.5-flash": {
        "input": 0.00015,
        "output": 0.0006
    },
    "groq-llama3-8b": {
        "input": 0.00005,
        "output": 0.0001
    }
}

def calculate_cost(model, input_tokens, output_tokens):
    cost_info = MODEL_COST.get(model)

    if not cost_info:
        return 0

    return (
        (input_tokens / 1000) * cost_info["input"] +
        (output_tokens / 1000) * cost_info["output"]
    )