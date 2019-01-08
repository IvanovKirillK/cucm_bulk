import glob
import csv
import configparser
from transliterate import translit
from tasks import check_file_exists, check_full_name, get_initials, get_all_ad_users, get_ad_user, get_normalized_number, \
    get_list_of_codes, get_operator_name, get_partition_by_dn

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
output_filename_prefix = config.get("vars", "output_filename_prefix")
site_description = config.get("vars", 'site_description')
dp_prefix = config.get("vars", "dp_prefix")
css = config.get("vars", "css")

# def create_rdp(row):
#
#
#
#     if row[3] != '':
#         rdp_profile_name = 'RD_' + translit(input_data_parser.get_initials(row[0]),'ru', reversed=True) + '_fmtn'

def worker():
    for file in (glob.glob('.\\data\\input_data*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\directory\\ad_users*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\data\\*Export_phones*')):
        check_file_exists.check_file_exists(file)

    user_list = get_all_ad_users.get_all_ad_users()


    filename = ".\\data\\input_data.csv"
    file = open(filename, 'r')
    readcsv = csv.reader(file, delimiter=',')
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            if row[2] != '':
                namelist = check_full_name.check_full_name(row[0])
                initials = get_initials.get_initials(namelist)
                rdp_profile_name = 'RDP_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_dect'
                rdp_profile_name = rdp_profile_name.replace("'", '')
                description = initials + u' /дект' + site_description
                short_number = row[7] + row[1]
                user_id = (get_ad_user.get_ad_user(short_number, user_list))
                out_number = (get_normalized_number.get_normalized_number(row[6]))
                list_codes = get_list_of_codes.get_list_of_codes(out_number)
                operator_name = (translit(get_operator_name.get_operator_name(out_number, list_codes), 'ru', reversed=True))
                device_pool = dp_prefix + operator_name
                directory_number = str(row[8]) + str(row[1])
                partition = get_partition_by_dn.get_partition_by_dn(directory_number)
                print(partition)

