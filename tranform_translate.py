import csv
import configparser
from tasks import get_initials, get_operator_name, get_normalized_number, \
    get_list_of_codes, write_header, write_data_to_output, check_file_exists, get_list_of_group_numbers

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
dn_partition = config.get("vars", "dn_partition")
dp_prefix = config.get("vars", "dp_prefix")
pt_prefix = config.get("vars", "pt_prefix")
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")

#TODO add comments
def worker():
    count_input_transform = 0
    count_input_translate = 0
    count_non_transform = 0
    count_group_transform = 0
    count_transform = 0
    count_non_translate = 0
    count_group_translate = 0
    count_translate = 0
    filename = ".\\data\\input_data.csv"
    check_file_exists.check_file_exists(filename)
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    callingpartytransparent_header = ['PATTERN', 'ROUTE PARTITION', 'DESCRIPTION', 'NUMBERING PLAN', 'ROUTE FILTER',
                                      'URGENT PRIORITY', 'USE CALLING PARTY EXTERNAL PHONE NUMBER MASK',
                                      'DISCARD DIGIT INSTRUCTIONS', 'CALLING PARTY TRANSFORMATION MASK',
                                      'PREFIX DIGITS_OUTGOING CALLS', 'CALLING LINE ID PRESENTATION',
                                      'CALLING PARTY NUMBER TYPE', 'CALLING PARTY NUMBERING PLAN',
                                      'MLPP PREEMPTION DISABLED']

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

    output_callingpartytransparent_filepath = '.\\output\\' + 'callingpartytransparent' + '.csv'
    output_translationpattern_filepath = '.\\output\\' + 'translationpattern' + '.csv'

    write_header.write_header_ansi(output_callingpartytransparent_filepath, callingpartytransparent_header)
    write_header.write_header_ansi(output_translationpattern_filepath, translationpattern_header)

    group_list_out = get_list_of_group_numbers.get_list_of_group_numbers(filename,6)
    group_list_in = get_list_of_group_numbers.get_list_of_group_numbers(filename, 5)

    list_codes = get_list_of_codes.get_list_of_codes()

    for row in readcsv:
        if row[0] == 'name':
            continue
        out_number = get_normalized_number.get_normalized_number(row[6])
        count_input_transform += 1
        if out_number in group_list_out:
            count_group_transform += 1
            continue
        else:
            if row[6] == '':
                count_non_transform += 1
                continue
            else:
                pattern = str(row[8]) + str(row[1])
                operator_name = get_operator_name.get_operator_name(out_number, list_codes)
                for key in config['oper_partition_suffix']:
                     if key == operator_name.lower():
                         route_partition = pt_prefix + config['oper_partition_suffix'][key]
                initials = get_initials.get_initials_from_string(row[0])
                description = str(out_number) + ' /' + operator_name + ' /' + initials + ' ' + site_description
                numbering_plan = route_filter = discard_digit_instruction = 'NULL'
                urgent_priority = 't'
                use_calling_party_external_phone_number_mask = 'Off'
                calling_party_transformation_mask = out_number
                prefix_digit_outgoing_call = ''
                calling_line_in_presentation = 'Default'
                calling_party_number_type = calling_party_numbering_plan = 'Cisco CallManager'
                mlpp_presentation_enabled = 'f'
                transform_data_list = [pattern, route_partition, description, numbering_plan, route_filter,
                                       urgent_priority, use_calling_party_external_phone_number_mask,
                                       discard_digit_instruction, calling_party_transformation_mask,
                                       prefix_digit_outgoing_call, calling_line_in_presentation,
                                       calling_party_number_type, calling_party_numbering_plan,
                                       mlpp_presentation_enabled]
                write_data_to_output.write_data_to_output_ansi(output_callingpartytransparent_filepath,
                                                               transform_data_list)
                print(transform_data_list)
                count_transform += 1

    file.close()
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    for row in readcsv:
        if row[0] == 'name':
            continue
        count_input_translate += 1
        in_number = get_normalized_number.get_normalized_number(row[5])
        if in_number in group_list_in:
            count_group_translate += 1
            continue
        else:
            if row[5] == '':
                count_non_translate += 1
                continue
            else:
                operator_name = get_operator_name.get_operator_name(in_number, list_codes)
                translation_pattern = in_number
                route_partition = 'Pt_SYS_PSTN_Incoming'
                initials = get_initials.get_initials_from_string(row[0])
                description = '/' + operator_name + ' /' + str(row[8]) + str(row[1]) + ' /' + initials + ' ' \
                              + site_description
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

                write_data_to_output.write_data_to_output_ansi(output_translationpattern_filepath, translation_datalist)
                print(translation_datalist)
                count_translate += 1
    file.close()

    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input transformations records ' + str(count_input_transform))
    print('total: input translations records ' + str(count_input_translate))
    print('total: records without inbound transformations ' + str(count_non_transform))
    print('total: records without outbound translations ' + str(count_non_translate))
    print('total: records with group inbound number ' + str(count_group_transform))
    print('total: records with group outbound number ' + str(count_group_translate))
    print('result: inbound_transformations ' + str(count_transform) + ' records')
    print('result: outbound_translations ' + str(count_translate) + ' records')
    print(30 * '#')
    print('\n')
