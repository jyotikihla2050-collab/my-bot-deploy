import os
import re
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes

# --- કોન્ફિગરેશન ---
TOKEN = '8835968464:AAGLJz1EfAVzafHgqbnJ66uEQRR2dbBHhUk' #
YOUR_CHAT_ID = 5306025504 #
GROUP_ID = -1003912250139 #

app = Flask(__name__)

# ૧. સ્ટાર્ટ કમાન્ડ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("નમસ્તે! બોટ સેટ થઈ ગયો છે. હવે તમે સુરક્ષિત રીતે ચેટ કરી શકશો.")

# ૨. મુખ્ય હેન્ડલર
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message:
        return

    # A. જો એડમિન (તમે) કોઈ મેસેજ પર રિપ્લાય આપો છો
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        original_msg = message.reply_to_message.text or message.reply_to_message.caption or ""
        
        # ગ્રુપમાં જવાબ મોકલવા માટે
        if "ગ્રુપમાં નવો મેસેજ:" in original_msg:
            try:
                await context.bot.copy_message(
                    chat_id=GROUP_ID,
                    from_chat_id=YOUR_CHAT_ID,
                    message_id=message.message_id,
                    protect_content=True  # સ્ક્રીનશોટ અને ફોરવર્ડિંગ પ્રોટેક્શન
                )
                await message.reply_text('✅ જવાબ ગ્રુપમાં મોકલી દીધો! (Protected)')
            except Exception as e:
                await message.reply_text(f'❌ ભૂલ: {e}')
            return

        # પર્સનલ યુઝરને જવાબ મોકલવા માટે (Regex થી ID શોધશે)
        id_match = re.search(r"ID:\s*(\d+)", original_msg)
        if id_match:
            target_id = int(id_match.group(1))
            try:
                await context.bot.copy_message(
                    chat_id=target_id,
                    from_chat_id=YOUR_CHAT_ID,
                    message_id=message.message_id,
                    protect_content=True  # સ્ક્રીનશોટ અને ફોરવર્ડિંગ પ્રોટેક્શન
                )
                await message.reply_text(f'✅ યુઝર (ID: {target_id}) ને મેસેજ મોકલ્યો! (Protected)')
            except Exception as e:
                await message.reply_text(f'❌ યુઝરને મેસેજ ન મોકલી શકાયો: {e}')
        else:
            await message.reply_text('❌ રિપ્લાય મેસેજમાં ID મળ્યું નથી.')
        return

    # B. જો ગ્રુપમાંથી કોઈ મેસેજ આવે તો તમને મોકલે
    if chat.id == GROUP_ID:
        user_name = message.from_user.first_name
        caption = f"💬 ગ્રુપમાં નવો મેસેજ:\n👤 નામ: {user_name}\n💬 મેસેજ: {message.text or ''}"
        
        await context.bot.copy_message(
            chat_id=YOUR_CHAT_ID,
            from_chat_id=GROUP_ID,
            message_id=message.message_id,
            caption=caption if not message.text else None
        )
        if message.text:
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=caption)
        return

    # C. જો કોઈ નવો યુઝર પર્સનલમાં બોટને મેસેજ કરે
    if chat.id != YOUR_CHAT_ID:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        info = f"👤 નામ: {user_name}\n🆔 ID: {user_id}\n💬 મેસેજ: {message.text or ''}"
        
        await context.bot.copy_message(
            chat_id=YOUR_CHAT_ID,
            from_chat_id=chat.id,
            message_id=message.message_id,
            caption=info if not message.text else None
        )
        if message.text:
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=info)

# Flask Server
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    
    # બધા મીડિયા ટાઈપ માટે ફિલ્ટર[cite: 1]
    all_media = (filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL)
    app_bot.add_handler(MessageHandler(all_media & (~filters.COMMAND), handle_message))
    
    print("બોટ શરૂ થઈ ગયો છે...")
    app_bot.run_polling(drop_pending_updates=True)
