import telebot
import os

# گرفتن توکن از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

# این هندلر وقتی کسی عضو جدید می‌شود (یا جوین می‌شود) فعال می‌شود
@bot.chat_member_handler()
def handle_new_chat_members(update):
    # بررسی می‌کنیم آیا تغییر وضعیت مربوط به عضویت جدید است؟
    if update.new_chat_member.status in ['member', 'restricted']:
        try:
            chat_id = update.chat.id
            user_id = update.new_chat_member.user.id
            
            # 1. اول کاربر را بن می‌کنیم (از کانال پرت می‌شود بیرون)
            bot.ban_chat_member(chat_id, user_id)
            
            # 2. بلافاصله کاربر را آن‌بن می‌کنیم (از لیست سیاه خارج می‌شود)
            # این باعث می‌شود فقط "عضویتش" لغو شود اما بلاک نشود
            bot.unban_chat_member(chat_id, user_id)
            
            print(f"User {user_id} removed (Soft Ban) from chat {chat_id}")
            
        except Exception as e:
            print(f"Error removing user: {e}")

# برای اطمینان از اینکه پیام‌های سیستمی ورود هم پاک شوند (اختیاری)
@bot.message_handler(content_types=['new_chat_members'])
def delete_join_message(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # بن کردن
        bot.ban_chat_member(chat_id, user_id)
        # آن‌بن کردن فوری (برای جلوگیری از بلاک شدن دائمی)
        bot.unban_chat_member(chat_id, user_id)
        
        # پاک کردن پیام "فلانی وارد شد"
        bot.delete_message(chat_id, message.message_id)
        
    except Exception as e:
        print(f"Error handling join message: {e}")

print("Bot is running...")
# هندل کردن همه آپدیت‌ها مربوط به ممبرها
bot.infinity_polling(allowed_updates=['chat_member', 'message'])
