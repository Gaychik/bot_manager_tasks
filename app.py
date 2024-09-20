from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
BOT_TOKEN='6429416800:AAGmnFMhkbD8XagsGCgIROmbM2wgwo7ApFE'

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username
    }
    response = requests.post("", json=user_data)
    if response.status_code == 201:  # 201 Created
        update.message.reply_text("Вы успешно зарегистрированы!")
    elif response.status_code == 409:  # Conflict - пользователь уже существует
        update.message.reply_text("Вы уже зарегистрированы!")
    else:
        update.message.reply_text("Произошла ошибка, попробуйте позже.")
    await update.message.reply_text('Привет! Ты мой бот. Как помогать мне будешь?')

# Функция для обработки текстовых сообщений
async def handler_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    # Вставьте свой токен
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_msg))

    # Запускаем поллинг
    application.run_polling()

if __name__ == '__main__':
    main()