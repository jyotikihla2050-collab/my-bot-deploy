import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

# તમારા બોટનો ટોકન અને તમારું Chat ID
TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
YOUR_CHAT_ID = 5306025504

app = Flask(__name__)

# મુખ્ય ફંક્શન જે ગ્રુપ અને પ્રાઇવેટ બંને મેસેજ હેન્ડલ કરશે
async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    # ખાતરી કરો કે મેસેજ ટેક્સ્ટ છે
    if update.message and update.message.text:
        # ફક્ત બીજાના મેસેજ ફોરવર્ડ કરો, તમારા પોતાના નહીં
        if chat.id != YOUR_CHAT_ID:
            # જો ગ્રુપમાં હોય તો ગ્રુપનું નામ અને ID પણ આવશે
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
    # ફ્લાસ્કને અલગ થ્રેડમાં ચલાવો
    Thread(target=run_flask).start()
    
    # ટેલિગ્રામ બોટ ચલાવો
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    print("બોટ હવે સક્રિય છે!")
    app_bot.run_polling()
