import csv

from cache.cache import search_cache


def binary_search_iterative_first(array, element, dict_key):
    '''Бинарный поиск индекса первого вхождения элемента в списке по ключу'''
    first = 0
    last = len(array)
    first_index = -1

    while (first <= last):
        mid = (first + last) // 2

        if element == array[mid][dict_key]:
            first_index = mid
            last = mid - 1  # Поиск влево (нижние индексы)

        if element < array[mid][dict_key]:
            last = mid - 1
        else:
            first = mid + 1
    return first_index


def binary_search_iterative_last(array, element, dict_key):
    '''Бинарный поиск индекса последнего вхождения элемента в списке по ключу'''
    first = 0
    last = len(array)
    last_index = -1

    while (first <= last):
        mid = (first + last) // 2

        if element == array[mid][dict_key]:
            last_index = mid
            first = mid + 1  # Поиск вправо (более высокие индексы)

        if element < array[mid][dict_key]:
            last = mid - 1
        else:
            first = mid + 1
    return last_index


def LinearSearch(array, element):  # РАБОТАЕТ Линейный поиск индекса элемента в строке по имени
    for i in range(len(array)):
        if array[i]['Name'] == element:
            return i
    return -1


@search_cache
def get_by_date(date=None, name=None, filename=None):
    with open('data/all_stocks_5yr.csv',
              encoding='utf-8') as file:  # Чтение отсортированного файла по дате (от меньшего к большему)
        read = csv.DictReader(file)
        list_data = []
        for items in read:
            list_data.append(items)

        if date == 'all':
            dict_key = 'Name'

            list_data.sort(key=lambda name: name['Name'])  # Сортируем список по имени

            index_first = binary_search_iterative_first(list_data,
                                                        name,
                                                        dict_key)  # Индекс первого вхождения в список, передаем список и имя
            index_last = binary_search_iterative_last(list_data,
                                                      name,
                                                      dict_key)  # Индекс последнего вхождения в список, передаем список и имя

            find_info = list_data[index_first:index_last]  # Выводим срез по имени и передаем в результат

        elif name == 'all':
            dict_key = 'date'

            list_data.sort(key=lambda data: data['date'])  # Сортируем список по дате

            index_first = binary_search_iterative_first(list_data,
                                                        date,
                                                        dict_key)  # Индекс первого вхождения в список, передаем список и дату
            index_last = binary_search_iterative_last(list_data,
                                                      date,
                                                      dict_key)  # Индекс последнего вхождения в список, передаем список и дату

            find_info = list_data[index_first:index_last]  # Выводим срез по дате и передаем в результат

        else:
            dict_key = 'date'

            list_data.sort(key=lambda data: data['date'])  #

            index_first = binary_search_iterative_first(list_data,
                                                        date,
                                                        dict_key)  # Индекс первого вхождения в список, передаем список и дату
            index_last = binary_search_iterative_last(list_data,
                                                      date,
                                                      dict_key)  # Индекс последнего вхождения в список, передаем список и дату

            list_with_data = list_data[index_first:index_last]  # Строка из словарей по дате из найденных индексов
            index_name = LinearSearch(list_with_data,
                                      name)  # Индекс значения по имени, передаем строку из словарей и имя

            find_info = [list_with_data[index_name]]  # Список из запрошенной даты и имени

            return find_info  # Возвращаем результат

        with open(f'result/{filename}', 'w', newline='') as write_file:  # Запись результата поиска в файл
            writer = csv.writer(write_file, delimiter='|')
            for item in find_info:
                writer.writerow(item.values())


find_data = input(f'Дата в формате yyyy-mm-dd [all]: ') or 'all'

find_name = input(f'Тикер [all]: ') or 'all'

file_name = input(f'Название файла для сохранения результата [search_results.csv]: ') or 'search_results.csv'

get_by_date(date=find_data, name=find_name, filename=file_name)

if __name__ == '__main__':
    main()
