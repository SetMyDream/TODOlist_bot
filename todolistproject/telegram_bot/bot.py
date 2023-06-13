import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler

bot_token = '5939894637:AAFMrpkeK8uh_eKy3q6Wc2zoPHs11j2De3g'
api_url = 'http://localhost:8000/api/'

# Створення об'єкта бота
bot = Bot(token=bot_token)

# Створення об'єкта оновлювача
updater = Updater(bot=bot, use_context=True)


# Стандартний стартер бота із поясненням можливостей
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привіт! Вітаю з запуском бота TODO list!\n")
    help(update, context)



def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Основні команди:\n"
                                                                    "/create <title> <description> <due_date> - "
                                                                    "створення нового завдання. Формат дати повинен бути у формі YYYY-MM-DD.\n" +
                                                                    "/list - виведення списку всіх завдань.\n" +
                                                                    "/view <task_id> - перегляд конкретного завдання за його ідентифікатором.\n" +
                                                                    "/update <task_id> <new_title> - оновлення заголовка завдання.\n" +
                                                                    "/complete <task_id> - відмітка завдання як виконаного.\n" +
                                                                    "/delete <task_id> - видалення завдання.\n")


#Створити запис
def create(update, context):
    args = context.args
    title = args[0]
    description = ' '.join(args[1:-1])
    due_date = args[-1:]

    url = f'{api_url}tasks/'
    data = {
        'title': title,
        'description': description,
        'due_date': due_date,
        'completed': False
    }
    response = requests.post(url, data=data)

    if response.status_code == 201:
        message = 'Задача успішно створена!'
    else:
        message = 'Виникла помилка при створенні задачі.'

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Вивести всі задачі
def list_tasks(update, context):
    url = f'{api_url}tasks/'
    response = requests.get(url)
    tasks = response.json()

    if response.status_code == 200:
        message = "Список задач:\n"
        for task in tasks:
            task_id = task['id']
            title = task['title']
            message += f"- {task_id}: {title}\n"  # Виведення task_id та назви задачі
    else:
        message = 'Виникла помилка при отриманні списку задач.'

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Вивести задачу за номером
def view_task(update, context):
    task_id = context.args[0]

    url = f'{api_url}tasks/{task_id}/'
    response = requests.get(url)
    task = response.json()

    if response.status_code == 200:
        message = f"Задача {task_id}:\n"
        message += f"Заголовок: {task['title']}\n"
        message += f"Опис: {task['description']}\n"
        message += f"Дата завершення: {task['due_date']}\n"
        status = 'виконано' if task['completed'] else 'не виконано'
        message += f"Статус: {status}\n"
    else:
        message = f"Задача {task_id} не знайдена."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Оновнити назву задачі
# У задачі сказано сновити саме тайтл задачі, проте не опис чи дату. Роблю що запитано, хоча розумію можливість виконати редагування інших параметрів
def update_task(update, context):
    task_id = context.args[0]
    new_title = ' '.join(context.args[1:])

    url = f'{api_url}tasks/{task_id}/'
    data = {'title': new_title}
    response = requests.patch(url, json=data)

    if response.status_code == 200:
        message = f"Заголовок задачі {task_id} оновлено."
    else:
        message = f"Не вдалося оновити задачу {task_id}."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# позначити задачу як виконану
def complete_task(update, context):
    task_id = context.args[0]

    url = f'{api_url}tasks/{task_id}/complete/'
    response = requests.get(url)

    if response.status_code == 200:
        message = f"Задача {task_id} відмічена як виконана."
    else:
        message = f"Не вдалося відмітити задачу {task_id} як виконану."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# видалити задачу
def delete_task(update, context):
    task_id = context.args[0]

    url = f'{api_url}tasks/{task_id}/'
    response = requests.delete(url)

    if response.status_code == 204:
        message = f"Задача {task_id} видалена."
    else:
        message = f"Не вдалося видалити задачу {task_id}."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Функція заготовлена для подальшого видалення всіх елементів списку справ
def clear_all(update, context):
    url = f'{api_url}tasks/'
    response = requests.delete(url)

    if response.status_code == 204:
        message = 'Усі задачі були успішно видалені.'
    else:
        message = 'Виникла помилка при видаленні задач.'

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# функція запуску боту, із додачею обробників команд
def run_bot():
    # Створення обробників команд для оновлювача
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    create_handler = CommandHandler('create', create)
    list_handler = CommandHandler('list', list_tasks)
    view_handler = CommandHandler('view', view_task)
    update_handler = CommandHandler('update', update_task)
    complete_handler = CommandHandler('complete', complete_task)
    delete_handler = CommandHandler('delete', delete_task)
    clear_all_handler = CommandHandler('clear_all', clear_all)

    # # Налаштування пулу зв'язків
    # session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)

    # Додавання обробників до оновлювача
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(create_handler)
    updater.dispatcher.add_handler(list_handler)
    updater.dispatcher.add_handler(view_handler)
    updater.dispatcher.add_handler(update_handler)
    updater.dispatcher.add_handler(complete_handler)
    updater.dispatcher.add_handler(delete_handler)
    updater.dispatcher.add_handler(clear_all_handler)

    # Запуск бота
    updater.start_polling()

    # Зупинка бота при натисканні Ctrl + C
    updater.idle()
