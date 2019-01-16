import input_data_parser
import update_user
import rd_rdp
import tranform_translate
import operator_list
from tasks import show_submenu, get_pt_dp_by_operator_name


menu = {}
menu['1'] = "Construct phones files."
menu['2'] = "Construct user_update and line_appearance files."
menu['3'] = "Construct RD and RDP files"
menu['4'] = "Construct translation and transformation files"
menu['5'] = "Construct pickup group files"
menu['8'] = "Show list of operators on the site"
menu['9'] = "Backup input and output files"
menu['0'] = "Exit"


while True:
    options=menu.keys()
    sorted(options)
    for entry in options:
        print(entry, menu[entry])

    selection=input("Please Select:")
    if selection == '1':
        if show_submenu.show_input_parser_submenu():
            print("Constructing phones files...")
            try:
                input_data_parser.worker()
            except Exception as e:
                print(e)

    elif selection == '2':
        if show_submenu.show_update_user_submenu():
            print("Constructing user_update and line_appearance files...")
            try:
                update_user.worker()
            except Exception as e:
                print(e)

    elif selection == '3':
        if show_submenu.show_RD_RDP_submenu():
            print("Constructing RD and RDP files...")
            try:
                rd_rdp.worker()
            except Exception as e:
                print(e)

    elif selection == '4':
        if show_submenu.show_translate_submenu():
            print("Constructing translation and transformation files...")
            try:
                tranform_translate.worker()
            except Exception as e:
                print(e)

    elif selection == '5':
        print("Constructing pickup group files...")
        print("WIP")
        get_pt_dp_by_operator_name.get_partition_by_operator_name('123')

    elif selection == '8':
        print("Building list of operators, be patient...")
        try:
            operator_list.worker()
        except Exception as e:
            print(e)

    elif selection == '9':
        print("Backup...")
        print("WIP")

    elif selection == '0':
        print("Goodbuy!")
        break
    else:
        print("Unknown Option Selected!")
        #TODO backup results and input files to archive folder
        #TODO add tests for tasks
        #TODO add tests for workers
        #TODO add travis CI pipeline
        #TODO add docker CD pipeline
        #TODO переделать логирование
