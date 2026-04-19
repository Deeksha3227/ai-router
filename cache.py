from db import get_connection

def get_cached_response(prompt):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT response FROM cache WHERE prompt = %s", (prompt,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return result[0]
    return None


def store_in_cache(prompt, response):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO cache (prompt, response) VALUES (%s, %s)",
            (prompt, response)
        )
        conn.commit()
    except:
        pass  # ignore duplicate

    cur.close()
    conn.close()