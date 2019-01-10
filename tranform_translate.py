import csv
import configparser
from transliterate import translit
from tasks import check_full_name, get_initials, get_all_ad_users, get_operator_name, get_normalized_number, \
    get_list_of_codes, write_header, write_data_to_output, get_ad_user, check_file_exists, get_list_of_group_numbers

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
dn_partition = config.get("vars", "dn_partition")
dp_prefix = config.get("vars", "dp_prefix")
pt_prefix = config.get("vars", "pt_prefix")
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")


def worker():
    count_input = 0
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

    translationpatter_header = ['TRANSLATION PATTERN', 'ROUTE PARTITION', 'DESCRIPTION', 'NUMBERING PLAN',
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
    output_translationpatter_filepath = '.\\output\\' + 'translationpatter' + '.csv'

    write_header.write_header_ansi(output_callingpartytransparent_filepath, callingpartytransparent_header)
    write_header.write_header_ansi(output_translationpatter_filepath, translationpatter_header)

    group_list = get_list_of_group_numbers.get_list_of_group_numbers(filename)

    for row in readcsv:
        if row[0] == 'name':
            continue
        out_number = get_normalized_number.get_normalized_number(row[6])
        if out_number in group_list:
            continue
        else:
            if row[6] == '':
                continue
            else:
                pattern = str(row[8]) + str(row[1])
                list_codes = get_list_of_codes.get_list_of_codes()
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
