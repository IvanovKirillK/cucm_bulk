def get_ad_user(short_number, user_list):
    ad_user = None
    user_count = 0
    for user in user_list:
        temp_list = user.split('\t')
        if temp_list[0] == short_number:
            ad_user = temp_list[1].rstrip('\n')
            user_count += 1
        else:
            continue
    if user_count != 1:
        ad_user = None

    return ad_user

