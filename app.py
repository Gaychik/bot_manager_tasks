from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import requests
BOT_TOKEN='6429416800:AAGmnFMhkbD8XagsGCgIROmbM2wgwo7ApFE'
SELECTED_EMPLOYES,ASSIGN=range(2)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username
    }
    response = requests.post("http://127.0.0.1:8000/users", json=user_data)
    res= response.json()
    if res['role']=='admin':
        keyboard = [
            ['Назначить задачу - /assign']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Что будем делать?", reply_markup=reply_markup)
    else:
        keyboard = [
            ['Получить список задач']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выбери действие", reply_markup=reply_markup)


async def handle_btn_clk_assign_task(update: Update, context: CallbackContext):
    response = requests.get("http://127.0.0.1:8000/users")
    users=[user for user in response.json() if user['role']!='admin']
    selected_users=""
    for j in range(len(users)):
        selected_users+=f"id = {j+1} Имя = {users[j]['name']} Телефон = {users[j]['phone']}\n"
    await update.message.reply_text(selected_users)
    await update.message.reply_text("Выберите сотрудника для назначения задачи.\n"
                                    "Если хотите выбрать нескольких сотрудников, введите их ID через запятую!")
    await update.message.reply_text("Если хотите назначить всем задачу введите команду /all")
    return SELECTED_EMPLOYES

async def assign_task(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(context)
    selected_users_id=update.message.text.split(',')
    context.user_data['selected_users']=selected_users_id
    await update.message.reply_text("Напишите задачу: ")
    return ASSIGN

async def send_tasks_by_users(update:Update,context:ContextTypes.DEFAULT_TYPE):
    ...



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