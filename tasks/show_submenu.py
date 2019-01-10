import configparser
import glob
from tasks import check_file_exists

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
dn_partition = config.get("vars", "dn_partition")
dp_prefix = config.get("vars", "dp_prefix")
pt_prefix = config.get("vars", "pt_prefix")
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")
css = config.get("vars", "css")


def show_input_parser_submenu():
    filename = ".\\data\\input_data.csv"
    print('\n')
    print(30 * '#')
    if check_file_exists.check_file_exists(filename):
        print('Input: Will be working with following input file - ', filename)
        filename = ".\\directory\\ad_users.txt"
        if check_file_exists.check_file_exists(filename):
            print('Input: Will be working with following input file - ', filename)
        for file in glob.glob('.\\directory\\Kod*'):
            if check_file_exists.check_file_exists(file):
                print('Input: Will be working with following input file - ', file)
        print('Config options: site_description - ', site_description)
        print('Config options: dn_partition - ', dn_partition)
        print('Config options: dp_prefix - ', dp_prefix)
        print('Config options: pt_prefix - ', pt_prefix)
        print('Config options: output_filename_prefix - ', output_filename_prefix)
        print('Config options: default_site_operator - ', default_site_operator)
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
            for file in (glob.glob('.\\output\\*_phone*')):
                if check_file_exists.check_file_exists(file):
                    print('Input: Will be working with following input files - ', file)
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
        for file in (glob.glob('.\\data\\*Export_phones*')):
            if check_file_exists.check_file_exists(file):
                print('Input: Will be working with following input files - ', file)
        filename = ".\\directory\\ad_users.txt"
        if check_file_exists.check_file_exists(filename):
            print('Input: Will be working with following input file - ', filename)
        print('Config options: site_description - ', site_description)
        print('Config options: dp_prefix - ', dp_prefix)
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
