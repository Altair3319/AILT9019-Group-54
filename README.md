# AILT9019-Group-54 #
# HKU Library Regulations Assistant #

This assistant is a small tool that answers students' questions about the HKU Library Regulations using the official document, "Regulation.docx". It answers enquiries and shows the citation alongside the answer.

WHAT IT DOES NOT DO:
It cannot check real-time availability, make bookings, handle personal data, or make subjective judgements.

---WEBSITE USAGE---
On the website, enter your question on the left side of the screen; the output appears on the right.

---MODEL TESTING---
HOW TO INSTALL:
pip3 install -r requirements.txt

HOW TO SEARCH DATA:
python3 parse_regulations.py

HOW TO RUN (TESTING):
python3 evaluate.py     runs the 10 test questions, evaluates, and prints a score
python3 app.py          opens the web chat UI
python3 assistant.py    terminal chat

ADDITIONAL INFORMATION:
The source is extracted from official HKU Library Regulations. Clause IDs are assigned by paragraph order inside each regulation. The original list letters are stored in Word format and not as readable text.

INPUTTING INSTRUCTIONS:
Keyword search can miss heavily paraphrased questions. English input only.
