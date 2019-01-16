import csv
import configparser
from tasks import check_file_exists, write_header, write_data_to_output

# Определяет путь к конфиг файлу, загружает конфигурацию
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
pickup_group_start_number = config.get("vars", "pickup_group_start_number")
output_filename_prefix = config.get("vars", "output_filename_prefix")


# Основная фунекция модуля, тут происходит вызов тасков и основная работа
def worker():
    # счетчики для вывода статистики по завершению работы
    count_input = 0

    # почему-то так нужно
    pickup_group_start_number = config.get("vars", "pickup_group_start_number")

    # путь к файлу с входными данными
    filename = ".\\data\\input_pickup.csv"

    # проверяет, существует ли файл
    check_file_exists.check_file_exists(filename)

    # создает выходной файл pickup групп
    output_filepath = '.\\output\\' + output_filename_prefix + 'pickup_group' + '.csv'

    # формирует заголовок выходного файла
    header = ['name', 'number', 'description']

    # пишет заголовок в выходной файл
    write_header.write_header(output_filepath, header)

    # открывает файл на чтение
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    # для каждой записи во входном файле:
    for row in readcsv:
        if row[0] == 'HuntGroup_number':
            continue
        else:
            count_input += 1
            hg_name = pickup_group_start_number
            hg_number = '**' + str(pickup_group_start_number)
            hg_description = ''
            for i in range(2, len(row)-1):
                if row[i] != '':
                    hg_description = str(hg_description) + str(row[i]) + ','

            # формируем правильную строку для description
            hg_description = '"' + hg_description.rstrip(',') + '"'
            
            # формируем выходной список
            data_list = [hg_name, hg_number, hg_description]

            # увеличиваем номер pickup группы для следующей записи 
            pickup_group_start_number = int(pickup_group_start_number) + 1

            # записывает лист в выходной файл
            write_data_to_output.write_data_to_output(output_filepath, data_list)
            print(data_list)


    # выводит статистику по завершении работы
    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input ' + str(count_input) + ' records')
    print(30 * '#')
    print('\n')

