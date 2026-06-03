import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from telegram import Update

TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.message
    
    # 1. જો મેસેજ તમારા તરફથી આવ્યો હોય (તમે કોઈને રિપ્લાય આપો છો)
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        # રિપ્લાયમાં રહેલા યુઝરનું ID શોધો
        original_text = message.reply_to_message.text
        # અહીં આપણે મેસેજમાંથી ID કાઢવાનો પ્રયત્ન કરીશું (જે તમે ફોરવર્ડ કરેલા મેસેજમાં મોકલી હતી)
        try:
            # આ તમારી ફોર્મેટમાંથી ID શોધી કાઢશે
            target_id = int(original_text.split("🆔 ID: ")[1].split("\n")[0])
            await context.bot.send_message(chat_id=target_id, text=message.text)
            await message.reply_text("✅ મેસેજ પહોંચી ગયો!")
        except:
            await message.reply_text("❌ મેસેજ ન મોકલી શકાયો. ખાતરી કરો કે તમે ID વાળા મેસેજ પર જ રિપ્લાય આપ્યો છે.")
        return

    # 2. જો મેસેજ બીજા કોઈ યુઝરનો હોય (તો તમને ફોરવર્ડ કરો)
    if chat.id != YOUR_CHAT_ID:
        user_info = f"👤 નામ: {user.first_name}\n🆔 ID: {user.id}\n💬 ચેટ ID: {chat.id}\n📝 મેસેજ: {message.text}"
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
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    app_bot.bot.delete_webhook(drop_pending_updates=True)
    app_bot.run_polling()
