import os
import re
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes

# --- કોન્ફિગરેશન ---
TOKEN = '8835968464:AAGLJz1EfAVzafHgqbnJ66uEQRR2dbBHhUk' # તમારો ટોકન
YOUR_CHAT_ID = 5306025504 # તમારી પર્સનલ આઈડી
GROUP_ID = -1003912250139 # તમારા ગ્રુપની આઈડી

app = Flask(__name__)

# ૧. સ્ટાર્ટ કમાન્ડ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("નમસ્તે! હું બોટ છું. હું તમારા મેસેજ ફોરવર્ડ કરવામાં મદદ કરીશ.")

# ૨. મુખ્ય હેન્ડલર (બધા મેસેજ માટે)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message:
        return

    # A. જો તમે (ADMIN) કોઈ મેસેજ પર રિપ્લાય આપો છો
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        original_msg = message.reply_to_message.text or message.reply_to_message.caption or ""
        
        # ગ્રુપમાં જવાબ મોકલવા માટે
        if "ગ્રુપમાં નવો મેસેજ:" in original_msg:
            try:
                await context.bot.copy_message(
                    chat_id=GROUP_ID,
                    from_chat_id=YOUR_CHAT_ID,
                    message_id=message.message_id
                )
                await message.reply_text('✅ જવાબ ગ્રુપમાં મોકલી દીધો!')
            except Exception as e:
                await message.reply_text(f'❌ ભૂલ આવી: {e}')
            return

        # પર્સનલ યુઝરને જવાબ મોકલવા માટે (Regex થી ID શોધશે)
        id_match = re.search(r"ID:\s*(\d+)", original_msg)
        if id_match:
            target_id = int(id_match.group(1))
            try:
                await context.bot.copy_message(
                    chat_id=target_id,
                    from_chat_id=YOUR_CHAT_ID,
                    message_id=message.message_id
                )
                await message.reply_text(f'✅ યુઝર (ID: {target_id}) ને મેસેજ મોકલી દીધો!')
            except Exception as e:
                await message.reply_text(f'❌ યુઝરને મેસેજ ન મોકલી શકાયો: {e}')
        else:
            await message.reply_text('❌ રિપ્લાય કરેલા મેસેજમાં કોઈ ID મળ્યું નથી.')
        return

    # B. જો ગ્રુપમાંથી કોઈ મેસેજ આવે તો તમને મોકલે
    if chat.id == GROUP_ID:
        caption = f"💬 ગ્રુપમાં નવો મેસેજ:\n👤 નામ: {message.from_user.first_name}\n💬 મેસેજ: {message.text or ''}"
        await context.bot.copy_message(
            chat_id=YOUR_CHAT_ID,
            from_chat_id=GROUP_ID,
            message_id=message.message_id,
            caption=caption if not message.text else None
        )
        if message.text:
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=caption)
        return

    # C. જો કોઈ યુઝર પર્સનલમાં બોટને મેસેજ કરે
    if chat.id != YOUR_CHAT_ID:
        user_info = f"👤 નામ: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}\n💬 મેસેજ: {message.text or ''}"
        await context.bot.copy_message(
            chat_id=YOUR_CHAT_ID,
            from_chat_id=chat.id,
            message_id=message.message_id,
            caption=user_info if not message.text else None
        )
        if message.text:
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_info)

# Flask Web Server (Render/Heroku માટે)
@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Flask ને અલગ થ્રેડમાં ચલાવો
    Thread(target=run_flask).start()
    
    # બોટ સેટઅપ
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    
    # ટેક્સ્ટ, ફોટો, વિડિયો અને ડોક્યુમેન્ટ ફિલ્ટર
    all_media = (filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL)
    app_bot.add_handler(MessageHandler(all_media & (~filters.COMMAND), handle_message))
    
    print("બોટ શરૂ થઈ રહ્યો છે...")
    app_bot.run_polling(drop_pending_updates=True)
