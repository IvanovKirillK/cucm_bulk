import csv
import configparser
from transliterate import translit
from tasks import check_full_name, get_initials, get_all_ad_users, get_operator_name, get_normalized_number, \
    get_list_of_codes, write_header, write_data_to_output, get_ad_user, check_file_exists

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

    # for key in config['oper_partition_suffix']:
    #     print(key)
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            count_input += 1
            if row[6] == '':
                continue
            else:
                pattern = str(row[8]) + str(row[1])
                out_number = get_normalized_number.get_normalized_number(row[6])
                list_codes = get_list_of_codes.get_list_of_codes(out_number)
                operator_name = get_operator_name.get_operator_name(out_number, list_codes)
                print(operator_name.lower())
                #route_partition = pt_prefix +

