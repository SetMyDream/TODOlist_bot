# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def test_script():
    import requests

    base_url = 'http://localhost:8000/api/tasks/'

    # Отримання списку всіх задач
    response = requests.get(base_url)
    print(response.json())

    # Створення нових задач
    for i in range(1, 6):
        task_data = {
            'title': f'Task {i}',
            'description': f'Description for Task {i}',
            'due_date': '2023-06-30',
            'completed': False
        }
        response = requests.post(base_url, data=task_data)
        print(response.json())

    # Отримання окремої задачі
    task_id = 2
    response = requests.get(base_url + f'{task_id}/')
    print(response.json())

    # Оновлення задачі
    task_id = 3
    updated_task_data = {
        'title': 'Updated Task 1',
        'description': 'Updated description for Task 1',
        'due_date': '2023-07-15',
        'completed': True
    }
    response = requests.put(base_url + f'{task_id}/', data=updated_task_data)
    print(response.json())

    # Видалення задачі
    response = requests.delete(base_url + f'{task_id}/')
    print(response)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # test_script()\
    import todolistproject.telegram_bot.bot as bot
    bot.run_bot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
