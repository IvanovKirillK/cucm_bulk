def get_normalized_number(line):
    newline = line.replace("\t", '')
    newline = newline.replace("(", '')
    newline = newline.replace(" ", '')
    newline = newline.replace(")", '')
    newline = newline.replace("-", '')
    if len(newline) < 10:
        print('Check fmtn number', line)
    if len(newline) > 13:
        print('Check fmtn number', line)
    if newline[:2] == '+7':
        newline = '08' + newline.lstrip('+7')
    if newline[:1] == '8' and len(newline) == 11:
        newline = '0' + newline
    if newline[:1] == '7' and len(newline) == 11:
        newline = '08' + newline[1:]
    return newline
