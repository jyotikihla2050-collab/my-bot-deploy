import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv('TOKEN')
MY_CHAT_ID = int(os.getenv('MY_CHAT_ID'))
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID'))

# /start કમાન્ડ માટે ફંક્શન
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 નમસ્તે! બોટ તૈયાર છે. હવે તમે ગ્રુપના મેસેજ અહીં જોઈ શકશો અને રિપ્લાય આપી શકશો.")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message or not message.text:
        return

    # ૧. જો તમારી પર્સનલ ચેટમાંથી મેસેજ આવ્યો હોય
    if chat.id == MY_CHAT_ID:
        if message.reply_to_message:
            try:
                await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message.text)
                await message.reply_text("✅ મેસેજ સફળતાપૂર્વક ગ્રુપમાં મોકલાઈ ગયો છે!") # આ લાઇન તમને મેસેજ આપશે
            except Exception as e:
                await message.reply_text(f"❌ ભૂલ આવી: {e}")
        return

    # ૨. જો ગ્રુપમાંથી મેસેજ આવ્યો હોય
    if chat.id == GROUP_CHAT_ID:
        user_info = f"👤 {update.effective_user.first_name} એ કહ્યું:\n\n{message.text}"
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=user_info)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # /start કમાન્ડ હેન્ડલર ઉમેર્યું
    app.add_handler(CommandHandler("start", start))
    # બાકીના મેસેજ માટે હેન્ડલર
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    print("Bot is running...")
    app.run_polling()
