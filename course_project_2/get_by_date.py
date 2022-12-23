import csv
import os


def cache(func):
    def wrapper(*args, **kwargs):
        cache_name = ''.join([str(i) for i in [*args]]) + ''.join([str(i) for i in kwargs.values()][:-1])
        if os.path.exists(f'cache/{cache_name}.csv'):
            with open(f'cache/{cache_name}.csv', 'r', newline='') as file:  # Открывает файл по названию
                read = csv.DictReader(file)
                result = [*read]

            with open(data/filename, 'w', newline='') as write_file:  # Передает содержимое из файла с кэшем в назначенный файл
                write_file.writelines(result)

        else:
            result = func(*args, **kwargs)

            with open(f'cache/{cache_name}.csv', 'w') as file:  # Записывает результат в кэш
                file.writelines(result)

        return result

    return wrapper


def binary_search_iterative_first_data(array,
                                       element):  # Бинарный поиск индекса первого вхождения элемента в списке по дате
    first = 0
    last = len(array)
    first_index = -1

    while (first <= last):
        mid = (first + last) // 2

        if element == array[mid]['date']:
            first_index = mid
            last = mid - 1  # Поиск влево (нижние индексы)

        if element < array[mid]['date']:
            last = mid - 1
        else:
            first = mid + 1
    return first_index


def binary_search_iterative_last_data(array,
                                      element):  # Бинарный поиск индекса последнего вхождения элемента в списке по дате
    first = 0
    last = len(array)
    last_index = -1

    while (first <= last):
        mid = (first + last) // 2

        if element == array[mid]['date']:
            last_index = mid
            first = mid + 1  # Поиск вправо (более высокие индексы)

        if element < array[mid]['date']:
            last = mid - 1
        else:
            first = mid + 1
    return last_index


def binary_search_iterative_first_name(array,
                                       element):  # Бинарный поиск индекса первого вхождения элемента в списке по имени
    first = 0
    last = len(array)
    first_index = -1

    while (first <= last):
        mid = (first + last) // 2

        if element == array[mid]['Name']:
            first_index = mid
            last = mid - 1  # Поиск влево (нижние индексы)

        if element < array[mid]['Name']:
            last = mid - 1
        else:
            first = mid + 1
    return first_index


def binary_search_iterative_last_name(array,
                                      element):  # Бинарный поиск индекса последнего вхождения элемента в списке по имени
    first = 0
    last = len(array)
    last_index = -1

    while (first <= last):
        mid = (first + last) // 2

        if element == array[mid]['Name']:
            last_index = mid
            first = mid + 1  # Поиск вправо (более высокие индексы)

        if element < array[mid]['Name']:
            last = mid - 1
        else:
            first = mid + 1
    return last_index


def LinearSearch(array, element):  # РАБОТАЕТ Линейный поиск индекса элемента в строке по имени
    for i in range(len(array)):
        if array[i]['Name'] == element:
            return i
    return -1


@cache
def get_by_date(date=None, name=None, filename=None):
    with open('data/all_stocks_5yr.csv',
              encoding='utf-8') as file:  # Чтение отсортированного файла по дате (от меньшего к большему)
        read = csv.DictReader(file)
        list_data = []
        for items in read:
            list_data.append(items)

        if date == 'all':
            list_data.sort(key=lambda name: name['Name'])  # Сортируем список по имени

            index_first = binary_search_iterative_first_name(list_data,
                                                             name)  # Индекс первого вхождения в список, передаем список и имя
            index_last = binary_search_iterative_last_name(list_data,
                                                           name)  # Индекс последнего вхождения в список, передаем список и имя

            find_info = list_data[index_first:index_last]  # Выводим срез по имени и передаем в результат

        if name == 'all':
            list_data.sort(key=lambda data: data['date'])  # Сортируем список по дате

            index_first = binary_search_iterative_first_data(list_data,
                                                             date)  # Индекс первого вхождения в список, передаем список и дату
            index_last = binary_search_iterative_last_data(list_data,
                                                           date)  # Индекс последнего вхождения в список, передаем список и дату

            find_info = list_data[index_first:index_last]  # Выводим срез по дате и передаем в результат

        else:
            list_data.sort(key=lambda data: data['date'])  #

            index_first = binary_search_iterative_first_data(list_data,
                                                             date)  # Индекс первого вхождения в список, передаем список и дату
            index_last = binary_search_iterative_last_data(list_data,
                                                           date)  # Индекс последнего вхождения в список, передаем список и дату

            list_with_data = list_data[index_first:index_last]  # Строка из словарей по дате из найденных индексов
            index_name = LinearSearch(list_with_data,
                                      name)  # Индекс значения по имени, передаем строку из словарей и имя

            find_info = list_with_data[index_name]  # Словарь из запрошенной даты и имени

        with open(data/filename, 'w', newline='') as write_file:  # Запись результата поиска в файл
            fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
            writer = csv.DictWriter(write_file, delimiter='|', fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(find_info)


find_data = input(f'Дата в формате yyyy-mm-dd [all]: ') or 'all'

find_name = input(f'Тикер [all]: ') or 'all'

file_name = input(f'Файл [dump.csv]: ') or 'dump.csv'

get_by_date(date=find_data, name=find_name, filename=file_name)

if __name__ == '__main__':
    main()
