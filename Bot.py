import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from telegram import Update

TOKEN = '8835968464:AAEgKB1vwE2S9cy2ziv5VT6jII1iNuZuxQ'
YOUR_CHAT_ID = 5306025504
GROUP_ID = -1003912250139 

app = Flask(__name__)

async def post_init(application):
    await application.bot.send_message(chat_id=YOUR_CHAT_ID, text="બોટ તૈયાર છે!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("હું તમારી શું મદદ કરી શકું !!!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    # ૧. જો તમે બોટને રિપ્લાય આપો છો (યુઝરને જવાબ આપવા માટે)
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        try:
            original_text = message.reply_to_message.text
            target_id = int(original_text.split("ID: ")[1].split("\n")[0])
            await context.bot.send_message(chat_id=target_id, text=message.text)
            await message.reply_text('✅ મેસેજ પહોંચી ગયો!')
        except Exception:
            await message.reply_text('❌ રિપ્લાય ન મોકલી શકાયો.')
        return

    # ૨. જો મેસેજ ગ્રુપમાંથી આવ્યો હોય: તો તેને તમારી પર્સનલ ચેટમાં પણ મોકલો
    if chat.id == GROUP_ID:
        # ફક્ત તમારી પર્સનલ ચેટમાં મેસેજ ફોરવર્ડ કરો
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"ગ્રુપમાં નવો મેસેજ:\n👤 નામ: {user.first_name}\n💬 મેસેજ: {message.text}")
        return

    # ૩. જો મેસેજ બોટ (પર્સનલ ચેટ) માંથી આવ્યો હોય: તો તેને ફક્ત તમારી પાસે રાખો (ગ્રુપમાં નહીં)
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
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    print("Bot is running...")
    app_bot.run_polling(drop_pending_updates=True)
