import csv
import configparser
import distutils.file_util
import os
from tasks import get_initials, get_operator_name, get_normalized_number, \
    get_list_of_codes, write_header, write_data_to_output, check_file_exists, get_list_of_group_numbers, \
    get_pt_dp_by_operator_name, check_empty_line, get_calling_party_transformation_mask, write_tar

# читает конфиг
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
output_filename_prefix = config.get('vars', 'output_filename_prefix')
analog_line_access_pt = config.get('vars', 'analog_line_access_pt')
check_inbound_group_number = config.get('vars', 'check_inbound_group_number')
check_outbound_group_number = config.get('vars', 'check_outbound_group_number')
site_name = config.get('vars', 'site_name')

# worker - в нем делется вся работа
def worker():
    # определяем счетчики для статистики
    count_input_transform = 0
    count_input_translate = 0
    count_non_transform = 0
    count_group_transform = 0
    count_transform = 0
    count_non_translate = 0
    count_group_translate = 0
    count_translate = 0

    # определяем путь к входному файлу, открываем файл
    filename = ".\\data\\input_data.csv"
    check_file_exists.check_file_exists(filename)
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    # определяем заголовок выходного файла
    callingpartytransparent_header = ['PATTERN', 'ROUTE PARTITION', 'DESCRIPTION', 'NUMBERING PLAN', 'ROUTE FILTER',
                                      'URGENT PRIORITY', 'USE CALLING PARTY EXTERNAL PHONE NUMBER MASK',
                                      'DISCARD DIGIT INSTRUCTIONS', 'CALLING PARTY TRANSFORMATION MASK',
                                      'PREFIX DIGITS_OUTGOING CALLS', 'CALLING LINE ID PRESENTATION',
                                      'CALLING PARTY NUMBER TYPE', 'CALLING PARTY NUMBERING PLAN',
                                      'MLPP PREEMPTION DISABLED']

    # определяем заголовок выходного файла
    translationpattern_header = ['TRANSLATION PATTERN', 'ROUTE PARTITION', 'DESCRIPTION', 'NUMBERING PLAN',
                                'ROUTE FILTER', 'MLPP PRECEDENCE', 'CALLING SEARCH SPACE', 'ROUTE OPTION',
                                'OUTSIDE DIAL TONE', 'URGENT PRIORITY', 'CALLING PARTY TRANSFORMATION MASK',
                                'CALLING PARTY PREFIX DIGITS (OUTGOING CALLS)',
                                'CALLING LINE ID PRESENTATION', 'CALLING NAME PRESENTATION',
                                'CONNECTED LINE ID PRESENTATION', 'CONNECTED NAME PRESENTATION', 'DISCARD DIGITS',
                                'CALLED PARTY TRANSFORM MASK', 'CALLED PARTY PREFIX DIGITS (OUTGOING CALLS)',
                                'BLOCK THIS PATTERN OPTION', 'CALLING PARTY IE NUMBER TYPE',
                                'CALLING PARTY NUMBERING PLAN', 'CALLED PARTY IE NUMBER TYPE',
                                'CALLED PARTY NUMBERING PLAN', 'USE CALLING PARTYS EXTERNAL PHONE NUMBER MASK',
                                'RESOURCE PRIORITY NAMESPACE NETWORK DOMAIN', 'ROUTE CLASS',
                                'ROUTE NEXT HOP BY CALLING PARTY NUMBER', 'EXTERNAL CALL CONTROL PROFILE',
                                'IS AN EMERGENCY SERVICES NUMBER',
                                'DO NOT WAIT FOR INTERDIGIT TIMEOUT ON SUBSEQUENT HOPS',
                                "USE ORIGINATOR'S CALLING SEARCH SPACE"]

    # определяем путь к выходным файлам
    output_callingpartytransparent_filepath = '.\\output\\' + 'callingpartytranspattern' + '.csv'
    output_translationpattern_filepath = '.\\output\\' + 'translationpattern' + '.csv'

    # создаем выходные файлы. пишем заголовки
    write_header.write_header_ansi(output_callingpartytransparent_filepath, callingpartytransparent_header)
    write_header.write_header_ansi(output_translationpattern_filepath, translationpattern_header)

    # определяем списки входящих и исходящих групповых номеров по исходным данным
    group_list_out = get_list_of_group_numbers.get_list_of_group_numbers(filename, 6)
    group_list_in = get_list_of_group_numbers.get_list_of_group_numbers(filename, 5)

    # загружаем в память список префиксов операторов связи
    list_codes = get_list_of_codes.get_list_of_codes()

    # читаем построково исходный файл
    for row in readcsv:
        if check_empty_line.check_empty_line(row):
            continue
        elif row[0] == 'name':
            continue
        # для каждой записи получаем нормализованный исходящий номер
        out_number = get_normalized_number.get_normalized_number(row[6])
        count_input_transform += 1

        # проверяем исходящий номер на пустой номер
        if row[6] == '':
            count_non_transform += 1
            continue

        # проверяем наличие кода выхода на аналоговую линию
        if row[9] != '' and row[9].isdigit():
            print(row[9])
            # получаем имя оператора по исходящему номеру
            operator_name = get_operator_name.get_operator_name(out_number, list_codes)

            # получаем имя партиции из конфигурционного файла по имени оператора
            route_partition = analog_line_access_pt

            # определяем префикс для исходящих вызовов
            prefix_digit_outgoing_call = '000' + row[8] + row[9]

        else:
            # проверяем исходящий номер на наличие в списке групповых и флаг проверки установлен в y
            if (out_number in group_list_out and check_outbound_group_number == 'y'):
                count_group_transform += 1
                continue
            else:

                # получаем имя оператора по исходящему номеру
                operator_name = get_operator_name.get_operator_name(out_number, list_codes)

                # получаем имя партиции из конфигурционного файла по имени оператора
                route_partition = get_pt_dp_by_operator_name.get_partition_by_operator_name(operator_name)

                # определяем константы
                prefix_digit_outgoing_call = ''

        # определяем pattern как новый префикс + внутренний номер
        pattern = str(row[8]) + str(row[1])

        # получаем фамилию и инициалы
        initials = get_initials.get_initials_from_string(row[0])

        # формируем description
        description = str(out_number) + ' /' + operator_name + ' /' + initials + ' ' + site_description
        if len(description) >= 50:
            if len(str(out_number) + ' /' + operator_name + ' /' + initials + ' ' + site_name) <= 50:
                description = str(out_number) + ' /' + operator_name + ' /' + initials + ' ' + site_name
            elif len(str(out_number) + ' /' + operator_name + ' /' + initials) <= 50:
                description = str(out_number) + ' /' + operator_name + ' /' + initials
            else:
                description = str(out_number) + ' /' + operator_name

        # определяем маску по оператору (а оператора по номеру)
        calling_party_transformation_mask = \
            get_calling_party_transformation_mask.get_calling_party_tranformation_mask_by_operator(out_number,
                                                                                                   operator_name)

        # определяем константы
        numbering_plan = route_filter = discard_digit_instruction = 'NULL'
        urgent_priority = 't'
        use_calling_party_external_phone_number_mask = 'Off'
        calling_line_in_presentation = 'Default'
        calling_party_number_type = calling_party_numbering_plan = 'Cisco CallManager'
        mlpp_presentation_enabled = 'f'

        # собираем лист для записи в файл
        transform_data_list = [pattern, route_partition, description, numbering_plan, route_filter,
                               urgent_priority, use_calling_party_external_phone_number_mask,
                               discard_digit_instruction, calling_party_transformation_mask,
                               prefix_digit_outgoing_call, calling_line_in_presentation,
                               calling_party_number_type, calling_party_numbering_plan,
                               mlpp_presentation_enabled]

        # пишем лист в файл, увеличиваем счетчик
        write_data_to_output.write_data_to_output_ansi(output_callingpartytransparent_filepath,
                                                       transform_data_list)
        print(transform_data_list)
        count_transform += 1

    # закрываем файл
    file.close()

    distutils.file_util.copy_file('.\\directory\\export_transform\\header.txt', '.\\directory\\header.txt')
    file_dict = {output_callingpartytransparent_filepath: 'callingpartytranspattern' + '.csv',
                 '.\\directory\\header.txt': 'header.txt'}
    write_tar.write_tar('.\\output\\' + output_filename_prefix + 'import_transform.tar', file_dict)
    os.remove('.\\directory\\header.txt')

    # открываем исходный файл, читаем построково
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    for row in readcsv:
        if check_empty_line.check_empty_line(row):
            continue
        elif row[0] == 'name':
            continue

        # для каждой записи получаем нормализованный входящий номер
        in_number = get_normalized_number.get_normalized_number(row[5])
        count_input_translate += 1

        # проверяем входящий номер на пустой номер
        if row[5] == '':
            count_non_translate += 1
            continue

        # проверяем входящий номер на наличие в списке групповых
        elif (in_number in group_list_in and check_inbound_group_number == 'y'):
            count_group_translate += 1
            continue
        else:
            # получаем имя оператора по входящему номеру
            operator_name = get_operator_name.get_operator_name(in_number, list_codes)
            translation_pattern = in_number
            route_partition = 'Pt_SYS_PSTN_Incoming'
            initials = get_initials.get_initials_from_string(row[0])
            description = '/' + operator_name + ' /' + str(row[8]) + str(row[1]) + ' /' + initials + ' ' \
                          + site_description
            if len(description) >= 50:
                if len('/' + operator_name + ' /' + str(row[8]) + str(row[1]) + ' /' + initials + ' ' + site_name) <= 50:
                    description = '/' + operator_name + ' /' + str(row[8]) + str(row[1]) + ' /' + initials + ' ' + site_name
                elif len('/' + operator_name + ' /' + str(row[8]) + str(row[1]) + ' /' + initials) <= 50:
                    description = '/' + operator_name + ' /' + str(row[8]) + str(row[1]) + ' /' + initials
                else:
                    description = '/' + operator_name + ' /' + str(row[8]) + str(row[1])

            # определяем констнты
            numbering_plan = route_filter = calling_party_transformation_mask = discard_digits = \
                called_partty_prefix_digits = resource_priority_namespace = external_call_control_profile = ''
            mlpp_presence = calling_line_id_presentation = calling_name_presentation = \
                connected_line_id_presentation = connected_name_presentation = route_class = 'Default'
            css = 'CSS_SYS_CUCM'
            route_option = outside_dial_tone = route_next_hop = is_an_energency = do_not_wait_interdigit \
                = use_origin_css = 'f'
            urgent_priority = 't'
            calling_party_prefix_digits = '08'
            called_partty_transform_mask = str(row[8]) + str(row[1])
            block_this_patter = 'No Error'
            calling_party_ie_number_type = calling_party_numbering_plan = called_partty_ie_number = \
                called_partty_numbering_plan = 'Cisco CallManager'
            use_calling_party_external_phone_number_mask = 'Off'

            # собираем лист для записи в файл
            translation_datalist = [translation_pattern, route_partition, description, numbering_plan, route_filter,
                                    mlpp_presence, css, route_option, outside_dial_tone, urgent_priority,
                                    calling_party_transformation_mask, calling_party_prefix_digits,
                                    calling_line_id_presentation, calling_name_presentation,
                                    connected_line_id_presentation, connected_name_presentation, discard_digits,
                                    called_partty_transform_mask, called_partty_prefix_digits, block_this_patter,
                                    calling_party_ie_number_type, calling_party_numbering_plan,
                                    called_partty_ie_number, called_partty_numbering_plan,
                                    use_calling_party_external_phone_number_mask, resource_priority_namespace,
                                    route_class, route_next_hop, external_call_control_profile, is_an_energency,
                                    do_not_wait_interdigit, use_origin_css]

            # пишем лист в файл, увеличиваем счетчик
            write_data_to_output.write_data_to_output_ansi(output_translationpattern_filepath, translation_datalist)
            print(translation_datalist)
            count_translate += 1
    file.close()

    distutils.file_util.copy_file('.\\directory\\export_translate\\header.txt', '.\\directory\\header.txt')
    file_dict = {output_translationpattern_filepath: 'translationpattern' + '.csv',
                 '.\\directory\\header.txt': 'header.txt'}
    write_tar.write_tar('.\\output\\' + output_filename_prefix + 'import_translate.tar', file_dict)
    os.remove('.\\directory\\header.txt')

    # выводим статистику по результатам работы
    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: transformation records ' + str(count_input_transform))
    print('total: records WITHOUT outbound transformations ' + str(count_non_transform))
    print('total: records WITH GROUP outbound number ' + str(count_group_transform))
    print('result: outbound_transformations ' + str(count_transform) + ' records')
    print('\n')
    print('total: translation records ' + str(count_input_translate))
    print('total: records WITHOUT inbound translations ' + str(count_non_translate))
    print('total: records WITH GROUP inbound number ' + str(count_group_translate))
    print('result: inbound_translations ' + str(count_translate) + ' records')
    print(30 * '#')
    print('\n')
