import configparser
config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')


def get_calling_party_tranformation_mask_by_operator(number, operator):
    if operator in config['oper_transformation_mask']:
        mask = config['oper_transformation_mask'][operator]
        if mask == 'Full':
            return number
        elif mask.isdigit():
            return number[-int(mask):]
    else:
        return number
