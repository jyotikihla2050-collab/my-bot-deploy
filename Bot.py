import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# લૉગિંગ સેટઅપ
logging.basicConfig(level=logging.INFO)

# Environment Variables મેળવો
TOKEN = os.getenv('TOKEN')
# જો વેલ્યુ ન મળે તો 0 લેશે, જેથી બોટ ક્રેશ ન થાય
MY_CHAT_ID = int(os.getenv('MY_CHAT_ID') or 0)
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID') or 0)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("બોટ સક્રિય છે અને ગ્રુપ સાથે કનેક્ટ થયેલ છે!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message or not message.text:
        return

    # પર્સનલ ચેટમાંથી રિપ્લાય આપવો
    if chat.id == MY_CHAT_ID:
        if message.reply_to_message:
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message.text)
            await message.reply_text("✅ મેસેજ ગ્રુપમાં મોકલાઈ ગયો છે!")
        return

    # ગ્રુપમાંથી મેસેજ પર્સનલમાં લાવવો
    if chat.id == GROUP_CHAT_ID:
        forward_text = f"👤 {update.effective_user.first_name}:\n{message.text}"
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=forward_text)

if __name__ == '__main__':
    if not TOKEN:
        print("ભૂલ: TOKEN મળ્યું નથી! Render સેટિંગ્સ તપાસો.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("બોટ રન થઈ રહ્યો છે...")
        app.run_polling()
