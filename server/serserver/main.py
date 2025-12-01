from fastapi import FastAPI
from pydantic import BaseModel
import json
import openai

app = FastAPI()

# Load config
with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

openai.api_key = CONFIG["OPENAI_API_KEY"]

# Load blacklist
with open("blacklist.json", "r", encoding="utf-8") as f:
    BLACKLIST = json.load(f)

class Query(BaseModel):
    text: str

def is_forbidden(text: str) -> bool:
    text_lower = text.lower()
    for bad in BLACKLIST:
        if bad in text_lower:
            return True
    return False

@app.post("/ask")
async def ask_ai(data: Query):
    if is_forbidden(data.text):
        return {"answer": "❗ המערכת הכשרה של KosherAI לא יכולה לענות על הבקשה הזו."}

    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "אתה עוזר כשר, צנוע, נקי, ומכובד. ענה בקצרה וברוגע."},
            {"role": "user", "content": data.text}
        ]
    )

    return {"answer": completion.choices[0].message["content"]}
