import csv


def write_data_to_output(path, list):
    file = open(path, 'a', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(list)
