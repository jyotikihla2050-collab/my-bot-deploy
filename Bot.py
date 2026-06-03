import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from telegram import Update

# તમારા બોટનો ટોકન અને તમારું Chat ID
TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

# /start કમાન્ડનો જવાબ આપવા માટેનું ફંક્શન
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("નમસ્કાર શું મદદ કરી શકું આપની!!!")

# મેસેજ હેન્ડલ કરવા માટેનું ફંક્શન
async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    if update.message and update.message.text:
        if chat.id != YOUR_CHAT_ID:
            chat_info = f"ગ્રુપ: {chat.title}" if chat.title else "પ્રાઇવેટ ચેટ"
            user_info = f"👤 નામ: {user.first_name}\n🆔 ID: {user.id}\n💬 {chat_info} (ID: {chat.id})\n📝 મેસેજ: {update.message.text}"
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

@app.route('/')
def index():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    # અહીં 'start' કમાન્ડ ઉમેર્યું છે
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    print("બોટ હવે સક્રિય છે!")
    app_bot.run_polling()
