import csv
import configparser

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
dn_partition = config.get("vars", "dn_partition")
dp_prefix = config.get("vars", "dp_prefix")
dp_prefix = config.get("vars", "dp_prefix")
pt_prefix = config.get("vars", "pt_prefix")
otput_filename_prefix = config.get("vars", "otput_filename_prefix")

print(site_description)

def check_full_name(name):
    try:
        namelist=name.split(' ')
        if len(namelist) == 3:
            return namelist
        else:
            print('Check names in input data')
    except Exception:
        print('Check names in input data')

def write_output():
    name = '132'
    filename = '.\\outout\\'+ name

def import_data_parse():
    filename = ".\\data\\input_data.csv"
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            namelist = check_full_name(row[0])
