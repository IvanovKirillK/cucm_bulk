import csv
import configparser
from transliterate import translit

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')
dn_partition = config.get("vars", "dn_partition")
dp_prefix = config.get("vars", "dp_prefix")
pt_prefix = config.get("vars", "pt_prefix")
output_filename_prefix = config.get("vars", "output_filename_prefix")
default_site_operator = config.get("vars", "default_site_operator")


def check_full_name(name):
    try:
        namelist=name.split(' ')
        if len(namelist) == 3:
            return namelist
        else:
            print('Check following name:', namelist)
    except Exception as e:
        print('Check names in input data ' + e)


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


def write_output():
    name = output_filename_prefix + 'phones'+'.csv'
    filename = '.\\output\\' + name
    file = open(filename, 'w')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(['MAC ADDRESS','DESCRIPTION','DEVICE POOL','OWNER USER ID','LINE DESCRIPTION  1',
                      'ALERTING NAME  1','ASCII ALERTING NAME  1','DIRECTORY NUMBER  1','FORWARD ALL DESTINATION  1',
                      'DISPLAY  1','ASCII DISPLAY  1','LINE TEXT LABEL  1'])


def get_initials(namelist):
    if namelist[2].isdigit():
        initials = (namelist[0] + ' ' + namelist[1] + ' ' + namelist[2])
    else:
        initials = (namelist[0] + ' ' + namelist[1][:1].upper() + '.' + namelist[2][:1].upper() + '.')
    return initials


def get_normalized_number(line):
    newline = line.replace(" ", '')
    newline = line.replace("\t", '')
    newline = newline.replace("(", '')
    newline = newline.replace(" ", '')
    newline = newline.replace(")", '')
    newline = newline.replace("-", '')
    newline = newline.rstrip('\n')
    if len(newline) < 10:
        newline = ''
    if len(newline) > 13:
        newline = ''
    if newline[:2] == '+7':
        newline = newline[2:]
    if len(newline) == 11 and (newline[0] == '7' or newline[0] == '8'):
        newline = newline[1:]
    return newline


def get_operator_name(number, list_codes):
    code = (number[:3])
    num = (number[3:])
    if number == (''):
        return default_site_operator
    for i in range(0, len(list_codes)):
        temp_list = str(list_codes[i]).split(';')
        if code == (temp_list[0].lstrip("['")):
            if int(temp_list[1]) <= int(num) <= int(temp_list[2]):
                oper = temp_list[4]
                if temp_list[4] == 'ПАО "Вымпел-Коммуникации"':
                    oper = 'Билайн'
                if temp_list[4] == 'ООО "Газпром телеком"':
                    oper = 'ГазпромТелеком'
                if temp_list[4] == 'ЗАО "ГЛОБУС-ТЕЛЕКОМ"':
                    oper = 'ГлобусТелеком'
                if temp_list[4] == 'ООО "Газпром связь"':
                    oper = 'ГазпромСвязь'
                if temp_list[4] == 'ПАО "Ростелеком"':
                    oper = 'Ростелеком'
                if temp_list[4] == 'ОАО "АСВТ"':
                    oper = 'АСВТ'
                if temp_list[4] == 'ОАО "КОМКОР"':
                    oper = 'Комкор'
                if temp_list[4] == 'ОАО "Костромская городская телефонная сеть"':
                    oper = 'Костромская городская телефонная сеть'
                if temp_list[4] == 'ООО "Фрязинская Телефонная Сеть"':
                    oper = 'Фрязинская Телефонная Сеть'
                if temp_list[4] == 'АО "Квантум"':
                    oper = 'Квантум'
                if temp_list[4] == 'ООО "ПО "Тонус"':
                    oper = 'Тонус'
                return oper


def get_ad_user(short_number, user_list):
    for user in user_list:
        if user.startswith('\t') or user.startswith('\n'):
            continue
        else:
            if user.startswith(short_number):
                ad_user = user.split('\t')
                return ad_user[1].rstrip('\n')
            else:
                ad_user = None
                return ad_user


def import_data_parse():
    filename = ".\\data\\input_data.csv"
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')

    with open('.\\directory\\Kod4.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        list_codes_4 = []
        for row in reader:
            list_codes_4.append(row)

    with open('.\\directory\\Kod8.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        list_codes_8 = []
        for row in reader:
            list_codes_8.append(row)

    with open('.\\directory\\ad_users.txt', mode='r') as txt_file:
        reader = txt_file.readlines()
        user_list = []
        for row in reader:
            user_list.append(row)

    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            namelist = check_full_name(row[0])
            check_internal_number(row[1])
            check_code(row[7])
            check_code(row[8])
            description = get_initials(namelist) + ' ' + site_description
            out_number = (get_normalized_number(row[6]))
            if out_number[:1] == '4':
                list_codes = list_codes_4
            elif out_number[:1] == '8':
                list_codes = list_codes_8
            operator_name = (translit(get_operator_name(out_number,list_codes), 'ru', reversed=True))
            device_pool = dp_prefix + operator_name
            short_number = row[7] + row[1]
            print(get_ad_user(short_number, user_list))




    #write_output()
