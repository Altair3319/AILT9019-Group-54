import json, re, os
from docx import Document

doc=Document("Regulation.docx")
paragraphs=[p.text.strip() for p in doc.paragraphs if p.text.strip()]

clauses=[]
current_reg=None
position=0
text_buffer=[]

def save_clause():
    global text_buffer, position
    if current_reg and text_buffer:
        label=chr(ord('a')+position)
        clauses.append({"id": f"{current_reg}({label})", "text": " ".join(text_buffer).strip()})
    text_buffer=[]

for line in paragraphs:
    heading=re.match(r"^(L\d+)\s+(.+)$", line)
    if heading:
        save_clause()
        current_reg=heading.group(1)
        position=-2
        continue
    if current_reg:
        position+=1
        save_clause()
        text_buffer=[line]
save_clause()

os.makedirs("data", exist_ok=True)
json.dump(clauses, open("data/regulations.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"{len(clauses)} clauses written")
for item in clauses[:5]:
    print(item["id"], "|", item["text"][:60])
