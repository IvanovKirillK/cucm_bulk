def get_initials(namelist):
    if namelist[2].isdigit():
        initials = (namelist[0] + ' ' + namelist[1] + ' ' + namelist[2])
    else:
        initials = (namelist[0] + ' ' + namelist[1][:1].upper() + '.' + namelist[2][:1].upper() + '.')
    return initials
