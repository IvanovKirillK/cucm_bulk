import glob
import csv
import configparser
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
output_filename_prefix = config.get("vars", "output_filename_prefix")


def check_file_exists(full_name):
    try:
        handler = open(full_name, 'r')
    except FileNotFoundError as e:
        print('File ' + full_name + ' not found', e)


def get_containing_row(short_number):
    for file in (glob.glob('.\\output\\*_phone*')):
        with open(file, mode='r', encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[7] == short_number:
                    return row
                else:
                    continue


def write_unassociated_users(row):
    name = output_filename_prefix + 'unassociated_users'+'.csv'
    filename = '.\\output\\' + name
    file = open(filename, 'a', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(row)


def write_line_appearence_header():
    name = output_filename_prefix + 'line_appearence' + '.csv'
    filename = '.\\output\\' + name
    file = open(filename, 'w', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(['User ID', 'Device', 'Directory Number', 'Partition'])


def write_line_appearence(user_id, device, short_number, partition):
    name = output_filename_prefix + 'line_appearence' + '.csv'
    filename = '.\\output\\' + name
    file = open(filename, 'a', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow([user_id, device, short_number, partition])


def write_update_users_header():
    name = output_filename_prefix + 'Update_Users' + '.csv'
    filename = '.\\output\\' + name
    file = open(filename, 'w', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(['USER ID', 'MANAGER USER ID', 'DEPARTMENT', 'DEFAULT PROFILE', 'USER LOCALE', 'PASSWORD',
                       'PIN', 'TELEPHONE NUMBER', 'MOBILE NUMBER', 'HOME NUMBER', 'PAGER NUMBER', 'TITLE',
                       'PRIMARY EXTENSION', 'ASSOCIATED PC', 'IPCC EXTENSION', 'MAIL ID', 'PRESENCE GROUP',
                       'SUBSCRIBE CALLING SEARCH SPACE', 'DIGEST CREDENTIALS', 'REMOTE DESTINATION LIMIT',
                       'MAXIMUM WAIT TIME FOR DESK PICKUP', 'ALLOW CONTROL OF DEVICE FROM CTI', 'ENABLE MOBILITY',
                       'ENABLE MOBILE VOICE ACCESS', 'ENABLE EMCC', 'DIRECTORY URI', 'NAME DIALING',
                       'MLPP USER IDENTIFICATION NUMBER', 'MLPP PASSWORD', 'MLPP PRECEDENCE AUTHORIZATION LEVEL',
                       'CONTROLLED DEVICE 1', 'HOME CLUSTER', 'ENABLE USER FOR UNIFIED CM IM AND PRESENCE',
                       'UC SERVICE PROFILE', 'INCLUDE MEETING INFORMATION IN PRESENCE', 'SELF-SERVICE USER ID',
                       'USER PROFILE', 'ASSIGNED PRESENCE SERVER'])


def write_update_users(user_id, pin, title, controlled_device):
    manager_user_id = department = default_profile = user_locale = password = telephone_number = mobile_number = \
        home_number = pager_numer = primary_extension = associated_pc = ipcc_extension = mail_id = presence_group = \
        subscribe_calling_search_space = digest_credentials = remote_destination_limit = \
        maximum_wait_time_for_desk_pickup = enable_mobile_voice_access = enable_emcc = directory_uri = name_dialing = \
        mlpp_user_identification_number = mlpp_password = mlpp_precedence_authorization_level = home_cluster =\
        enable_user_for_unified_cm_and_presence = uc_service_profile = inclume_meeting_information_in_presence =\
        self_service_user_id = user_profile = assigned_presence_server = '#'

    allow_control_of_device_from_cti = enable_mobility = 't'

    name = output_filename_prefix + 'Update_Users' + '.csv'
    filename = '.\\output\\' + name
    file = open(filename, 'a', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow([user_id, manager_user_id, department, default_profile, user_locale, password,
                       pin, telephone_number, mobile_number, home_number, pager_numer, title,
                       primary_extension, associated_pc, ipcc_extension, mail_id, presence_group,
                       subscribe_calling_search_space, digest_credentials, remote_destination_limit,
                       maximum_wait_time_for_desk_pickup, allow_control_of_device_from_cti, enable_mobility,
                       enable_mobile_voice_access, enable_emcc, directory_uri, name_dialing,
                       mlpp_user_identification_number, mlpp_password, mlpp_precedence_authorization_level,
                       controlled_device, home_cluster, enable_user_for_unified_cm_and_presence,
                       uc_service_profile, inclume_meeting_information_in_presence, self_service_user_id,
                       user_profile, assigned_presence_server])
    print([user_id, manager_user_id, department, default_profile, user_locale, password,
                       pin, telephone_number, mobile_number, home_number, pager_numer, title,
                       primary_extension, associated_pc, ipcc_extension, mail_id, presence_group,
                       subscribe_calling_search_space, digest_credentials, remote_destination_limit,
                       maximum_wait_time_for_desk_pickup, allow_control_of_device_from_cti, enable_mobility,
                       enable_mobile_voice_access, enable_emcc, directory_uri, name_dialing,
                       mlpp_user_identification_number, mlpp_password, mlpp_precedence_authorization_level,
                       controlled_device, home_cluster, enable_user_for_unified_cm_and_presence,
                       uc_service_profile, inclume_meeting_information_in_presence, self_service_user_id,
                       user_profile, assigned_presence_server])


def worker():
    count_uu = 0
    count_la = 0
    count_unassociated = 0
    for file in (glob.glob('.\\output\\*_phone*')):
        check_file_exists(file)
    for file in (glob.glob('.\\data\\*Export_phones*')):
        check_file_exists(file)
    write_update_users_header()
    write_line_appearence_header()

    with open(glob.glob('.\\data\\*Export_phones*')[0], mode='r', encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[4].isdigit():
                phone_record=get_containing_row(row[4])
                user_id = phone_record[3]
                title = str(row[4]) + ' in ' + str(row[5])
                device_name = row[0]
                write_update_users(user_id, row[4], title, device_name)
                count_uu += 1
                write_line_appearence(user_id, device_name, row[4], row[5])
                count_la += 1
            else:
                write_unassociated_users(row)
                count_unassociated += 1

    print('\n')
    print(30 * '#')
    print('Done!, Check the output directory')
    print('total: update_users ' + str(count_uu) + ' records')
    print('total: line_appearance ' + str(count_la) + ' records')
    print('total: unassociated_users ' + str(count_unassociated) + ' records')
    print(30 * '#')
    print('\n')


