def get_ad_user(short_number, user_list):
    ad_user = None
    for user in user_list:
        temp_list = user.split('\t')
        if temp_list[0] == short_number:
            ad_user = temp_list[1].rstrip('\n')
        else:
            continue
    return ad_user
