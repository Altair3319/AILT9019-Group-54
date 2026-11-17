import os, re
from retriever import retrieve

use_llm=os.getenv("USE_LLM")=="1"
blocked_phrases=["right now", "real-time", "available seat", "is seat", "book", "reserve", "check availability", "borrow a book online"]

def ask(question):
    if re.search(r"[\u4e00-\u9fff]", question):
        return {"answer": "Please ask in English.", "citation": "N/A"}
    if any(p in question.lower() for p in blocked_phrases):
        return {"answer": "I can't do real-time checks or bookings. Use the library website.", "citation": "Out of scope"}

    matches=retrieve(question)
    if not matches:
        return {"answer": "No matching regulation found. Check the library website.", "citation": "None"}

    source=f"Regulation.docx, {matches[0]['id']}"

    if use_llm:
        try:
            from llm import answer_from_clauses
            return {"answer": answer_from_clauses(question, matches), "citation": source}
        except Exception as err:
            return {"answer": matches[0]["text"], "citation": source+f" (LLM off: {err})"}

    return {"answer": matches[0]["text"], "citation": source}

if __name__=="__main__":
    while True:
        try:
            user_input=input("\nQuestion: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue
        result=ask(user_input)
        print("\n"+result["answer"]+"\n\nCitation: "+result["citation"])
