import os
from flask import Flask
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

# મુખ્ય બોટ ફંક્શન
async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if update.message and update.message.text:
        user_info = f"નામ: {user.first_name}\nID: {user.id}\nચેટ ID: {chat.id}\nમેસેજ: {update.message.text}"
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # બોટ અને ફ્લાસ્ક બંનેને એકસાથે ચલાવવા માટે
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
