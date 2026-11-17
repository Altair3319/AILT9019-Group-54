import json
from rank_bm25 import BM25Okapi

clauses=json.load(open("data/regulations.json", encoding="utf-8"))
search_index=[(c["id"]+" "+c["text"]).lower().split() for c in clauses]
ranking=BM25Okapi(search_index)

synonyms={
    "take out": "borrow", "check out": "borrow", "volumes": "books", "penalty": "fine", "fee": "fine", "late return": "overdue",
    "opening times": "hours", "eating": "food", "drinking": "drink", "bag": "belongings", "desk": "learning spaces",
}

def expand(question):
    q=question.lower()
    for k, v in synonyms.items():
        if k in q:
            q+=" " + v
    return q

def retrieve(question, k=3):
    scores=ranking.get_scores(question.lower().split())
    order=sorted(range(len(clauses)), key=lambda i: scores[i], reverse=True)
    return [clauses[i] for i in order[:k] if scores[i] > 0]

