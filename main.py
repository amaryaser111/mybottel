import telebot
import time
import os
import sys

# دریافت توکن از متغیرهای محیطی گیت‌هاب (امنیت بالا)
TOKEN = os.environ.get('BOT_TOKEN')

if not TOKEN:
    print("Error: BOT_TOKEN not found!")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)

# این هندلر فقط تغییرات اعضا (مثل جوین شدن) را رصد می‌کند
@bot.chat_member_handler()
def handle_chat_member_update(update):
    try:
        # بررسی وضعیت جدید کاربر
        new_status = update.new_chat_member.status
        
        # اگر کاربر عضو شد (member) ولی ادمین یا سازنده نیست
        if new_status == 'member':
            user_id = update.new_chat_member.user.id
            chat_id = update.chat.id
            first_name = update.new_chat_member.user.first_name
            
            print(f"User {first_name} ({user_id}) joined. Kicking...")

            # 1. کاربر را بن (اخراج) می‌کنیم
            bot.ban_chat_member(chat_id, user_id)
            
            # 2. یک ثانیه صبر می‌کنیم تا تلگرام پردازش کند
            time.sleep(1)
            
            # 3. کاربر را آنبن می‌کنیم (تا بلاک نماند و بتواند کانال را ببیند)
            bot.unban_chat_member(chat_id, user_id)
            
            print(f"User {first_name} kicked and unbanned successfully.")
            
    except Exception as e:
        print(f"Error occurred: {e}")

print("Bot started and listening for joins...")
# اجرای ربات
bot.infinity_polling(allowed_updates=['chat_member'], timeout=10, long_polling_timeout=5)
