import telebot
import time

# ===== ЗАМЕНИТЕ ЭТИ ДВЕ СТРОЧКИ =====
BOT_TOKEN = "8841305618:AAGAvmWazoEfLU-Mw9APHEGs-zbOp5t2qRU"
ADMIN_ID = 7686890144

# Словарь для хранения ответов пользователей
user_data = {}

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    
    # Отправляем уведомление админу
    try:
        bot.send_message(
            ADMIN_ID,
            f"🔔 <b>Кто-то нажал /start!</b>\n\n"
            f"👤 Имя: {message.from_user.first_name}\n"
            f"📱 Юзернейм: @{message.from_user.username if message.from_user.username else 'нет'}\n"
            f"🆔 ID: {user_id}",
            parse_mode="HTML"
        )
    except:
        pass
    
    bot.send_message(message.chat.id, "📋 Здравствуйте! Ответьте на несколько вопросов.\n\n1️⃣ Сколько вам лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_id = message.from_user.id
    user_data[user_id]['age'] = message.text
    bot.send_message(message.chat.id, "2️⃣ Имеете ли вы опыт работы с «лохматыми»?\n(напишите да/нет или подробно)")
    bot.register_next_step_handler(message, get_experience)

def get_experience(message):
    user_id = message.from_user.id
    user_data[user_id]['experience'] = message.text
    bot.send_message(message.chat.id, "3️⃣ Какая у вас была прошлая сфера работы? (если есть)\nЕсли нет опыта, напишите «нет»")
    bot.register_next_step_handler(message, get_past_sphere)

def get_past_sphere(message):
    user_id = message.from_user.id
    user_data[user_id]['past_sphere'] = message.text
    
    text = f"""📬 <b>НОВАЯ АНКЕТА</b>

1️⃣ Сколько вам лет: {user_data[user_id]['age']}

2️⃣ Опыт с «лохматыми»: {user_data[user_id]['experience']}

3️⃣ Прошлая сфера: {user_data[user_id]['past_sphere']}

━━━━━━━━━━━━━━━
👤 От пользователя: @{message.from_user.username if message.from_user.username else 'нет'}
🆔 ID: {user_id}"""
    
    try:
        bot.send_message(ADMIN_ID, text, parse_mode="HTML")
        bot.send_message(message.chat.id, "✅ Спасибо! Ваша анкета отправлена.")
    except:
        bot.send_message(message.chat.id, "✅ Спасибо! Ваша анкета сохранена.")

if __name__ == "__main__":
    print("🤖 Бот запущен и работает...")
    bot.infinity_polling()