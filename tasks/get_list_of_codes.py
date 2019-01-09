import csv


def get_list_of_codes(number):
    if number[:1] == '4':
        with open('.\\directory\\Kod4.csv', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            list_codes = []
            try:
                for row in reader:
                    list_codes.append(row)
            except Exception as e:
                print('Reference exception', e)
    if number[:1] == '8':
        with open('.\\directory\\Kod4.csv', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            list_codes = []
            try:
                for row in reader:
                    list_codes.append(row)
            except Exception as e:
                print('Reference exception', e)
    if number == '':
        list_codes = ''

    return list_codes
