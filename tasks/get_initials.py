def get_initials(namelist):
    if namelist[2].isdigit():
        initials = (namelist[0] + ' ' + namelist[1] + ' ' + namelist[2])
    else:
        initials = (namelist[0] + ' ' + namelist[1][:1].upper() + '.' + namelist[2][:1].upper() + '.')
    return initials


def get_initials_from_string(fullname):
    namelist = fullname.split(' ')
    return get_initials(namelist)
