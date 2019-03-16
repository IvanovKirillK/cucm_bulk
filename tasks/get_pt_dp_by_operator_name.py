import configparser

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')


def get_partition_by_operator_name(name):
    if name in config['oper_partition_name']:
        return config['oper_partition_name'][name]
    else:
        return None


def get_device_pool_by_operator_name(name):
    if name in config['oper_device_pool_name']:
        return config['oper_device_pool_name'][name]
    else:
        return None


def get_device_pool_by_analog_prefix(name):
    if name in config['oper_analog_device_pool_name']:
        return config['oper_analog_device_pool_name'][name]
    else:
        return None