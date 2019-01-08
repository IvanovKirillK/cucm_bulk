def get_normalized_number(line):
    newline = line.replace(" ", '')
    newline = line.replace("\t", '')
    newline = newline.replace("(", '')
    newline = newline.replace(" ", '')
    newline = newline.replace(")", '')
    newline = newline.replace("-", '')
    newline = newline.rstrip('\n')
    if len(newline) < 10:
        newline = ''
    if len(newline) > 13:
        newline = ''
    if newline[:2] == '+7':
        newline = newline[2:]
    if len(newline) == 11 and (newline[0] == '7' or newline[0] == '8'):
        newline = newline[1:]
    return newline
