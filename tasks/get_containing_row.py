def get_containing_row(list, short_number):
    print(list)
    print(short_number)
    for record in list:
        if record[7] == short_number:
            return record
        else:
            continue
