def check_file_exists(full_name):
    try:
        handler = open(full_name, 'r')
        handler.close()
    except FileNotFoundError as e:
        print('File ' + full_name + ' not found', e)
