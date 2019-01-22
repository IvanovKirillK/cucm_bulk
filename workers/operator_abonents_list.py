import csv
import configparser
from tasks import check_file_exists, get_normalized_number, get_list_of_codes, get_operator_name, check_empty_line

# читает конфиг
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')


# worker - в нем делется вся работа
def worker():
    # загружает в память список опреаторов и их кодов
    list_codes = get_list_of_codes.get_list_of_codes()

    # определяет путь к входному файлу, проеряет его наличие, открывает, потроково читает
    filename = ".\\data\\input_data.csv"
    check_file_exists.check_file_exists(filename)
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')
    op_list = []

    print('\n')
    print(30 * '#')
    print('Operators in input data: ')

    for row in readcsv:
        # проеряем строку на "пустую строку"
        if check_empty_line.check_empty_line(row):
            continue
        # проверяем строку на заголовок
        elif row[0] == 'name':
            continue
        else:
            # получаем из входного файла входящий номер
            in_number = get_normalized_number.get_normalized_number(row[5])
            # получаем из входного файла исходящий номер
            out_number = get_normalized_number.get_normalized_number(row[6])
            # получает имя опретаора по номеру телеофна, заносит в список
            in_operator = get_operator_name.get_full_operator_name(in_number, list_codes)
            # получает имя опретаора по номеру телеофна, заносит в список
            out_operator = get_operator_name.get_full_operator_name(out_number, list_codes)
            print(row[0])
            print('\t', 'in_number: ', row[5], 'in operator:', in_operator)
            print('\t', 'out_number: ', row[6], 'out operator :', out_operator)

    print(30 * '#')
    print('\n')
