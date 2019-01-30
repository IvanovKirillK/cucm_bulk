import configparser
import glob
from tasks import check_file_exists

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")
css = config.get("vars", "rdp_css")
forward_all_destination_prefix = config.get('vars', 'forward_all_destination_prefix')
pickup_group_start_number = config.get('vars', 'pickup_group_start_number')
use_site_prefix_in_CFA_destination = config.get('vars', 'use_site_prefix_in_CFA_destination')
analog_line_access_pt = config.get('vars', 'analog_line_access_pt')
check_inbound_group_number = config.get('vars', 'check_inbound_group_number')
check_outbound_group_number = config.get('vars', 'check_outbound_group_number')
show_line_text_label = config.get('vars', 'show_line_text_label')


def show_input_parser_submenu():
    filename = ".\\data\\input_data.csv"
    print('\n')
    print(30 * '#')
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')
    filename = ".\\directory\\ad_users.txt"
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')
    for file in glob.glob('.\\directory\\Kod*'):
        if check_file_exists.check_file_exists(file):
            print('Input: Will be working with following input file - ', file)
        else:
            print('!!!!! File - ' + filename + ' Not Found')
    print('Config options: site_description - ', site_description)
    print('Config options: output_filename_prefix - ', output_filename_prefix)
    print('Config options: default_site_operator - ', default_site_operator)
    print('Config options: forward_all_destination_prefix - ', forward_all_destination_prefix)
    print('Config options: use_site_prefix_in_CFA_destination - ', use_site_prefix_in_CFA_destination)
    print('Config options: css for forward all - ', css)
    print('Config options: show line text label - ', show_line_text_label)
    print('Output: following files will be generated - ', output_filename_prefix + ' phones_*model*.csv')
    print('Output: following files will be generated - ', output_filename_prefix + ' unassociated_dn.csv')
    selection = input("Continue? [y/n]:")
    if selection == 'y':
        return True
    if selection == 'n':
        return False
    else:
        return False


def show_update_user_submenu():
    print('\n')
    print(30 * '#')
    for file in (glob.glob('.\\data\\*Export_phones*')):
        if check_file_exists.check_file_exists(file):
            print('Input: Will be working with following input files - ', file)
        else:
            print('!!!!! File - ' + file + ' Not Found')

        for file in (glob.glob('.\\output\\*_phone*')):
            if check_file_exists.check_file_exists(file):
                print('Input: Will be working with following input files - ', file)
            else:
                print('!!!!! File - ' + file + ' Not Found')

        print('Config options: output_filename_prefix - ', output_filename_prefix)
        print('Output: following files will be generated - ',
              '.\\output\\' + output_filename_prefix + 'Update_Users' + '.csv')
        print('Output: following files will be generated - ',
              '.\\output\\' + output_filename_prefix + 'unassociated_users' + '.csv')
        selection = input("Continue? [y/n]:")
        if selection == 'y':
            return True
        if selection == 'n':
            return False
        else:
            return False


def show_RD_RDP_submenu():
    filename = ".\\data\\input_data.csv"
    print('\n')
    print(30 * '#')
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')

    for file in (glob.glob('.\\data\\*Export_phones*')):
        if check_file_exists.check_file_exists(file):
            print('Input: Will be working with following input files - ', file)
        else:
            print('!!!!! File - ' + filename + ' Not Found')

    filename = ".\\directory\\ad_users.txt"
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')

    print('Config options: site_description - ', site_description)
    print('Config options: output_filename_prefix - ', output_filename_prefix)
    print('Config options: css - ', css)
    print('Output: following files will be generated - ', '.\\output\\' + output_filename_prefix + 'RDP' + '.csv')
    print('Output: following files will be generated - ', '.\\output\\' + output_filename_prefix + 'RD' + '.csv')
    print('Output: following files will be generated - ',
          '.\\output\\' + output_filename_prefix + 'RDP_unresolved' + '.csv')
    selection = input("Continue? [y/n]:")
    if selection == 'y':
        return True
    if selection == 'n':
        return False
    else:
        return False


def show_translate_submenu():
    filename = ".\\data\\input_data.csv"
    print('\n')
    print(30 * '#')
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')
    print('Config options: site_description - ', site_description)
    print('Config options: analog_line_access_pt - ', analog_line_access_pt)
    print('Config options: check_inbound_group_number - ', check_inbound_group_number)
    print('Config options: check_outbound_group_number - ', check_outbound_group_number)
    print('Output: following files will be generated - ', '.\\output\\' + 'callingpartytransparent' + '.csv')
    print('Output: following files will be generated - ', '.\\output\\' + 'translationpattern' + '.csv')
    print('Output: following files will be generated - ', '.\\output\\' + output_filename_prefix + 'import_transform' + '.tar')
    print('Output: following files will be generated - ', '.\\output\\' + output_filename_prefix + 'import_translate' + '.tar')
    selection = input("Continue? [y/n]:")
    if selection == 'y':
        return True
    if selection == 'n':
        return False
    else:
        return False


def show_pickup_submenu():
    filename = ".\\data\\input_pickup.csv"
    print('\n')
    print(30 * '#')
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')
    filename = ".\\data\\input_data.csv"
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
    else:
        print('!!!!! File - ' + filename + ' Not Found')
    print('Config options: pickup_group_start_number - ', pickup_group_start_number)
    print('Config options: output_filename_prefix - ', output_filename_prefix)
    print('Output: following files will be generated - ', output_filename_prefix + 'pickup_group' + '.csv')
    print('Output: following files will be generated - ', output_filename_prefix + 'pickups' + '.csv')
    print('Output: following files will be generated - ', output_filename_prefix + 'unassociated_pickups' + '.csv')
    selection = input("Continue? [y/n]:")
    if selection == 'y':
        return True
    if selection == 'n':
        return False
    else:
        return False
