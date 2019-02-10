import csv
import configparser
import re
from transliterate import translit
from tasks import check_full_name, get_initials, get_all_ad_users, get_operator_name, get_normalized_number, \
    get_list_of_codes, write_header, write_data_to_output, get_ad_user, check_file_exists, get_pt_dp_by_operator_name, \
    check_data_list_contains_none, get_phone_model_list, check_empty_line, get_site_desc, check_input_data

# Определяет путь к конфиг файлу, загружает конфигурацию
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")
forward_all_destination_prefix = config.get('vars', 'forward_all_destination_prefix')
use_site_prefix_in_CFA_destination = config.get('vars', 'use_site_prefix_in_CFA_destination')
rdp_css = config.get('vars', 'rdp_css')
show_line_text_label = config.get('vars', 'show_line_text_label')
analog_line_access_dp = config.get('vars', 'analog_line_access_dp')
site_name = config.get('vars', 'site_name')


# Основная фунекция модуля, тут происходит вызов тасков и основная работа
def worker():

    # счетчики для вывода статистики по завершению работы
    count_7811 = 0
    count_7821 = 0
    count_8851 = 0
    count_input = 0
    count_unassociated = 0

    # путь к файлу с входными данными
    filename = ".\\data\\input_data.csv"

    # определяет лист моделей телефонов во входных данных
    model_list = get_phone_model_list.get_phone_model_list(filename)

    # проверяет, существует ли файл
    check_file_exists.check_file_exists(filename)

    # открывает файл на чтение
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    # загружает в память лист всех пользователей ad из справочника
    user_list = get_all_ad_users.get_all_ad_users()

    # формирует заголовок выходного файла
    header = ['MAC ADDRESS', 'DESCRIPTION', 'DEVICE POOL', 'OWNER USER ID', 'LINE DESCRIPTION  1',
                      'ALERTING NAME  1', 'ASCII ALERTING NAME  1', 'DIRECTORY NUMBER  1', 'FORWARD ALL DESTINATION  1',
                      'DISPLAY  1', 'ASCII DISPLAY  1', 'LINE TEXT LABEL  1', 'FORWARD ALL CSS 1',
              'SECONDARY CSS FOR FORWARD ALL 1', 'CSS']

    # создает выходные файлы для моделей телефонов, пишет заголовокв выходные файлы
    for model in model_list:
        output_filepath = '.\\output\\' + output_filename_prefix + 'phones_' + model + '.csv'
        write_header.write_header(output_filepath, header)

    # создает выходной файл неассоциированных телефонов, пишет пустой заголовок
    output_filepath = '.\\output\\' + output_filename_prefix + 'unassociated_dn' + '.csv'
    unassociated_header = ['']
    write_header.write_header(output_filepath, unassociated_header)

    # загружает в память лист кодов опретаоров связи
    list_codes = get_list_of_codes.get_list_of_codes()

    # для каждой записи во входном файле:
    for row in readcsv:
        if check_empty_line.check_empty_line(row):
            continue
        elif row[0] == 'name':
            continue
        else:
            count_input += 1

            # делит имя по пробелам на ФИО
            name = re.sub(' +', ' ', row[0].rstrip(' ').lstrip(' '))
            namelist = check_full_name.check_full_name(name)

            # проверяет input_data
            if (check_input_data.check_internal_number(row[1]) and check_input_data.check_code(row[7])
                    and check_input_data.check_code(row[8]) and check_input_data.check_model(row[4])):

                # получает инициалы из ФИО
                initials = get_initials.get_initials(namelist)

                # определяет строку для записи в файл
                mac_address = ''
                description = initials + ' ' + get_site_desc.get_site_desc(site_description) + ' ' + site_name
                out_number = (get_normalized_number.get_normalized_number(row[6]))
                operator_name = get_operator_name.get_operator_name(out_number, list_codes)

                # определяет device pool
                if row[9].isdigit():
                    device_pool = analog_line_access_dp
                else:
                    device_pool = get_pt_dp_by_operator_name.get_device_pool_by_operator_name(operator_name)

                short_number = row[7] + row[1]

                # определяет имя пользователя ad (из справочника всех пользователей)
                owner_user_id = (get_ad_user.get_ad_user(short_number, user_list))

                line_description = initials
                alerting_name = initials
                asci_diaplay = ascii_alerting_name = (translit(initials, 'ru', reversed=True))
                directory_number = row[8] + row[1]

                # формируем CFA номер
                if use_site_prefix_in_CFA_destination == 'y':
                    forward_all_destination = forward_all_destination_prefix + row[8] + str(row[1])
                if use_site_prefix_in_CFA_destination == 'n':
                    forward_all_destination = forward_all_destination_prefix + str(row[1])

                display = initials

                # проверяем надо ли показывать line text label на телефоне, формируем line_text_label
                if show_line_text_label == 'y':
                    line_text_label = row[1].rstrip('\n')
                else:
                    line_text_label = ''

                # определяет выходной файл исходя из модели телфона во входных данных
                output_filepath = '.\\output\\' + output_filename_prefix + 'phones_' + row[4] + '.csv'

                # собирает данные для записи в лист
                data_list = [mac_address, description, device_pool, owner_user_id, line_description, alerting_name,
                             ascii_alerting_name, directory_number, forward_all_destination, display, asci_diaplay,
                             line_text_label, rdp_css, rdp_css, rdp_css]

                # проверяет содерждит ли какое-либо из полей None
                if check_data_list_contains_none.check_data_list_contains_none(data_list):
                    element = check_data_list_contains_none.get_none_item(header, data_list)
                    # если пользователь ad неопределен записывает лист в выходной файл
                    if element == 'OWNER USER ID':
                        element = 'OWNER USER ID'
                    # если неопределен любой другой стобец - записывает в лог
                    else:
                        output_filepath = '.\\output\\' + output_filename_prefix + 'unassociated_dn' + '.csv'
                        write_data_to_output.write_data_to_output(output_filepath, row)
                        data_list.append('---None in datalist, ' + element + ' is None')
                        write_data_to_output.write_data_to_output(output_filepath, data_list)
                        write_data_to_output.write_data_to_output(output_filepath, '\n')
                        count_unassociated += 1
                        continue

                # записывает лист в выходной файл
                write_data_to_output.write_data_to_output(output_filepath, data_list)
                print(data_list)
                if row[4] == '7811':
                    count_7811 += 1
                if row[4] == '7821':
                    count_7821 += 1
                if row[4] == '8851':
                    count_8851 += 1

            else:
                break

    # выводит статистику по завершении работы
    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input ' + str(count_input) + ' records')
    print('total: 7811 ' + str(count_7811) + ' phones')
    print('total: 7821 ' + str(count_7821) + ' phones')
    print('total: 8851 ' + str(count_8851) + ' phones')
    print('total: ready to upload ' + str(count_7811 + count_7821 + count_8851) + ' phones')
    print('total: unassociated dn ' + str(count_unassociated) + ' phones')
    print(30 * '#')
    print('\n')
