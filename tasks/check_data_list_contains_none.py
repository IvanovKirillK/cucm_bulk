def check_data_list_contains_none(list):
    for element in list:
        if element is None:
            return True


def check_data_list_contains_empty(list):
    for element in list:
        if element == '' or element == ' ':
            return True


def get_none_item(header,list):
    for element in list:
        if element is None:
            index = list.index(element)
            return header[index]

def get_empty_item(header,list):
    for element in list:
        if element == '':
            index = list.index(element)
            return header[index]
