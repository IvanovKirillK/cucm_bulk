import csv
import configparser
from tasks import check_file_exists, write_header, write_data_to_output, check_empty_line, get_prefix_by_number

# Определяет путь к конфиг файлу, загружает конфигурацию
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
pickup_group_start_number = config.get("vars", "pickup_group_start_number")
output_filename_prefix = config.get("vars", "output_filename_prefix")


# Основная фунекция модуля, тут происходит вызов тасков и основная работа
def worker():
    # счетчики для вывода статистики по завершению работы
    count_input_groups = 0
    count_input_numbers = 0
    count_unassociated = 0
    count_pickups = 0

    # почему-то так нужно
    pickup_group_start_number = config.get("vars", "pickup_group_start_number")

    # путь к файлу с входными данными
    filename = ".\\data\\input_pickup.csv"
    # этот файл используем для поиска нового префикса
    input_data_filename = ".\\data\\input_data.csv"

    # проверяет, существует ли файл
    check_file_exists.check_file_exists(filename)
    check_file_exists.check_file_exists(input_data_filename)

    # открываем и читаем файл входных данных в память
    input_data_list = []
    file = open(input_data_filename, "r")
    readcsv = csv.reader(file, delimiter=',')
    for row in readcsv:
        if check_empty_line.check_empty_line(row):
            continue
        elif row[0] == 'name':
            continue
        else:
            input_data_list.append(row)

    # создает выходной файл pickup групп
    group_output_filepath = '.\\output\\' + output_filename_prefix + 'pickup_group' + '.csv'
    pickup_output_filepath = '.\\output\\' + output_filename_prefix + 'pickups' + '.csv'
    unassociated_pickup_output_filepath = '.\\output\\' + output_filename_prefix + 'unassociated_pickups' + '.csv'

    # формирует заголовок выходного файла
    group_header = ['name', 'number', 'description']
    pickup_header = ['pattern', 'callpickupname']

    # пишет заголовок в выходной файл
    write_header.write_header(group_output_filepath, group_header)
    write_header.write_header(pickup_output_filepath, pickup_header)
    write_header.write_header(unassociated_pickup_output_filepath, '')

    # открывает файл на чтение
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    # для каждой записи во входном файле:
    for row in readcsv:
        if check_empty_line.check_empty_line(row):
            continue
        elif row[0] == 'HuntGroup_number':
            continue
        else:
            # увеличивает счетчик для статистики
            count_input_groups += 1
            # определяет имя pickup группы
            hg_name = pickup_group_start_number
            # опредеяет номер pickup группы
            hg_number = '**' + str(pickup_group_start_number)
            hg_description = ''
            # для всех записей в строке в файле input_pickups, начиная с 3 и до конца
            for i in range(2, len(row)-1):
                # проверяет если строка не пустая и не состоит из пробелов
                if row[i] != '' and row[i] != ' ':
                    # увеличивает счетчик для статистики
                    count_input_numbers += 1
                    # опредеяет описание pickup группы
                    hg_description = str(hg_description) + str(row[i]) + ','
                    # получает новый префмкс по короткому номеру, для проверки использует данные из файла input_data.csv
                    prefix = get_prefix_by_number.get_new_prefix(row[i], input_data_list)
                    # если префикс не найден
                    if prefix is None:
                        # пишет в лог
                        logrow = []
                        logrow.append(row)
                        logrow.append('---Number ' + row[i] + ' not found in input_data.csv')
                        count_unassociated += 1
                        write_data_to_output.write_data_to_output(unassociated_pickup_output_filepath, logrow)
                        continue
                    # если префикс найден
                    else:
                        # формирыет паттерн
                        pattern = str(prefix) + str(row[i])
                        callpickupname = hg_name
                        # формирует лист для записи в файл
                        pickup_data_list = [pattern, callpickupname]
                        # пишет в файл
                        write_data_to_output.write_data_to_output(pickup_output_filepath, pickup_data_list)
                        count_pickups += 1

            # формируем правильную строку для description
            hg_description = hg_description.rstrip(',')
            
            # формируем выходной список
            data_list = [hg_name, hg_number, hg_description]

            # увеличиваем номер pickup группы для следующей записи 
            pickup_group_start_number = int(pickup_group_start_number) + 1

            # записывает лист в выходной файл
            write_data_to_output.write_data_to_output(group_output_filepath, data_list)
            print(data_list)

    # записывает неиспользуемую строку в конец выходного файла, какие-то баги AXL или Postman
    dummy_row = ['dummy', 'dummy', 'dummy']
    write_data_to_output.write_data_to_output(group_output_filepath, dummy_row)
    write_data_to_output.write_data_to_output(pickup_output_filepath, dummy_row)


    # выводит статистику по завершении работы
    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input group ' + str(count_input_groups) + ' records')
    print('total: input numbers in groups ' + str(count_input_numbers) + ' records')
    print('total: output numbers in groups ' + str(count_pickups) + ' records')
    print('total: unassociated numbers ' + str(count_unassociated) + ' records')
    print(30 * '#')
    print('\n')
