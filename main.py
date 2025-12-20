import telebot
import os
import time

# دریافت توکن
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

print("Bot is running...")

# هندلر برای وقتی کسی جدید وارد می‌شود (پیام سرویس)
@bot.message_handler(content_types=['new_chat_members'])
def ban_new_members(message):
    try:
        chat_id = message.chat.id
        for user in message.new_chat_members:
            print(f"Detecting user: {user.first_name}")
            # کاربر را بن میکند
            bot.ban_chat_member(chat_id, user.id)
            # بلافاصله آنبن میکند تا بتواند بعدا برگردد (اختیاری)
            # bot.unban_chat_member(chat_id, user.id) 
            print(f"Kicked user: {user.id}")
            
            # پاک کردن پیام "فلانی وارد شد"
            try:
                bot.delete_message(chat_id, message.message_id)
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")

# هندلر برای آپدیت وضعیت اعضا (روش مدرن‌تر برای کانال‌ها)
@bot.chat_member_handler()
def chat_member_update(event):
    # اگر کاربری وضعیتش به 'member' تغییر کرد (یعنی جوین شد)
    if event.new_chat_member.status == 'member' and event.old_chat_member.status != 'member':
        try:
            user_id = event.new_chat_member.user.id
            chat_id = event.chat.id
            print(f"New member detected via update: {user_id}")
            
            bot.ban_chat_member(chat_id, user_id)
            print(f"Kicked user: {user_id}")
        except Exception as e:
            print(f"Error in chat_member_handler: {e}")

# اجرای ربات با قابلیت شنیدن همه چیز
bot.infinity_polling(allowed_updates=['message', 'chat_member', 'my_chat_member'])
