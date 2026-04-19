from db import get_connection

def log_to_db(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO logs (
            prompt, response, model_used,
            tokens_input, tokens_output, total_tokens,
            cost, latency
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["prompt"],
        data["response"],
        data["model"],
        data["input_tokens"],
        data["output_tokens"],
        data["total_tokens"],
        data["cost"],
        data["latency"]
    ))

    conn.commit()
    cur.close()
    conn.close()