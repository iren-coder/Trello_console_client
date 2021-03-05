import sys
import requests

# Данные авторизации в API Trello
# Необходимо заполнить свои данные key и token
# Как получить ключ и токен - читайте в README.MD

auth_params = {
    'key': "__________________",    
    'token': "__________________________________", }


# Адрес, на котором расположен API Trello, туда будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"
# Необхиодимо заполнить board_id для вашей доски
# Как получить board_id - читайте в README.MD
board_id = "_______________"


def read():
    # Обновляем счетчик задач в названии колонок
    add_counter()
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for i, task in enumerate(task_data):
            print('\t' + str(i + 1) + " - " + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if get_column_name(column['name']) == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    tasks = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                tasks.append({'id': task['id'], 'idShort': task['idShort'], 'idList': task['idList'], 'column': get_column_name(column['name'])})

    if len(tasks) > 1:
        print("Найдено несколько задач с именем \"{}\":".format(name))
        for i, task in enumerate(tasks):
            print("Порядковый номер: {}. Идентификатор - {}, расположена в колонке {}.".format(i, task['id'], task['column']))

        task_index = int(input("Введите порядковый номер задачи которую хотите перенсти в колонку \"{}\": ".format(column_name)))
        while len(tasks) - 1 < int(task_index) or int(task_index) < 0:
            task_index = int(input("Вы ввели не корректный номер задачи. Попробуйте еще раз: "))

        task_id = tasks[task_index]['id']
        task_column_name = tasks[task_index]['column']
    else:
        task_id = tasks[0]['id']
        task_column_name = tasks[0]['column']

    # Теперь у нас есть id задачи, которую мы хотим переместить.
    # Переберём данные обо всех колонках и найдём ту, в которую мы будем перемещать задачу.
    for column in column_data:
        if get_column_name(column['name']) == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            print("Задача \"{}\" с id = {} перемещена из колонки \"{}\" в колонку \"{}\".".format(name, task_id, task_column_name, column_name))
            break


# Функция добавления счетчика задач в название колонки
def add_counter():
    counter = 0
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        # Подсчитываем колличество задач в колонке
        for task in column_tasks:
            counter += 1

        # Обновляем данные с названием колонки
        if column['name'].isalpha():
            requests.put(base_url.format('lists') + '/' + column['id'],
                         data={'name': column['name'] + " " + str(counter), **auth_params})
        else:
            split_name = column['name'].split(" ")
            new_name = ""
            for item in split_name:
                if item.isalpha():
                    new_name = new_name + " " + item

            requests.put(base_url.format('lists') + '/' + column['id'],
                         data={'name': new_name[1:] + " " + str(counter), **auth_params})

        counter = 0


# Функция возвращает название колонки без счетчика задач
def get_column_name(name):
    new_name = ""
    split_name = name.split(" ")
    for item in split_name:
        if item.isalpha():
            new_name = new_name + " " + item
    return new_name[1:]


# Функция добавления новой колонки
def add_column(column_name):
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', params={'name': column_name, **auth_params})

#Функция удаления колонки
def delete_column(column_name):
    requests.delete(base_url.format('boards') + '/' + board_id + '/lists', params={'name': column_name, **auth_params})
    
#Функция удаления задачи
def delete_task(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, найдём ту колонку, которая нам нужна.
    for column in column_data:
        if get_column_name(column['name']) == column_name:
            # Удалим задачу с именем _name_ в найденной колонке
            requests.delete(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'add_column':
        add_column(sys.argv[2])
    elif sys.argv[1] == 'delete_task':
        delete_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'delete_column':
        delete_column(sys.argv[2])



