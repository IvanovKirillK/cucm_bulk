import distutils.dir_util
import datetime
import configparser

config = configparser.ConfigParser()
config.read(".\\data\\config.ini", encoding='utf-8')
site_description = config.get("vars", 'site_description')


def worker():
    now = datetime.datetime.now()
    for folder in ['\\output', '\\data']:
        dest = '.\\backup\\' + site_description.lstrip('\\') + '_' + now.strftime("%Y-%m-%d-%H-%M") + folder + '\\'
        distutils.dir_util.copy_tree('.' + folder, dest)

    print('\n')
    print(30 * '#')
    print('Backup is Done!')
    print(30 * '#')
