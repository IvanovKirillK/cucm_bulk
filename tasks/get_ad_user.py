def get_ad_user(short_number, user_list):
    ad_user = None
    user_count = 0
    found_list = []
    for user in user_list:
        temp_list = user.split('\t')
        if temp_list[0] == short_number:
            ad_user = temp_list[1].rstrip('\n')
            user_count += 1
            found_list.append(ad_user)
        else:
            continue
    if user_count == 0:
        ad_user = None
    elif user_count > 1:
        for user in found_list:
            if user[:3] == 'gpbu':
                found_list.remove(user)
        ad_user = found_list[0]
    return ad_user

