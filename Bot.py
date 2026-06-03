import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

# તમારો ટોકન અને ID
TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
YOUR_CHAT_ID = 5306025504

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == YOUR_CHAT_ID:
        if update.message.reply_to_message:
            try:
                text = update.message.reply_to_message.text
                user_id = text.split("ID: ")[1].split("\n")[0]
                await context.bot.send_message(chat_id=user_id, text=update.message.text)
            except:
                await update.message.reply_text("ભૂલ: આ રિપ્લાયમાં ID મળી નથી.")
        else:
            user_info = f"ID: {update.effective_chat.id}\nમેસેજ: {update.message.text}"
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

app = Flask(__name__)
@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # વેબ સર્વર ચાલુ કરો
    Thread(target=run_flask).start()
    
    # બોટ ચાલુ કરો
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    print("બોટ હવે તૈયાર છે!")
    app_bot.run_polling()
