import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, Application
from telegram import Update

TOKEN = '8835968464:AAEgKB1vwE2S9cy2ziv5VT6jII1iNuZuxQ'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

async def post_init(application: Application):
    await application.bot.send_message(chat_id=YOUR_CHAT_ID, text="હું તમારી શું મદદ કરી શકું !!!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        original_text = message.reply_to_message.text
        try:
            target_id = int(original_text.split("ID: ")[1].split("\n")[0])
            await context.bot.send_message(chat_id=target_id, text=message.text)
            await message.reply_text('✅ મેસેજ પહોંચી ગયો!')
        except:
            await message.reply_text('❌ મેસેજ ન મોકલી શકાયો.')
        return

    if chat.id != YOUR_CHAT_ID:
        user_info = f"👤 નામ: {user.first_name}\n🆔 ID: {user.id}\n💬 મેસેજ: {message.text}"
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    
    app_bot = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    # અહીં 'delete_webhook' ને કાઢી નાખ્યું છે જેથી ભૂલ ન આવે
    app_bot.run_polling()
