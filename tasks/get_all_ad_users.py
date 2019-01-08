def get_all_ad_users():
    with open('.\\directory\\ad_users.txt', mode='r') as txt_file:
        reader = txt_file.readlines()
        user_list = []
        for row in reader:
            user_list.append(row)
    return user_list
