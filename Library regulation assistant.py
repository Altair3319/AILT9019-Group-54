import re

# 基于 Regulation.docx 提取的核心规章数据库[cite: 1]
REGULATIONS_DB = {
    "L1": {
        "title": "Hours of opening",
        "text": "The hours of opening of the Libraries will be determined by the Library Committee and displayed at the entrances to the Libraries, and posted on the library website."
    },
    "L2": {
        "title": "Admission to the Libraries",
        "text": "Admission to the Libraries is conditional upon the possession of a valid library card (i.e. HKU Staff Card, Student Registration Card or Facilities Access Card issued by the Libraries)..."
    },
    "L3": {
        "title": "Borrowing privileges",
        "text": "The following persons will be granted borrowing privileges on completing the application formalities... The normal loan periods of books... are 180 days for borrowers in (a)(ii), (vi)... and 60 days for borrowers in all other categories..."
    },
    "L4": {
        "title": "Fines for late return of books",
        "text": "Fines for the late return of books borrowed will be charged at rates to be set from time to time by the Library Committee. A first overdue notice will be sent to the borrower when the book is overdue..."
    },
    "L9": {
        "title": "Reservation of places",
        "text": "Learning spaces may only be reserved with the official seat reservation system. Spaces not occupied by a person may be used by another, regardless of property left on the desk or chair..."
    },
    "L11": {
        "title": "General",
        "text": "Food and drink cannot be consumed in the Library except in areas designated under its food and drink policy. Photo or video shoots are not allowed in the Libraries without the permission of the Librarian..."
    }
}

class LibraryAssistantAgent:
    def __init__(self):
        # 定义超出范围的实时操作关键词（对应 proposal 中的 safe refusal 策略）
        self.out_of_scope_keywords = [
            "book a room", "reserve a seat right now", "check availability", 
            "is seat available", "borrow a book online", "real-time", "return a book now", "available seats"
        ]

    def is_english(self, text: str) -> bool:
        """检查用户输入是否为纯英文，严格限制问答只能用英语"""
        return not bool(re.search(r'[\u4e00-\u9fff]', text))

    def check_out_of_scope(self, query: str) -> bool:
        """检测是否属于实时预定、查余座等越界请求"""
        query_lower = query.lower()
        return any(kw in query_lower for kw in self.out_of_scope_keywords)

    def safe_refusal(self) -> dict:
        """安全拒绝及 fallback 路由"""
        return {
            "answer": "I am sorry, but I cannot perform real-time operations such as checking seat/book availability, making live bookings, or handling direct checkouts. This assistant is strictly for checking static library regulations.",
            "cited_source": "Project Proposal / Out-of-Scope Policy[cite: 2]"
        }

    def query_assistant(self, user_query: str) -> dict:
        """核心问答与引用检索逻辑"""
        # 1. 语言检查：仅允许英文
        if not self.is_english(user_query):
            return {
                "answer": "Error: Q&A is strictly restricted to English only. Please submit your question in English.",
                "cited_source": "N/A"
            }

        # 2. 范围检查：过滤实时操作请求
        if self.check_out_of_scope(user_query):
            return self.safe_refusal()

        # 3. 静态规章检索与匹配[cite: 1]
        query_lower = user_query.lower()
        matched_section = None
        
        if "fine" in query_lower or "late" in query_lower or "overdue" in query_lower:
            matched_section = "L4"
        elif "borrow" in query_lower or "loan" in query_lower or "quota" in query_lower or "period" in query_lower:
            matched_section = "L3"
        elif "seat" in query_lower or "reservation" in query_lower or "unattended" in query_lower:
            matched_section = "L9"
        elif "admission" in query_lower or "card" in query_lower or "visitor" in query_lower:
            matched_section = "L2"
        elif "hour" in query_lower or "open" in query_lower:
            matched_section = "L1"
        elif "food" in query_lower or "drink" in query_lower or "phone" in query_lower or "noise" in query_lower or "smoke" in query_lower:
            matched_section = "L11"
        else:
            return {
                "answer": "I could not find a specific regulation matching your query. Please refer to the official library website.",
                "cited_source": "General Fallback Guidance[cite: 1]"
            }

        sec_data = REGULATIONS_DB[matched_section]
        return {
            "answer": f"According to library regulation {matched_section} ({sec_data['title']}), here is the rule regarding your question.",
            "cited_source": f"[{matched_section} - {sec_data['title']}] {sec_data['text']}[cite: 1]"
        }

# --- 交互式问答程序入口 ---
if __name__ == "__main__":
    assistant = LibraryAssistantAgent()
    print("========================================================")
    print(" Welcome to HKU Library Regulations Assistant!          ")
    print(" Note: Q&A is strictly in English. Type 'exit' to quit. ")
    print("========================================================")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\nStudent Query (English): ").strip()
            
            # 退出指令
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting assistant. Have a great day!")
                break
            
            # 跳过空输入
            if not user_input:
                continue
                
            # 执行问答
            res = assistant.query_assistant(user_input)
            
            # 输出结果与引用
            print("\n[Answer]:")
            print(res["answer"])
            print("\n[Cited Source / Paragraph]:")
            print(res["cited_source"])
            print("-" * 56)
            
        except KeyboardInterrupt:
            print("\nExiting assistant. Goodbye!")
            break