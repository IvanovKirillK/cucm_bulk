import glob
import csv
import configparser
from transliterate import translit
from tasks import check_file_exists, check_full_name, get_initials, get_all_ad_users, get_ad_user, get_normalized_number, \
    get_list_of_codes, get_operator_name, get_partition_by_dn, write_header, write_data_to_output, \
    check_data_list_contains_none

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
output_filename_prefix = config.get("vars", "output_filename_prefix")
site_description = config.get("vars", 'site_description')
dp_prefix = config.get("vars", "dp_prefix")
css = config.get("vars", "css")


def worker():
    for file in (glob.glob('.\\data\\input_data*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\directory\\ad_users*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\data\\*Export_phones*')):
        check_file_exists.check_file_exists(file)

    user_list = get_all_ad_users.get_all_ad_users()

    header = ['REMOTE DESTINATION PROFILE NAME', 'DESCRIPTION', 'USER ID', 'DEVICE POOL', 'REROUTING CSS',
              'CSS', 'DIRECTORY NUMBER  1', 'ROUTE PARTITION  1', 'LINE DESCRIPTION  1', 'ALERTING NAME  1',
              'ASCII ALERTING NAME  1', 'DISPLAY  1', 'ASCII DISPLAY  1']

    output_filepath = '.\\output\\' + output_filename_prefix + 'RDP' + '.csv'
    output_filepath_to_check = '.\\output\\' + output_filename_prefix + 'RDP_unresolved' + '.csv'
    count_rdp = 0
    count_unresolved_rdp = 0

    write_header.write_header(output_filepath, header)

    filename = ".\\data\\input_data.csv"
    file = open(filename, 'r')
    readcsv = csv.reader(file, delimiter=',')
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            if row[2] != '' or row[3] != '':
                namelist = check_full_name.check_full_name(row[0])
                initials = get_initials.get_initials(namelist)
                if row[2] != '':
                    rdp_profile_name = 'RDP_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_dect'
                if row[3] != '':
                    rdp_profile_name = 'RDP_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_fmtn'
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
                line_description = alerting_name = display = initials
                ascii_alerting_name = ascii_display = translit(initials, 'ru', reversed=True).replace("'", '')
                data_list = [rdp_profile_name, description, user_id, device_pool, css, css, directory_number, partition,
                             line_description, alerting_name, ascii_alerting_name, display, ascii_display]

                if check_data_list_contains_none.check_data_list_contains_none(data_list):
                    write_data_to_output.write_data_to_output(output_filepath_to_check, data_list)
                    count_unresolved_rdp += 1
                    continue
                else:
                    write_data_to_output.write_data_to_output(output_filepath, data_list)
                    print(data_list)
                    count_rdp += 1
    print('\n')
    print(30 * '#')
    print('Done!, Check the output directory')
    print('total: RDP ' + str(count_rdp) + ' records')
    print('total: unresolved RDP ' + str(count_unresolved_rdp) + ' records')
    print(30 * '#')
    print('\n')
