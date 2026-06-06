import os
import re
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes

# --- કોન્ફિગરેશન ---
TOKEN = '8835968464:AAGLJz1EfAVzafHgqbnJ66uEQRR2dbBHhUk'
YOUR_CHAT_ID = 5306025504
GROUP_ID = -1003912250139

app = Flask(__name__)

# મેસેજ મોકલીને ૧૦ સેકન્ડમાં ડિલીટ કરવાનું નવું પાવરફુલ ફંક્શન
async def send_and_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message: Update.message):
    try:
        sent_msg = None
        text_content = message.text or message.caption or ""

        # મેસેજના પ્રકાર (Type) મુજબ અલગથી મોકલો જેથી Delete ID પાકો મળે
        if message.photo:
            sent_msg = await context.bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id, caption=text_content, protect_content=True)
        elif message.video:
            sent_msg = await context.bot.send_video(chat_id=chat_id, video=message.video.file_id, caption=text_content, protect_content=True)
        elif message.document:
            sent_msg = await context.bot.send_document(chat_id=chat_id, document=message.document.file_id, caption=text_content, protect_content=True)
        elif message.text:
            sent_msg = await context.bot.send_message(chat_id=chat_id, text=text_content, protect_content=True)

        # જો મેસેજ સક્સેસફુલી મોકલાઈ ગયો હોય, તો ૧૦ સેકન્ડનું ટાઈમર શરૂ કરો
        if sent_msg:
            await asyncio.sleep(300) # અહીં સમય બદલી શકો છો (૧૦ સેકન્ડ)
            await context.bot.delete_message(chat_id=chat_id, message_id=sent_msg.message_id)
            print(f"✅ મેસેજ સફળતાપૂર્વક ડિલીટ થયો: {sent_msg.message_id}")
            
    except Exception as e:
        print(f"❌ ડિલીટ કરવામાં ભૂલ આવી: {e}")

# ૧. સ્ટાર્ટ કમાન્ડ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("નમસ્તે! હું બોટ છું. તમારી શું મદદ કરી શકું.")

# ૨. મુખ્ય હેન્ડલર
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message
    
    if not message:
        return

    # A. જો એડમિન (તમે) કોઈ મેસેજ પર રિપ્લાય આપો છો
    if chat.id == YOUR_CHAT_ID and message.reply_to_message:
        original_msg = message.reply_to_message.text or message.reply_to_message.caption or ""
        
        # ગ્રુપમાં સેલ્ફ-ડિસ્ટ્રક્ટ જવાબ મોકલવા માટે
        if "ગ્રુપમાં નવો મેસેજ:" in original_msg:
            asyncio.create_task(send_and_delete(context, GROUP_ID, message))
            await message.reply_text('✅ જવાબ ગ્રુપમાં મોકલ્યો છે, ૧૦ સેકન્ડમાં ડિલીટ થઈ જશે!')
            return

        # પર્સનલ યુઝરને સેલ્ફ-ડિસ્ટ્રક્ટ જવાબ મોકલવા માટે
        id_match = re.search(r"ID:\s*(\d+)", original_msg)
        if id_match:
            target_id = int(id_match.group(1))
            asyncio.create_task(send_and_delete(context, target_id, message))
            await message.reply_text(f'✅ યુઝર (ID: {target_id}) ને મેસેજ મોકલ્યો, ૧૦ સેકન્ડમાં ડિલીટ થઈ જશે!')
        else:
            await message.reply_text('❌ રિપ્લાય મેસેજમાં ID મળ્યું નથી.')
        return

    # B. જો ગ્રુપમાંથી કોઈ મેસેજ આવે તો તમને મોકલે
    if chat.id == GROUP_ID:
        user_name = message.from_user.first_name
        caption = f"💬 ગ્રુપમાં નવો મેસેજ:\n👤 નામ: {user_name}\n💬 મેસેજ: {message.text or ''}"
        
        await context.bot.copy_message(chat_id=YOUR_CHAT_ID, from_chat_id=GROUP_ID, message_id=message.message_id, caption=caption if not message.text else None)
        if message.text:
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=caption)
        return

    # C. જો કોઈ યુઝર પર્સનલમાં બોટને મેસેજ કરે
    if chat.id != YOUR_CHAT_ID:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        info = f"👤 નામ: {user_name}\n🆔 ID: {user_id}\n💬 મેસેજ: {message.text or ''}"
        
        await context.bot.copy_message(chat_id=YOUR_CHAT_ID, from_chat_id=chat.id, message_id=message.message_id, caption=info if not message.text else None)
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
    
    all_media = (filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL)
    app_bot.add_handler(MessageHandler(all_media & (~filters.COMMAND), handle_message))
    
    print("બોટ શરૂ થઈ ગયો છે...")
    app_bot.run_polling(drop_pending_updates=True)
