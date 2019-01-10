import csv
from tasks import check_file_exists, get_normalized_number


def get_list_of_group_numbers(filename):
    group_dict = {}
    group_list = []
    check_file_exists.check_file_exists(filename)
    file = open(filename, "r")
    readcsv = csv.reader(file, delimiter=',')
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            if get_normalized_number.get_normalized_number(row[6]) in group_dict.keys():
                group_dict[get_normalized_number.get_normalized_number(row[6])] += 1
            else:
                group_dict[get_normalized_number.get_normalized_number(row[6])] = 1

    for key in group_dict:
        if group_dict[key] == 1:
            continue
        else:
            group_list.append(key)

    return group_list
