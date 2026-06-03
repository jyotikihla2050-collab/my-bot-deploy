import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, Application, CommandHandler
from telegram import Update

TOKEN = '8835968464:AAE1VshLpK1WZUwnXeh2AqkIZwADv01fkGg'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("હું તમારી શું મદદ કરી શકું !!!")

async def post_init(application: Application):
    # આ બોટ સ્ટાર્ટ થતા જ મેસેજ મોકલશે
    await application.bot.send_message(chat_id=YOUR_CHAT_ID, text="બોટ શરૂ થઈ ગયો છે! હું તમારી શું મદદ કરી શકું !!!")

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
    # ફ્લાસ્ક સર્વર ચાલુ કરો
    Thread(target=run_flask).start()
    
    # બોટ એપ્લિકેશન તૈયાર કરો
    app_bot = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    # હેન્ડલર્સ ઉમેરો
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    # પોલિંગ શરૂ કરો
    print("Bot is polling...")
    app_bot.run_polling(drop_pending_updates=True)
