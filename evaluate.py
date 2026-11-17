import json
from assistant import ask

with open("tests/questions.json", encoding="utf-8") as f:
    tests=json.load(f)

passed=0
for case in tests:
    result=ask(case["q"])
    outcome="refuse" if result["citation"] in ("Out of scope", "N/A") else "answer"
    ok=outcome==case["expect"]
    passed+=ok
    print(("PASS" if ok else "FAIL"), "|", case["q"], "->", result["citation"])

print(f"\nScore: {passed}/{len(tests)}")
