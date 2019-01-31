from transliterate import translit


def get_site_desc(line):
    desc_list = line.split(' ')
    if len(desc_list) < 1:
        print('!!!!Check site description config option')
    elif len(desc_list) == 1:
        return translit(desc_list[0], 'ru', reversed=True).replace("'",'')
    elif len(desc_list) > 1:
        result = ''
        for i in range(0, len(desc_list) - 1):
            result += desc_list[i] + ' '
        return result + translit(desc_list[len(desc_list) - 1], 'ru', reversed=True).replace("'",'')
