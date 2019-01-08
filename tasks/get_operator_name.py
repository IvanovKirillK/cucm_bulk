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
