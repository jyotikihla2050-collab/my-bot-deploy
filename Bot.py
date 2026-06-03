import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from telegram import Update

# તમારા ટોકન અને IDs અહીં સાચા છે તેની ખાતરી કરી લેવી
TOKEN = '8835968464:AAEgKB1vwE2S9cy2ziv5VT6jII1iNuZuxQ'
YOUR_CHAT_ID = 5306025504
GROUP_ID = -1003912250139 

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("બોટ સક્રિય છે અને કામ કરી રહ્યો છે!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    # ૧. રિપ્લાય લોજિક (તમે રિપ્લાય આપો છો)
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        original_text = message.reply_to_message.text
        
        # જો મેસેજ ગ્રુપમાંથી આવ્યો હોય, તો જવાબ ગ્રુપમાં મોકલો
        if "ગ્રુપમાં નવો મેસેજ:" in original_text:
            await context.bot.send_message(chat_id=GROUP_ID, text=f"રિપ્લાય:\n{message.text}")
            await message.reply_text('✅ જવાબ ગ્રુપમાં મોકલી દીધો!')
            return
        
        # જો મેસેજ પર્સનલ ચેટનો હોય, તો યુઝરને મોકલો
        if "ID: " in original_text:
            try:
                target_id = int(original_text.split("ID: ")[1].split("\n")[0])
                await context.bot.send_message(chat_id=target_id, text=message.text)
                await message.reply_text('✅ યુઝરને મેસેજ મોકલી દીધો!')
            except:
                await message.reply_text('❌ યુઝર આઈડી મળ્યું નથી.')
            return

    # ૨. જો મેસેજ ગ્રુપમાંથી આવ્યો હોય: તો તેને તમારી પર્સનલ ચેટમાં ફોરવર્ડ કરો
    if chat.id == GROUP_ID:
        forward_text = f"ગ્રુપમાં નવો મેસેજ:\n👤 નામ: {message.from_user.first_name}\n💬 મેસેજ: {message.text}"
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=forward_text)
        return

    # ૩. જો મેસેજ બોટ (પર્સનલ ચેટ) માંથી આવ્યો હોય
    if chat.id != YOUR_CHAT_ID:
        user_info = f"👤 નામ: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}\n💬 મેસેજ: {message.text}"
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    print("Bot is running...")
    # પોલિંગ દ્વારા બોટ શરૂ કરો
    app_bot.run_polling(drop_pending_updates=True)
