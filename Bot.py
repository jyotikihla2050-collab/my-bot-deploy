import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# લૉગિંગ સેટઅપ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# અહીં તમારા ટોકન અને ID સીધા લખો
TOKEN = '8035968464:AAHa...'  # તમારું અસલી ટોકન અહીં મૂકો
MY_CHAT_ID = 5306025504
GROUP_CHAT_ID = -1003912250139

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("બોટ સક્રિય છે!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message or not message.text:
        return

    # ૧. જો તમે તમારી પર્સનલ ચેટમાં રિપ્લાય આપો છો
    if chat.id == MY_CHAT_ID:
        if message.reply_to_message:
            try:
                await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message.text)
                await message.reply_text("✅ મેસેજ ગ્રુપમાં મોકલાઈ ગયો છે!")
            except Exception as e:
                await message.reply_text(f"❌ ભૂલ આવી: {e}")
        return

    # ૨. જો કોઈ બીજાએ ગ્રુપમાં મેસેજ કર્યો હોય
    if chat.id == GROUP_CHAT_ID:
        user_info = f"👤 {update.effective_user.first_name} એ કહ્યું:\n\n{message.text}"
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=user_info)

if __name__ == '__main__':
    # બોટ એપ્લિકેશન તૈયાર કરો
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    print("Bot is running...")
    app.run_polling()
