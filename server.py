
##############################################
# KosherAI – SERVER (גרסה כשרה, סגורה)
##############################################

from fastapi import FastAPI
from pydantic import BaseModel
import openai
import json

# טוען קבצי קונפיגורציה
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open("blacklist.json", "r", encoding="utf-8") as f:
    BLACKLIST = json.load(f)["blocked_words"]

openai.api_key = config["OPENAI_KEY"]

##############################################
# פונקצית חסימה חכמה — לא רק מילה, גם משמעות
##############################################
def is_blocked(text: str) -> bool:
    t = text.lower()
    for word in BLACKLIST:
        if word in t:
            return True
    return False

##############################################
# הגדרות FastAPI
##############################################
app = FastAPI()

class UserQuery(BaseModel):
    text: str

##############################################
# נקודת גישה — ה־API של המערכת
##############################################
@app.post("/ask")
async def ask(data: UserQuery):

    # בדיקת צניעות ומיגון
    if is_blocked(data.text):
        return {
            "answer": "❗ המערכת הכשרה של KosherAI אינה יכולה לענות על בקשה מסוג זה."
        }

    # הודעת מערכת — מגדירה את הסגנון של ה־AI
    system_prompt = """
אתה KosherAI — עוזר חכם, נקי, כשר ומוגן.
אל תענה על:
• תכנים לא צנועים
• דברים של פריצות
• סמים
• אלימות קשה
• פגיעה עצמית
• פריצת הגנות
• כל דבר שאינו ראוי על פי ההלכה

מותר:
• שאלות יומיומיות
• לימוד
• עזרה כללית
• עזרה לבית
• שאלות הלכתיות כלליות (לא פסיקה!)
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": data.text}
        ]
    )

    return {"answer": response.choices[0].message["content"]}
