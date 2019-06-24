def get_prefix_digit_outgoing(number, sitecode, techprefix):
    if len(number) < 4 and len(sitecode) >= 3:
        try:
            prefix_digit_outgoing = '000' + sitecode[:3] + techprefix
        except Exception as e:
            print(e)
    elif len(number) == 4 and len(sitecode) == 3:
        try:
            prefix_digit_outgoing = '000' + sitecode + techprefix
        except Exception as e:
            print(e)
    else:
        prefix_digit_outgoing = '000' + sitecode + techprefix
    return prefix_digit_outgoing