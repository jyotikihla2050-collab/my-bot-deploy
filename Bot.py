import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, Application
from telegram import Update

TOKEN = '8835968464:AAHa8sZGbmrQrYQa0UXbwHIeeuw40G6IAA'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

# બોટ શરૂ થાય ત્યારે મેસેજ મોકલવાનું ફંક્શન
async def post_init(application: Application):
    await application.bot.send_message(chat_id=YOUR_CHAT_ID, text="હું તમારી શું મદદ કરી શકું !!!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    # 1. જો મેસેજ તમારા તરફથી આવ્યો હોય (તમે કોઈને રિપ્લાય આપો છો)
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        original_text = message.reply_to_message.text
        try:
            # આ તમારી ફોર્મેટમાંથી ID શોધી કાઢશે
            target_id = int(original_text.split("ID: ")[1].split("\n")[0])
            await context.bot.send_message(chat_id=target_id, text=message.text)
            await message.reply_text('✅ મેસેજ પહોંચી ગયો!')
        except:
            await message.reply_text('❌ મેસેજ ન મોકલી શકાયો. ખાતરી કરો કે તમે ID વાળા મેસેજ પર જ રિપ્લાય આપ્યો છે.')
        return

    # 2. જો મેસેજ બીજા કોઈ યુઝરનો હોય
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
    # ફ્લાસ્ક સર્વર ચાલુ કરો
    Thread(target=run_flask).start()
    
    # બોટ એપ્લિકેશન તૈયાર કરો અને post_init સેટ કરો
    app_bot = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    # મેસેજ હેન્ડલર ઉમેરો
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    # વેબહુક ડિલીટ કરી પોલિંગ શરૂ કરો
    app_bot.bot.delete_webhook(drop_pending_updates=True)
    app_bot.run_polling()
