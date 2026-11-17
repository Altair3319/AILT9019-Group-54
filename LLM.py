import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("HKU_API_KEY"),
    base_url=os.getenv("HKU_BASE_URL", "https://api.deepseek.com"),
)

def answer_from_clauses(question, clauses):
    passages="\n\n".join(f"[{c['id']}] {c['text']}" for c in clauses)
    reply=client.chat.completions.create(
        model="deepseek-v4-flash",
        temperature=0.1,
        messages=[
            {"role": "system",
             "content": "Answer only from the clauses. Cite [Lx]. If not covered, say so."},
            {"role": "user", "content": f"Clauses:\n{passages}\n\nQuestion: {question}"},
        ],
    )
    return reply.choices[0].message.content
