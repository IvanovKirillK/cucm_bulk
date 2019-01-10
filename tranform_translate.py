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

    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            count_input += 1
