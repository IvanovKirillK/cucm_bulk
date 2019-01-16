def get_new_prefix(number, list):
    for element in list:
        if element[1] == number:
            prefix = element[8]
            return prefix
