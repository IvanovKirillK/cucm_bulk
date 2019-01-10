import glob
import csv
import configparser
from transliterate import translit
from tasks import check_file_exists, check_full_name, get_initials, get_all_ad_users, get_ad_user, get_normalized_number, \
    get_list_of_codes, get_operator_name, get_partition_by_dn, write_header, write_data_to_output, \
    check_data_list_contains_none, get_normalized_fmtn_number

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
output_filename_prefix = config.get("vars", "output_filename_prefix")
site_description = config.get("vars", 'site_description')
dp_prefix = config.get("vars", "dp_prefix")
css = config.get("vars", "css")

#TODO add comments
def worker():
    for file in (glob.glob('.\\data\\input_data*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\directory\\ad_users*')):
        check_file_exists.check_file_exists(file)
    for file in (glob.glob('.\\data\\*Export_phones*')):
        check_file_exists.check_file_exists(file)

    user_list = get_all_ad_users.get_all_ad_users()

    rdp_header = ['REMOTE DESTINATION PROFILE NAME', 'DESCRIPTION', 'USER ID', 'DEVICE POOL', 'REROUTING CSS',
              'CSS', 'DIRECTORY NUMBER  1', 'ROUTE PARTITION  1', 'LINE DESCRIPTION  1', 'ALERTING NAME  1',
              'ASCII ALERTING NAME  1', 'DISPLAY  1', 'ASCII DISPLAY  1']

    rd_header = ['NAME', 'REMOTE DESTINATION PROFILE', 'TIME ZONE', 'DUAL MODE DEVICE', 'MOBILE SMART CLIENT',
                 'CTI REMOTE DEVICE', 'DESTINATION', 'ANSWER TOO SOON TIMER', 'ANSWER TOO LATE TIMER',
                 'DELAY BEFORE RINGING TIMER', 'IS MOBILE PHONE', 'ENABLE MOBILE CONNECT 1', 'DAY OF WEEK 1',
                 'START TIME 1', 'END TIME 1', 'DAY OF WEEK 2', 'START TIME 2', 'END TIME 2', 'DAY OF WEEK 3',
                 'START TIME 3', 'END TIME 3', 'DAY OF WEEK 4', 'START TIME 4', 'END TIME 4', 'DAY OF WEEK 5',
                 'START TIME 5', 'END TIME 5', 'DAY OF WEEK 6', 'START TIME 6', 'END TIME 6', 'DAY OF WEEK 7',
                 'START TIME 7', 'END TIME 7', 'ACCESS LIST 1', 'ASSOCIATED LINE NUMBER 1', 'ROUTE PARTITION 1',
                 'MOBILITY PROFILE', 'SINGLE NUMBER REACH VOICEMAIL POLICY', 'DIAL-VIA-OFFICE REVERSE VOICEMAIL POLICY']

    output_rdp_filepath = '.\\output\\' + output_filename_prefix + 'RDP' + '.csv'
    output_rd_filepath = '.\\output\\' + output_filename_prefix + 'RD' + '.csv'
    output_filepath_to_check = '.\\output\\' + output_filename_prefix + 'RDP_unresolved' + '.csv'
    count_input = 0
    count_rdp = 0
    count_rd = 0
    count_unresolved_rdp = 0

    write_header.write_header(output_rdp_filepath, rdp_header)
    write_header.write_header(output_rd_filepath, rd_header)

    filename = ".\\data\\input_data.csv"
    file = open(filename, 'r')
    readcsv = csv.reader(file, delimiter=',')
    list_codes = get_list_of_codes.get_list_of_codes()
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            if row[2] != '' or row[3] != '':
                namelist = check_full_name.check_full_name(row[0])
                initials = get_initials.get_initials(namelist)
                if row[2] != '':
                    rdp_profile_name = 'RDP_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_dect'
                    rd_name = 'RD_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_dect'
                    destination = row[2]
                    count_input += 1
                if row[3] != '':
                    rdp_profile_name = 'RDP_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_fmtn'
                    rd_name = 'RD_' + translit(initials.replace(" ", ""), 'ru', reversed=True) + '_fmtn'
                    destination = get_normalized_fmtn_number.get_normalized_number(row[3])
                    count_input += 1

                rdp_profile_name = rdp_profile_name.replace("'", '')
                description = initials + u' /дект' + site_description
                short_number = row[7] + row[1]
                user_id = (get_ad_user.get_ad_user(short_number, user_list))
                out_number = (get_normalized_number.get_normalized_number(row[6]))
                #list_codes = get_list_of_codes.get_list_of_codes(out_number)
                operator_name = (translit(get_operator_name.get_operator_name(out_number, list_codes), 'ru', reversed=True))
                device_pool = dp_prefix + operator_name
                directory_number = str(row[8]) + str(row[1])
                partition = get_partition_by_dn.get_partition_by_dn(directory_number)
                line_description = alerting_name = display = initials
                ascii_alerting_name = ascii_display = translit(initials, 'ru', reversed=True).replace("'", '')
                rdp_data_list = [rdp_profile_name, description, user_id, device_pool, css, css, directory_number, partition,
                             line_description, alerting_name, ascii_alerting_name, display, ascii_display]

                if check_data_list_contains_none.check_data_list_contains_none(rdp_data_list):
                    write_data_to_output.write_data_to_output(output_filepath_to_check, rdp_data_list)
                    count_unresolved_rdp += 1
                    continue
                else:
                    write_data_to_output.write_data_to_output(output_rdp_filepath, rdp_data_list)
                    print(rdp_data_list)
                    count_rdp += 1

                time_zone = 'Etc/GMT'
                dual_mode_device = mobile_smart_client = cti_remote_device = day_of_week = start_time = end_time = \
                    mobility_profile = access_list = ''
                answer_too_soon_timer = '1500'
                answer_too_late_timer = '19000'
                delay_before_ringing_timer = '0'
                is_mobile_phone = enable_mobile_connect = 't'
                associated_line_number = str(row[8]) + str(row[1])
                single_number_reach_voicemail_policy = dial_via_office = 'Use System Default'

                rd_data_list = [rd_name, rdp_profile_name, time_zone, dual_mode_device, mobile_smart_client,
                                cti_remote_device, destination, answer_too_soon_timer, answer_too_late_timer,
                                delay_before_ringing_timer, is_mobile_phone, enable_mobile_connect, day_of_week,
                                start_time, end_time, day_of_week, start_time, end_time, day_of_week, start_time,
                                end_time, day_of_week, start_time, end_time, day_of_week, start_time, end_time,
                                day_of_week, start_time, end_time, day_of_week, start_time, end_time, access_list,
                                associated_line_number, partition, mobility_profile,
                                single_number_reach_voicemail_policy, dial_via_office]

                write_data_to_output.write_data_to_output(output_rd_filepath, rd_data_list)
                count_rd += 1
                print(rd_data_list)

    print('\n')
    print(30 * '#')
    print('Done! Check the output directory')
    print('total: input RD ' + str(count_input) + ' records')
    print('total: RDP ' + str(count_rdp) + ' records')
    print('total: RD ' + str(count_rd) + ' records')
    print('total: unresolved RDP ' + str(count_unresolved_rdp) + ' records')
    print(30 * '#')
    print('\n')
