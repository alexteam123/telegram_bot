import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# ===== ЗАМЕНИТЕ ЭТИ ДВЕ СТРОЧКИ =====
BOT_TOKEN = "8841305618:AAGAvmWazoEfLU-Mw9APHEGs-zbOp5t2qRU"
ADMIN_ID = 7686890144

# Этапы анкеты
AGE, EXPERIENCE, PAST_SPHERE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "нет юзернейма"
    user_id = user.id
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔔 <b>Кто-то нажал /start!</b>\n\n"
             f"👤 Имя: {user.first_name}\n"
             f"📱 Юзернейм: {username}\n"
             f"🆔 ID: {user_id}",
        parse_mode="HTML"
    )
    
    await update.message.reply_text(
        "📋 Здравствуйте! Ответьте на несколько вопросов.\n\n"
        "1️⃣ Сколько вам лет?",
        reply_markup=ReplyKeyboardRemove()
    )
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text
    await update.message.reply_text(
        "2️⃣ Имеете ли вы опыт работы с «лохматыми»?\n"
        "(напишите да/нет или подробно)"
    )
    return EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['experience'] = update.message.text
    await update.message.reply_text(
        "3️⃣ Какая у вас была прошлая сфера работы? (если есть)\n"
        "Если нет опыта, напишите «нет»"
    )
    return PAST_SPHERE

async def get_past_sphere(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['past_sphere'] = update.message.text
    
    text = f"""📬 <b>НОВАЯ АНКЕТА</b>

1️⃣ Сколько вам лет: {context.user_data['age']}

2️⃣ Опыт с «лохматыми»: {context.user_data['experience']}

3️⃣ Прошлая сфера: {context.user_data['past_sphere']}

━━━━━━━━━━━━━━━
👤 От пользователя: @{update.effective_user.username if update.effective_user.username else 'нет юзернейма'}
🆔 ID: {update.effective_user.id}"""
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
    
    await update.message.reply_text(
        "✅ Спасибо! Ваша анкета отправлена.\n"
        "Мы свяжемся с вами при необходимости.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Опрос отменён.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            PAST_SPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_past_sphere)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    app.add_handler(conv_handler)
    print("🤖 Бот запущен и работает...")
    app.run_polling()

if __name__ == "__main__":
    main()
