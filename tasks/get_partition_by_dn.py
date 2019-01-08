import csv
import glob


def get_partition_by_dn(number):
    with open(glob.glob('.\\data\\*Export_phones*')[0], mode='r', encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[4] == number:
                return row[5]
