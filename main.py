import os
import asyncio
from fastapi import FastAPI, Request
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
import requests
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def test_mongo_connection(url):
    try:
        client = MongoClient(url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        client.close()
        return True, None
    except (ConnectionFailure, ConfigurationError) as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def send_message_sync(chat_id, text):
    if not BOT_TOKEN:
        return
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        
        if text.startswith("/start"):
            welcome_text = (
                "🙏 **Welcome to 𝒮𝒶𝓃𝒶𝓉𝒶𝓃𝒾 𝑀𝑜𝓃𝑔𝑜𝐷𝐵 𝐵𝑜𝓉!**\n\n"
                "Send me any MongoDB connection URL (`mongodb://...` or `mongodb+srv://...`), "
                "and I will check if it is active and working correctly."
            )
            await asyncio.to_thread(send_message_sync, chat_id, welcome_text)
        
        elif text.startswith("mongodb://") or text.startswith("mongodb+srv://"):
            await asyncio.to_thread(send_message_sync, chat_id, "🔄 Testing MongoDB connection... Please wait.")
            
            # Run blocking mongodb ping in a separate thread so server doesn't shutdown/freeze
            success, error_msg = await asyncio.to_thread(test_mongo_connection, text)
            
            if success:
                reply = "✅ **Connection Successful!**\nThe MongoDB URL is active, valid, and responding."
            else:
                reply = f"❌ **Connection Failed!**\n\n`{error_msg}`"
                
            await asyncio.to_thread(send_message_sync, chat_id, reply)
        else:
            await asyncio.to_thread(send_message_sync, chat_id, "ℹ️ Please send a valid MongoDB connection string starting with `mongodb://` or `mongodb+srv://`.")
            
    return {"status": "ok"}

@app.get("/")
@app.head("/")
def home():
    return {"status": "𝒮𝒶𝓃𝒶𝓉𝒶𝓃𝒾 𝑀𝑜𝓃𝑔𝑜𝐷𝐵 𝐵𝑜𝓉 is running successfully! 🙏"}
