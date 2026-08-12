import os
import secrets
import threading
import requests
import asyncio
from flask import Flask, render_template_string, request, jsonify
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient

# MongoDB Setup
MONGO_URI = "mongodb+srv://teamthumbupsgaming_db_user:6I3dbGX4kNjcEXBP@vinay.pprhqmn.mongodb.net/?appName=Vinay"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telugumovies40_bot"]
users_col = db["users"]

app = Flask(__name__)
token_db = {}
async_loop = asyncio.new_event_loop()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, args=(async_loop,), daemon=True).start()

DENIED_HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>TELUGU MOVIES 40 - Access Denied</title><style>body{background:#0f0f1a;color:#ff4d4d;font-family:sans-serif;text-align:center;padding-top:50px;}.card{background:#1a1a2e;padding:25px;border-radius:15px;border:2px solid #ff4d4d;display:inline-block;width:85%;max-width:400px;}.btn{background:#ff4d4d;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;display:inline-block;margin-top:20px;font-weight:bold;}</style></head><body><div class="card"><h2>🎬 TELUGU MOVIES 40 🎬</h2><h1>🚫 ACCESS DENIED</h1><p>{{ reason }}</p><a href="https://t.me/Telugumovies40" class="btn">JOIN TELUGU MOVIES 40</a></div></body></html>"""

GRANTED_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TELUGU MOVIES 40 - Verification</title>
    <style>
        body { background: #0f0f1a; color: #ffffff; font-family: sans-serif; text-align: center; padding-top: 40px; }
        .card { background: #1a1a2e; padding: 30px; border-radius: 18px; border: 1px solid #2cb67d; display: inline-block; width: 85%; max-width: 420px; }
        .timer-circle { width: 90px; height: 90px; border-radius: 50%; background: #242442; border: 4px solid #2cb67d; display: flex; align-items: center; justify-content: center; margin: 20px auto; font-size: 32px; font-weight: bold; color: #2cb67d; }
        .btn { background: #2cb67d; color: #0f0f1a; padding: 14px 28px; border-radius: 10px; text-decoration: none; display: none; margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="color: #2cb67d;">🎬 TELUGU MOVIES 40 🎬</h2>
        <p>Verification Successful</p>
        <div class="timer-circle" id="timer">10</div>
        <p id="status">Please wait <span id="sec">10</span> seconds...</p>
        <a href="{{ target_url }}" class="btn" id="go-btn">🚀 GET FILE LINK NOW</a>
    </div>
    <script>
        let t = 10;
        let inv = setInterval(() => {
            t--;
            document.getElementById("timer").innerText = t;
            document.getElementById("sec").innerText = t;
            if (t <= 0) {
                clearInterval(inv);
                document.getElementById("timer").style.display = "none";
                document.getElementById("status").innerText = "Link Ready!";
                document.getElementById("go-btn").style.display = "inline-block";
            }
        }, 1000);
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return "TeluguMovies40 Multi-User Protection Server Alive!"

@app.route('/create_token', methods=['POST'])
def create_token():
    data = request.json or {}
    token = secrets.token_urlsafe(16)
    token_db[token] = {"target_url": data.get("target_url")}
    return jsonify({"status": "success", "token": token})

@app.route('/verify/<token>')
def verify(token):
    data = token_db.get(token)
    user_agent = request.headers.get('User-Agent', '').lower()
    user_ip = request.remote_addr
    
    if not data:
        return render_template_string(DENIED_HTML, reason="Invalid or Expired Link!"), 403
    
    bypasser_keywords = ['python', 'curl', 'wget', 'aiohttp', 'bot', 'scraper', 'spider']
    if any(k in user_agent for k in bypasser_keywords):
        alert_text = f"<b>⚠️ #BypassAttackBlocked ⚠️</b>\n\n<b>IP:</b> <code>{user_ip}</code>\n<b>User Agent:</b> <code>{user_agent}</code>"
        asyncio.run_coroutine_threadsafe(bot.send_message(LOG_CHANNEL, alert_text), async_loop)
        return render_template_string(DENIED_HTML, reason="Automated Bypasser Tool Detected! Access Blocked."), 403

    return render_template_string(GRANTED_HTML, target_url=data['target_url'])

API_ID = 23209524
API_HASH = "3042159268b8b90557a5e2b8ab346843"
BOT_TOKEN = "8770337415:AAEVxe7UfMQqInJJ1RJraefastcLNPILjRM"
LOG_CHANNEL = -1004427714969
DEFAULT_GPLINKS_KEY = "cd02492acca21d2f5aff76690e7a901d401c2799"

WEBAPP_URL = os.getenv("RENDER_EXTERNAL_URL", os.getenv("TUNNEL_URL", "http://127.0.0.1:8080"))

bot = Client("svbrand_bypass_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_main_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎛️ Dashboard", callback_data="btn_dash"), InlineKeyboardButton("🌐 My API Key", callback_data="btn_sites")],
        [InlineKeyboardButton("📊 My Stats", callback_data="btn_stats"), InlineKeyboardButton("🆘 Help", callback_data="btn_help")]
    ])

@bot.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    users_col.update_one({"_id": user_id}, {"$set": {"name": message.from_user.first_name}}, upsert=True)
    
    caption = f"<b>🎬 WELCOME TO TELUGU MOVIES 40 MULTI-ADMIN PROTECTION BOT</b>\n\nEvaraina e bot use cheskovachu mawa!\n\n🔹 Send any Telegram Storage link to convert into protected link.\n🔹 Use `/set_api YOUR_GPLINKS_KEY` to set your custom shortener API key."
    try:
        await message.reply_photo(photo="https://i.ibb.co/6P0zJgM/128913.jpg", caption=caption, reply_markup=get_main_markup())
    except Exception:
        await message.reply(caption, reply_markup=get_main_markup())

@bot.on_message(filters.command("set_api"))
async def set_api_key(client, message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply("<b>⚠️ Format Error!</b>\n\nUsage: `/set_api YOUR_GPLINKS_API_KEY`")
        return
    
    new_api = args[1].strip()
    users_col.update_one({"_id": user_id}, {"$set": {"api_key": new_api}}, upsert=True)
    await message.reply(f"<b>✅ API Key Successfully Saved!</b>\n\nIppudu meeru pame links mee personal API key (<code>{new_api[:6]}...</code>) thone shorten avthayi.")

@bot.on_message(filters.text & filters.private)
async def protect_link(client, message):
    if message.text.startswith("/"):
        return
        
    target_link = message.text.strip()
    user = message.from_user
    
    if "t.me/" not in target_link:
        await message.reply("Valid Telegram storage link pampu mawa!")
        return

    # Check User Custom API Key
    user_data = users_col.find_one({"_id": user.id}) or {}
    user_api = user_data.get("api_key", DEFAULT_GPLINKS_KEY)

    try:
        req = requests.post(f"{WEBAPP_URL}/create_token", json={"target_url": target_link}, timeout=10)
        res = req.json()
        token = res.get("token")
        verify_url = f"{WEBAPP_URL}/verify/{token}"
        
        # Call GPLinks API using user's custom key
        short_res = requests.get(f"https://gplinks.in/api?api={user_api}&url={verify_url}").json()
        
        if short_res.get("status") == "success":
            short_url = short_res.get("shortenedUrl")
            reply_text = f"<b>🎬 TELUGU MOVIES 40 PROTECTED LINK 🎬</b>\n\n<b>Original:</b> <code>{target_link}</code>\n<b>Protected Link:</b> {short_url}\n\n<i>Note: Direct bypass tools vaadithe access block avthundhi!</i>"
            await message.reply(reply_text)
            
            # Send Log to Channel
            log_text = f"<b>#NewLinkProtected</b>\n<b>User:</b> {user.mention} (<code>{user.id}</code>)\n<b>Original:</b> {target_link}\n<b>Protected:</b> {short_url}"
            try:
                await client.send_message(LOG_CHANNEL, log_text)
            except Exception as e:
                print("Log Error:", e)
        else:
            await message.reply("⚠️ Shortener API Error! Check if your API key is valid.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data == "btn_sites":
        user_data = users_col.find_one({"_id": user_id}) or {}
        curr_key = user_data.get("api_key", "Default System Key")
        await query.message.reply(f"<b>🌐 Your Current Shortener Settings:</b>\n\n<b>API Key:</b> <code>{curr_key}</code>\n\nTo update your key, send:\n`/set_api YOUR_GPLINKS_API_KEY`")
    elif data == "btn_stats":
        await query.answer("Profile Stats Active!", show_alert=True)
    elif data == "btn_help":
        await query.message.reply("<b>🆘 Help Guide:</b>\n\n1. Send any Telegram storage link to get protected link.\n2. Add your own GPLinks API key using `/set_api KEY` command.")

if __name__ == "__main__":
    bot.run()
