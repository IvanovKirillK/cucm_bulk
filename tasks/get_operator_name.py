import configparser

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
default_site_operator = config.get("vars", "default_site_operator")


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
                if oper in config['oper_name']:
                    oper = config['oper_name'][oper]
                return oper
