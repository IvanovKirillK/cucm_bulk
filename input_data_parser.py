import csv
import configparser
from transliterate import translit
from tasks import check_full_name, get_initials, get_all_ad_users, get_operator_name, get_normalized_number, \
    get_list_of_codes, write_header, write_data_to_output, get_ad_user

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
dn_partition = config.get("vars", "dn_partition")
dp_prefix = config.get("vars", "dp_prefix")
pt_prefix = config.get("vars", "pt_prefix")
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")

model_list = ['7811', '7821', '8851']

#TODO add comments
def check_internal_number(number):
    try:
        if number.isdigit:
            return True
        else:
            print('Check following internal number:', number)
    except Exception as e:
        print('Check names in input data ' + e)


def check_code(code):
    try:
        if code.isdigit and (3 <= len(code) <= 4):
            return True
        else:
            print('Check following site_prefix:', code)
    except Exception as e:
        print('Check names in input data ' + e)


def worker():
    count_7811 = 0
    count_7821 = 0
    count_8851 = 0
    count_input = 0
    count_unassociated = 0
    filename = ".\\data\\input_data.csv"
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    user_list=get_all_ad_users.get_all_ad_users()

    header = ['MAC ADDRESS','DESCRIPTION','DEVICE POOL','OWNER USER ID','LINE DESCRIPTION  1',
                      'ALERTING NAME  1','ASCII ALERTING NAME  1','DIRECTORY NUMBER  1','FORWARD ALL DESTINATION  1',
                      'DISPLAY  1','ASCII DISPLAY  1','LINE TEXT LABEL  1']

    for model in model_list:
        output_filepath = '.\\output\\' + output_filename_prefix + 'phones_' + model + '.csv'
        write_header.write_header(output_filepath, header)

    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            count_input += 1
            namelist = check_full_name.check_full_name(row[0])
            check_internal_number(row[1])
            check_code(row[7])
            check_code(row[8])
            initials = get_initials.get_initials(namelist)
            mac_address=''
            description = initials + ' ' + site_description
            out_number = (get_normalized_number.get_normalized_number(row[6]))
            list_codes = get_list_of_codes.get_list_of_codes(out_number)
            operator_name = (translit(get_operator_name.get_operator_name(out_number,list_codes), 'ru', reversed=True))
            device_pool = dp_prefix + operator_name
            short_number = row[7] + row[1]
            owner_user_id = (get_ad_user.get_ad_user(short_number, user_list))
            if owner_user_id is None:
                output_filepath = '.\\output\\' + output_filename_prefix + 'unassociated_dn' + '.csv'
                write_data_to_output.write_data_to_output(output_filepath, row)
                count_unassociated += 1
                continue
            line_description=initials
            alerting_name=initials
            asci_diaplay=ascii_alerting_name=(translit(initials, 'ru', reversed=True))
            directory_number=row[8]+row[1]
            forward_all_destination='###'+row[1]
            display=initials
            line_text_label=row[1].rstrip('\n')
            output_filepath = '.\\output\\' + output_filename_prefix + 'phones_' + row[4] + '.csv'

            data_list = [mac_address, description, device_pool, owner_user_id, line_description, alerting_name,
                         ascii_alerting_name, directory_number, forward_all_destination, display, asci_diaplay,
                         line_text_label]

            write_data_to_output.write_data_to_output(output_filepath, data_list)
            print(data_list)
            if row[4] == '7811':
                count_7811 += 1
            if row[4] == '7821':
                count_7821 += 1
            if row[4] == '8851':
                count_8851 += 1

    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input ' + str(count_input) + ' records')
    print('total: 7811 ' + str(count_7811) + ' phones')
    print('total: 7821 ' + str(count_7821) + ' phones')
    print('total: 8851 ' + str(count_8851) + ' phones')
    print('total: unassociated dn ' + str(count_unassociated) + ' phones')
    print(30 * '#')
    print('\n')
