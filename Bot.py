import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from telegram import Update, Bot

# અહીં તમારા ટોકન અને IDs મૂકો
TOKEN = '8835968464:AAEgKB1vwE2S9cy2ziv5VT6jII1iNuZuxQ'
YOUR_CHAT_ID = 5306025504
GROUP_ID = -1003912250139 

app = Flask(__name__)

# બોટ સ્ટાર્ટ થતી વખતે મેસેજ મોકલવા માટે
async def post_init(application: ApplicationBuilder):
    await application.bot.send_message(chat_id=YOUR_CHAT_ID, text="બોટ શરૂ થઈ ગયો છે! હું તમારી શું મદદ કરી શકું !!!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("હું તમારી શું મદદ કરી શકું !!!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    # ૧. જો તમે રિપ્લાય આપો છો (યુઝરને જવાબ આપવા માટે)
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        try:
            # મેસેજમાંથી ટાર્ગેટ યુઝરનું ID મેળવવું
            original_text = message.reply_to_message.text
            target_id = int(original_text.split("ID: ")[1].split("\n")[0])
            await context.bot.send_message(chat_id=target_id, text=message.text)
            await message.reply_text('✅ મેસેજ પહોંચી ગયો!')
        except Exception as e:
            await message.reply_text('❌ મેસેજ ન મોકલી શકાયો. ખાતરી કરો કે તમે ID વાળા મેસેજ પર જ રિપ્લાય આપ્યો છે.')
        return

    # ૨. જો મેસેજ બીજા કોઈ યુઝરનો હોય, તો તેને પર્સનલ અને ગ્રુપમાં ફોરવર્ડ કરો
    if chat.id != YOUR_CHAT_ID and chat.id != GROUP_ID:
        user_info = f"👤 નામ: {user.first_name}\n🆔 ID: {user.id}\n💬 મેસેજ: {message.text}"
        
        # તમારી પર્સનલ ચેટમાં મોકલો
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)
        
        # ગ્રુપમાં મોકલો
        await context.bot.send_message(chat_id=GROUP_ID, text=user_info)

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
