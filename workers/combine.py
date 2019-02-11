import datetime
import configparser
import os
import csv
from tasks import write_header, check_empty_line, write_data_to_output

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')


def combine(filelist, model):
    # открывает файл на чтение
    file = open(filelist[0], "r", encoding="utf8")
    readcsv = csv.reader(file, delimiter=',')
    now = datetime.datetime.now()
    output_filepath = '.\\output\\' + now.strftime("%Y-%m-%d-%H-%M") + '_combined' + model + '.csv'

    for row in readcsv:
        if row[0] == '﻿MAC ADDRESS':
            header = row
            write_header.write_header(output_filepath, header)
    file.close()

    for file in filelist:
        file = open(file, "r", encoding="utf8")
        readcsv = csv.reader(file, delimiter=',')
        for row in readcsv:
            if check_empty_line.check_empty_line(row):
                continue
            elif row[0] == '﻿MAC ADDRESS':
                continue
            else:
                write_data_to_output.write_data_to_output(output_filepath, row)

    print('Done', output_filepath)


def worker():
    model_list = ['_phones_7811', '_phones_7821', '_phones_8851']
    for model in model_list:
        filelist = []
        for root, dirs, files in os.walk("combined"):
            for filename in files:
                if filename.__contains__(model):
                    path = root + '\\' + filename
                    filelist.append(path)
        if len(filelist) > 0:
            combine(filelist, model)
