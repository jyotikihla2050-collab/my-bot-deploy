import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# લૉગિંગ સેટઅપ (ભૂલ શોધવા માટે)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Render ના Environment Variables માંથી ડેટા મેળવવો
TOKEN = os.getenv('TOKEN')
MY_CHAT_ID = int(os.getenv('MY_CHAT_ID'))
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID'))

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message or not message.text:
        return

    # જો મેસેજ તમારી પર્સનલ ચેટમાંથી આવ્યો હોય
    if chat.id == MY_CHAT_ID:
        if message.reply_to_message:
            try:
                await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message.text)
            except Exception as e:
                await message.reply_text(f"ભૂલ: {e}")
        return

    # જો મેસેજ ગ્રુપમાંથી આવ્યો હોય
    if chat.id == GROUP_CHAT_ID:
        user_info = f"👤 {update.effective_user.first_name} (ID: {update.effective_user.id}) એ કહ્યું:\n\n{message.text}"
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=user_info)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    print("Bot is running...")
    app.run_polling()
