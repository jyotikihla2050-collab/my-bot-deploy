import os
import logging
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from telegram import Update

# તમારા બોટનો ટોકન અને તમારું Chat ID
TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
YOUR_CHAT_ID = 5306025504

# લોગિંગ ચાલુ કરો જેથી તમે એરર જોઈ શકો
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("નમસ્કાર! હું તમારી શું મદદ કરી શકું?")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    if update.message and update.message.text:
        # ફક્ત બીજાના મેસેજ તમને મોકલવા માટે
        if chat.id != YOUR_CHAT_ID:
            user_info = f"👤 નામ: {user.first_name}\n🆔 ID: {user.id}\n💬 ચેટ ID: {chat.id}\n📝 મેસેજ: {update.message.text}"
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    # જૂના કનેક્શન સાફ કરીને બોટ ચાલુ કરો
    app_bot.bot.delete_webhook(drop_pending_updates=True)
    app_bot.run_polling()
