import glob
import csv
import configparser
from tasks import check_file_exists, write_header, write_data_to_output, get_containing_row

# читает конфиг
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
output_filename_prefix = config.get("vars", "output_filename_prefix")


# worker - в нем делется вс работа
def worker():
    # определяем счетчики для статистики
    count_uu = 0
    count_la = 0
    count_unassociated = 0
    count_input = 0

    # проверяем наличие файлов в нужных местах
    for file in (glob.glob('.\\output\\*_phone*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\data\\*Export_phones*')):
        check_file_exists.check_file_exists(file)

    # определяем заголовок выходного файла
    update_users_header = ['USER ID', 'MANAGER USER ID', 'DEPARTMENT', 'DEFAULT PROFILE', 'USER LOCALE', 'PASSWORD',
                       'PIN', 'TELEPHONE NUMBER', 'MOBILE NUMBER', 'HOME NUMBER', 'PAGER NUMBER', 'TITLE',
                       'PRIMARY EXTENSION', 'ASSOCIATED PC', 'IPCC EXTENSION', 'MAIL ID', 'PRESENCE GROUP',
                       'SUBSCRIBE CALLING SEARCH SPACE', 'DIGEST CREDENTIALS', 'REMOTE DESTINATION LIMIT',
                       'MAXIMUM WAIT TIME FOR DESK PICKUP', 'ALLOW CONTROL OF DEVICE FROM CTI', 'ENABLE MOBILITY',
                       'ENABLE MOBILE VOICE ACCESS', 'ENABLE EMCC', 'DIRECTORY URI', 'NAME DIALING',
                       'MLPP USER IDENTIFICATION NUMBER', 'MLPP PASSWORD', 'MLPP PRECEDENCE AUTHORIZATION LEVEL',
                       'CONTROLLED DEVICE 1', 'HOME CLUSTER', 'ENABLE USER FOR UNIFIED CM IM AND PRESENCE',
                       'UC SERVICE PROFILE', 'INCLUDE MEETING INFORMATION IN PRESENCE', 'SELF-SERVICE USER ID',
                       'USER PROFILE', 'ASSIGNED PRESENCE SERVER']

    # определяем путь к выходному файлу
    update_users_filepath = '.\\output\\' + output_filename_prefix + 'Update_Users' + '.csv'

    # определяем заголовок выходного файла  line apearence
    line_appearence_header = ['User ID', 'Device', 'Directory Number', 'Partition']

    # определяем путь к выходному файлу
    line_appearence_filepath = '.\\output\\' + output_filename_prefix + 'line_appearence' + '.csv'

    # определяем путь к выходному файлу необработанных записей
    unassociated_users_filepath = '.\\output\\' + output_filename_prefix + 'unassociated_users' + '.csv'

    # создаем выходные файлы. пишем заголовка
    write_header.write_header(update_users_filepath, update_users_header)
    write_header.write_header(line_appearence_filepath, line_appearence_header)

    # определяем лист записей о телефонах (результат работы первого пункта)
    phone_list = []

    # читаем все файлы с записями о телефонах, храним лист в памяти
    for file in (glob.glob('.\\output\\*_phone*')):
        with open(file, mode='r', encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[1] == 'DESCRIPTION':
                    continue
                elif row[3] == '' or row[3] is None:
                    continue
                else:
                    phone_list.append(row)

    # откываем файл выгрузк с CUCM
    csv_file = open(glob.glob('.\\data\\*Export_phones*')[0], mode='r', encoding="utf8")
    reader = csv.reader(csv_file)

    # читаем построково файл выгрузки с CUCM
    for row in reader:
        count_input += 1
        # для каждой записи проверяем внутренний номер, если там цифры продолжаем
        if row[4].isdigit():
            # пытаемся получить запись из файла телефонов содержащую номер из файла выгрузки
            if get_containing_row.get_containing_row(phone_list, row[4]) is None:
                continue
            else:
                phone_record = get_containing_row.get_containing_row(phone_list, row[4])
                # определяем логин пользователя в ad из записи из файла телефонов
                user_id = phone_record[3]
                # определяем запись primary extension (номер + партиция)
                primary_extension = str(row[4]) + ' in ' + str(row[5])
                # получаем device_name из файла выгрузки CUCM
                device_name = row[0]

                # определяем неиспользуемые столбцы (#)
                manager_user_id = department = default_profile = user_locale = password = telephone_number = \
                    mobile_number = home_number = pager_numer = title = associated_pc = ipcc_extension = \
                    mail_id = presence_group = subscribe_calling_search_space = digest_credentials = \
                    remote_destination_limit = maximum_wait_time_for_desk_pickup = enable_mobile_voice_access = \
                    enable_emcc = directory_uri = name_dialing = mlpp_user_identification_number = mlpp_password = \
                    mlpp_precedence_authorization_level = home_cluster = enable_user_for_unified_cm_and_presence = \
                    uc_service_profile = inclume_meeting_information_in_presence = self_service_user_id = \
                    user_profile = assigned_presence_server = '#'

                # определяем константы
                allow_control_of_device_from_cti = enable_mobility = 't'

                # собираем лист для записи в файл
                update_users_datalist = [user_id, manager_user_id, department, default_profile, user_locale, password,
                       row[4], telephone_number, mobile_number, home_number, pager_numer, title,
                       primary_extension, associated_pc, ipcc_extension, mail_id, presence_group,
                       subscribe_calling_search_space, digest_credentials, remote_destination_limit,
                       maximum_wait_time_for_desk_pickup, allow_control_of_device_from_cti, enable_mobility,
                       enable_mobile_voice_access, enable_emcc, directory_uri, name_dialing,
                       mlpp_user_identification_number, mlpp_password, mlpp_precedence_authorization_level,
                       device_name, home_cluster, enable_user_for_unified_cm_and_presence,
                       uc_service_profile, inclume_meeting_information_in_presence, self_service_user_id,
                       user_profile, assigned_presence_server]

                # пишем лист в файл, увеличиваем счетчик
                write_data_to_output.write_data_to_output(update_users_filepath,update_users_datalist)
                count_uu += 1
                print(update_users_datalist)

                # собираем лист для записи line_apearance
                line_appearence_datalist = (user_id, device_name, row[4], row[5])

                # пием лист в файл, увеличиваем счетчик
                write_data_to_output.write_data_to_output(line_appearence_filepath, line_appearence_datalist)
                count_la += 1
        else:
            write_data_to_output.write_data_to_output(unassociated_users_filepath,row)
            count_unassociated += 1

    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input ' + str(count_input - 1) + ' Export Phone records')
    print('total: update_users ' + str(count_uu) + ' records')
    print('total: line_appearance ' + str(count_la) + ' records')
    print('total: unassociated_users ' + str(count_unassociated - 1) + ' records')
    print(30 * '#')
    print('\n')
