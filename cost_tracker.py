MODEL_COST = {
    "gpt-4o-mini": {
        "input": 0.00015,
        "output": 0.0006
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