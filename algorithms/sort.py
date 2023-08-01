import csv

from cache.cache import sort_cache


def partition(nums, low, high, sort_column):
    # Выбираем средний элемент в качестве опорного
    # Также возможен выбор первого, последнего
    # или произвольного элементов в качестве опорного
    pivot = nums[(low + high) // 2][sort_column]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while float(nums[i][sort_column]) < float(pivot):
            i += 1

        j -= 1
        while float(nums[j][sort_column]) > float(pivot):
            j -= 1

        if i >= j:
            return j

        # Если элемент с индексом i (слева от опорного) больше, чем
        # элемент с индексом j (справа от опорного), меняем их местами
        nums[i], nums[j] = nums[j], nums[i]


def quick_sort(nums, sort_column):
    def _quick_sort(items, low, high, sort_column):
        if low < high:
            # This is the index after the pivot, where our lists are split
            split_index = partition(items, low, high, sort_column)
            _quick_sort(items, low, split_index, sort_column)
            _quick_sort(items, split_index + 1, high, sort_column)

    _quick_sort(nums, 0, len(nums) - 1, sort_column)

    return nums


@sort_cache
def select_sorted(sort_columns=None, limit=None, order=None, filename=None):
    with open('data/all_stocks_5yr.csv', encoding='utf-8') as file:  # Чтение файла
        read = csv.DictReader(file)
        list_data = []
        for items in read:
            if items[sort_columns[0]] != '':  # Проверка на пустые значения и добавление не пустых в список
                list_data.append(items)
        quick_sort(list_data, sort_columns[0])  # Сортировка методом "быстрой сортировки"
        if order == "desc":  # Реверсия значений по ключу high от большего к меньшему
            list_data.reverse()

    with open(f'result/{filename}', 'w', newline='') as write_file:  # Запись отсортированных данных в новый файл
        writer = csv.writer(write_file, delimiter='|')
        for item in list_data[:limit]:
            writer.writerow(item.values())

    return list_data


sort_by_price = int(
    input(f'Сортировать по цене: \nоткрытия (1) \nзакрытия (2) \nмаксимум [3] \nминимум (4) \nобъем (5)') or 3)
if sort_by_price == 1:
    column = ['open']
if sort_by_price == 2:
    column = ['close']
if sort_by_price == 3:
    column = ['high']
if sort_by_price == 4:
    column = ['low']
if sort_by_price == 5:
    column = ['volume']

oder = int(input(f'Порядок по убыванию [1] / возрастанию (2):') or 1)
if oder == 1:
    oder_direction = 'desc'
if oder == 2:
    oder_direction = 'asc'

limit_data = int(input(f'Ограничение выборки [10]:') or 10)

name_file = input(f'Название файла для сохранения результата [sort_result.csv]: ') or 'sort_result.csv'

select_sorted(sort_columns=column, order=oder_direction, limit=limit_data, filename=name_file)

if __name__ == '__main__':
    main()
