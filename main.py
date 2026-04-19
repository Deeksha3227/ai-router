from model_executor import call_model
from cost_tracker import calculate_cost
from logger import log_to_db
from cache import get_cached_response, store_in_cache
from router import route_prompt   # ✅ import at top

def main():
    prompt = input("Enter your prompt: ")

    # 🔍 STEP 1 — Check cache
    cached = get_cached_response(prompt)

    if cached:
        print("\n⚡ CACHE HIT")
        print("\n===== OUTPUT =====")
        print(cached)
        return

    print("\n🚀 CACHE MISS → calling model...")

    # 🧠 STEP 2 — Router decision (FIXED INDENTATION)
    route = route_prompt(prompt)

    selected_model = route["model"]
    category = route["category"]
    complexity = route["complexity"]

    # 🧾 Print routing decision (important for demo)
    print("\n🧠 ROUTER DECISION")
    print(f"Category: {category}")
    print(f"Complexity: {complexity}")
    print(f"Selected Model: {selected_model}")

    # 🤖 STEP 3 — Call model
    result = call_model(selected_model, prompt)

    # 📊 STEP 4 — Token percentage
    if result["total_tokens"] > 0:
        input_pct = (result["input_tokens"] / result["total_tokens"]) * 100
        output_pct = (result["output_tokens"] / result["total_tokens"]) * 100
    else:
        input_pct = output_pct = 0

    # 💰 STEP 5 — Cost calculation
    cost = calculate_cost(
        selected_model,
        result["input_tokens"],
        result["output_tokens"]
    )

    # 🧾 STEP 6 — Prepare log data (ADD category + complexity)
    log_data = {
        "prompt": prompt,
        "response": result["response"],
        "model": selected_model,
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "total_tokens": result["total_tokens"],
        "cost": cost,
        "latency": result["latency"],
        "category": category,
        "complexity": complexity
    }

    # ✅ Store in DB logs
    if result["total_tokens"] > 0:
        log_to_db(log_data)

    # ✅ Store in cache
    store_in_cache(prompt, result["response"])

    # 🖥️ OUTPUT
    print("\n===== OUTPUT =====")
    print(result["response"])

    print("\n===== STATS =====")
    print(f"Model: {selected_model}")
    print(f"Input Tokens: {result['input_tokens']} ({input_pct:.2f}%)")
    print(f"Output Tokens: {result['output_tokens']} ({output_pct:.2f}%)")
    print(f"Total Tokens: {result['total_tokens']}")
    print(f"Cost: ${cost:.6f}")
    print(f"Latency: {result['latency']:.2f}s")

if __name__ == "__main__":
    main()