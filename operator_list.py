import csv
import configparser
from tasks import check_file_exists, get_normalized_number, get_list_of_codes, get_operator_name

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')


def worker():
    list_codes = get_list_of_codes.get_list_of_codes()
    filename = ".\\data\\input_data.csv"
    check_file_exists.check_file_exists(filename)
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')
    op_list = []
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            in_number = get_normalized_number.get_normalized_number(row[5])
            out_number = get_normalized_number.get_normalized_number(row[6])
            in_operator = get_operator_name.get_full_operator_name(in_number, list_codes)
            if in_operator not in op_list:
                op_list.append(in_operator)
            out_operator = get_operator_name.get_full_operator_name(out_number, list_codes)
            if out_operator not in op_list:
                op_list.append(out_operator)

    for item in op_list:
        if item == '':
            op_list.pop(item)
        if item == 'None':
            op_list.pop(item)

    print('\n')
    print(30*'#')
    print('Operators in input data: ', op_list)

    for item in op_list:
        if item == 'None':
            continue
        if item is None:
            continue
        print('Operator - ' + item + ' :')
        if item in config['oper_name']:
            print('\t' + 'short name in config.ini - ', config['oper_name'][item])
            op_short_name = config['oper_name'][item]
        if item not in config['oper_name']:
            print('!!!!Operator is not defined in oper_name section in config.ini')

        if op_short_name in config['oper_partition_name']:
            print('\t' + 'Partition for operator in config.ini - ', config['oper_partition_name'][op_short_name])
        if op_short_name not in config['oper_partition_name']:
            print('!!!!Operator is not defined in oper_partition_name section in config.ini')

        if op_short_name in config['oper_device_pool_name']:
            print('\t' + 'Device Pool for operator in config.ini - ', config['oper_device_pool_name'][op_short_name])
        if op_short_name not in config['oper_device_pool_name']:
            print('!!!!Operator is not defined in oper_device_pool_name section in config.ini')

    print(30 * '#')
    print('\n')
