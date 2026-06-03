from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ૧. તમારું ટોકન અહીં લખો
TOKEN = 'તમારું_બોટ_ટોકન_અહીં_લખો'

# ૨. તમારી પોતાની (Admin) ચેટ ID
MY_CHAT_ID = 5306025504 

# ૩. તમારા ગ્રુપની ID જે તમે શોધી છે
GROUP_CHAT_ID = -1003912250139 

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    # જો મેસેજ તમારી પર્સનલ ચેટમાંથી આવ્યો હોય
    if chat.id == MY_CHAT_ID:
        # જો તમે કોઈ મેસેજને રિપ્લાય આપ્યો હોય
        if message.reply_to_message:
            try:
                # મેસેજ ગ્રુપમાં મોકલો
                await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message.text)
                await message.reply_text("✅ મેસેજ ગ્રુપમાં મોકલાઈ ગયો છે!")
            except Exception as e:
                await message.reply_text(f"❌ ભૂલ આવી: {e}")
        return

    # જો મેસેજ ગ્રુપમાંથી આવ્યો હોય, તો તે તમને ફોરવર્ડ કરો
    if chat.id == GROUP_CHAT_ID:
        user = update.effective_user
        # આ તમારા પર્સનલ ચેટમાં મેસેજ લાવશે
        user_info = f"👤 {user.first_name} (ID: {user.id}) એ ગ્રુપમાં કહ્યું:\n\n{message.text}"
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=user_info)

if __name__ == '__main__':
    # બોટ એપ્લિકેશન તૈયાર કરો
    app = ApplicationBuilder().token(TOKEN).build()
    
    # બધા મેસેજ હેન્ડલ કરવા માટે હેન્ડલર ઉમેરો
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_all))
    
    # બોટ શરૂ કરો
    print("બોટ ચાલી રહ્યો છે...")
    app.run_polling()
