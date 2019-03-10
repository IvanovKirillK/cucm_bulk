def change_translit(string):
    tranlate_dict = {'ju':'yu', 'yh':'ykh', 'ah':'akh', 'oh':'okh', 'ja':'ya', 'aj':'ya'}
    for i in tranlate_dict.keys():
        if i in string:
            string = string.replace(i, tranlate_dict[i])
    return string

