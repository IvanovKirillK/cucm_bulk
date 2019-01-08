def check_full_name(name):
    try:
        namelist=name.split(' ')
        if len(namelist) == 3:
            return namelist
        else:
            print('Check following name:', namelist)
    except Exception as e:
        print('Check names in input data ' + e)
