import csv
import os


def sort_cache(func):
    '''Функция кэширования данных сортировки. Сохраняет кэш в папку "cache"'''
    def wrapper(*args, **kwargs):
        cache_name = ''.join([str(i) for i in [*args]]) + ''.join([str(i) for i in kwargs.values()][:-1])
        cache_file = f'cache/{cache_name}.csv'

        if not os.path.exists('cache'):
            os.mkdir('cache')

        if os.path.exists(cache_file):
            print(f'Этот запрос уже был, можете посмотреть результат в папке "cache" название файла {cache_name}')
            with open(cache_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                result = [*reader]

        else:
            result = func(*args, **kwargs)

            if result is not None:
                with open(cache_file, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=result[0].keys())
                    writer.writeheader()
                    writer.writerows(result[:kwargs.get('limit')])

        return result[:kwargs.get('limit')]

    return wrapper


def search_cache(func):
    '''Функция кэширования данных поиска. Сохраняет кэш в папку "cache"'''
    def wrapper(*args, **kwargs):
        cache_name = ''.join([str(i) for i in [*args]]) + ''.join([str(i) for i in kwargs.values()][:-1])
        cache_file = f'cache/{cache_name}.csv'

        if not os.path.exists('cache'):
            os.mkdir('cache')

        if os.path.exists(cache_file):
            print(f'Этот запрос уже был, можете посмотреть результат в папке "cache" название файла {cache_name}')
            with open(cache_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                result = [*reader]

        else:
            result = func(*args, **kwargs)

            if result is not None:
                with open(cache_file, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=result[0].keys())
                    writer.writeheader()
                    writer.writerows(result)

        return result

    return wrapper
