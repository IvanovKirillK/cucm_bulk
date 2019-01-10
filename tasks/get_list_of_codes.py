import csv


def get_list_of_codes():
    with open('.\\directory\\Kod4.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        list_codes = []
        try:
            for row in reader:
                list_codes.append(row)
        except Exception as e:
            print('Reference exception', e)
    with open('.\\directory\\Kod4.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        try:
            for row in reader:
                list_codes.append(row)
        except Exception as e:
            print('Reference exception', e)

    return list_codes
