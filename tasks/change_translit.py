def change_translit(string):
    tranlate_dict = {'ju':'yu', 'Ju':'Yu', 'yh':'ykh', 'Yh':'Ykh', 'ah':'akh', 'Ah':'Akh', 'oh':'okh', 'Oh':'Okh',
                     'ja':'ya', 'Ja':'Ya', 'aj':'ay', 'Aj':'Aj'}
    for i in tranlate_dict.keys():
        if i in string:
            string = string.replace(i, tranlate_dict[i])
    return string

