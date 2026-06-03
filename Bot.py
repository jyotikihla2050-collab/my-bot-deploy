from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

# તમારો ટોકન
TOKEN = '8835968464:AAHa0sZGbmmQrYQa8UXbwHIeeuwv40G68AA'
# તમારી પોતાની ID જે તમે મેળવી હતી
YOUR_CHAT_ID = 5306025504

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # જો મેસેજ તમારી પાસે આવે (તમારી ID થી)
    if update.effective_chat.id == YOUR_CHAT_ID:
        if update.message.reply_to_message:
            # જો તમે ફોરવર્ડ કરેલા મેસેજ પર રિપ્લાય આપશો, તો બોટ તે યુઝરને મોકલશે
            try:
                # યુઝરની ID જે આપણે મેસેજમાં મોકલી હતી
                text = update.message.reply_to_message.text
                user_id = text.split("ID: ")[1].split("\n")[0]
                await context.bot.send_message(chat_id=user_id, text=update.message.text)
            except:
                await update.message.reply_text("ભૂલ: આ રિપ્લાયમાં ID મળતી નથી.")
    else:
        # જો કોઈ બીજા યુઝરનો મેસેજ હોય, તો તે તમારી પાસે ફોરવર્ડ કરો
        user_info = f"ID: {update.effective_chat.id}\nયુઝર: {update.effective_chat.first_name}\n\n{update.message.text}"
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    print("બોટ હવે તૈયાર છે! ફક્ત પર્સનલ ચેટમાં વાત કરો.")
    app.run_polling()
