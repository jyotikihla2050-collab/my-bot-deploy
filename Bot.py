import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# લૉગિંગ સેટઅપ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Environment Variables માંથી ડેટા મેળવો
TOKEN = os.getenv('TOKEN')
MY_CHAT_ID = int(os.getenv('MY_CHAT_ID', 5306025504))
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID', -1003912250139))

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message or not message.text:
        return

    # ૧. જો મેસેજ તમારી પર્સનલ ચેટમાંથી આવ્યો હોય (રિપ્લાય આપવા માટે)
    if chat.id == MY_CHAT_ID:
        if message.reply_to_message:
            try:
                # મેસેજ ગ્રુપમાં મોકલો
                await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message.text)
                await message.reply_text("✅ મેસેજ સફળતાપૂર્વક ગ્રુપમાં મોકલાઈ ગયો છે!")
            except Exception as e:
                await message.reply_text(f"❌ ભૂલ આવી: {e}")
        return

    # ૨. જો મેસેજ ગ્રુપમાંથી આવ્યો હોય, તો તે તમને ફોરવર્ડ કરો
    if chat.id == GROUP_CHAT_ID:
        user = update.effective_user
        user_info = f"👤 {user.first_name} (ID: {user.id}) એ ગ્રુપમાં કહ્યું:\n\n{message.text}"
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=user_info)

if __name__ == '__main__':
    if not TOKEN:
        print("ભૂલ: TOKEN મળ્યું નથી! Render સેટિંગ્સ તપાસો.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
        print("Bot is running...")
        app.run_polling()
