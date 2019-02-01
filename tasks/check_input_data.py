

def check_internal_number(number):
    try:
        if number.isdigit():
            return True
        else:
            print('Check following internal number:', number)
            return False
    except Exception as e:
        print('Check data in input_data file ' + e)
        return False


# Проверяет что префикс сайта не более 4 и не менее 2 символов
def check_code(code):
    try:
        if code.isdigit() and (2 <= len(code) <= 4):
            return True
        else:
            print('Check following site_prefix:', code)
            return False
    except Exception as e:
        print('Check data in input_data file ' + e)
        return False


def check_model(model):
    try:
        if model.isdigit() and len(model) == 4:
            return True
        else:
            print('!!!! Phone model is not present !@!#!#@!#! in input_data file !!!!')
            return False
    except Exception as e:
        print('Check data in input_data file ' + str(e))
        return False
