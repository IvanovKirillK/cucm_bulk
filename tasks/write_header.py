import csv


def write_header(path, list):
    file = open(path, 'w', encoding='utf-8-sig', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(list)


def write_header_ansi(path, list):
    file = open(path, 'w', encoding='mbcs', newline='')
    writecsv = csv.writer(file, delimiter=',')
    writecsv.writerow(list)
