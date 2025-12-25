# web/summarize.py

def summarize_web_results(query: str, results: list, llm):
    if not results:
        return "I couldn’t find reliable information on that right now."

    context = "\n\n".join(
        f"Title: {r['title']}\nInfo: {r['snippet']}"
        for r in results
    )

    prompt = f"""
You are FRIDAY, a professional AI assistant.

User question:
{query}

Web information:
{context}

Rules:
- Answer clearly and factually
- If values vary, give an approximate range
- Do NOT hallucinate
- Do NOT mention sources unless asked

Final Answer:
"""

    return llm.generate(prompt)
