from tasks import get_all_ad_users, write_data_to_output

out_file = '.\\directory\\new_ad_users.txt'

with open('.\\directory\\cucm_ad_users.txt', mode='r') as txt_file:
        reader = txt_file.readlines()
        cucm_user_list = []
        for row in reader:
            cucm_user_list.append(row)

old_user_list = get_all_ad_users.get_all_ad_users()
for item in old_user_list:
    name = item.split('\t')[1].rstrip('\n')
    for item2 in cucm_user_list:
        if item2.rstrip('\n') == name:
            write_data_to_output.write_data_to_output(out_file,item.rstrip('\n'))
            print(item)

