import csv
from tasks import check_file_exists


def get_phone_model_list(filepath):
    check_file_exists.check_file_exists(filepath)
    file = open(filepath, "r")
    readcsv = csv.reader(file, delimiter=',')
    phone_model_list = []
    for row in readcsv:
        if row[0] == 'name':
            continue
        else:
            if row[4] in phone_model_list:
                continue
            else:
                phone_model_list.append(row[4])

    file.close()
    return phone_model_list
