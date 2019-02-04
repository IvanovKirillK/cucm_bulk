from workers import input_data_parser, operator_list, pickup, rd_rdp, tranform_translate, update_user, backup, clear, \
    operator_abonents_list
from tasks import show_submenu

# определяем сисок пунктов меню
menu = {}
menu['1'] = "Construct phones files."
menu['2'] = "Construct user_update and line_appearance files."
menu['3'] = "Construct RD and RDP files"
menu['4'] = "Construct translation and transformation files"
menu['5'] = "Construct pickup group files"
menu['7'] = "Show list of phone_numbers and operator names from input data"
menu['8'] = "Show list of operators on the site"
menu['9'] = "Backup input and output files"
menu['10'] = "Clear input and output directories"
menu['0'] = "Exit"

# в цикле выводим пункты меню
while True:
    options=menu.keys()
    sorted(options)
    for entry in options:
        print(entry, menu[entry])

    selection=input("Please Select:")
    if selection == '1':
        # показываем подменю
        if show_submenu.show_input_parser_submenu():
            print("Constructing phones files...")
            try:
                # вызываем модуль для обработки данных
                input_data_parser.worker()
            except Exception as e:
                print(e)

    elif selection == '2':
        # показываем подменю
        if show_submenu.show_update_user_submenu():
            print("Constructing user_update and line_appearance files...")
            try:
                # вызываем модуль для обработки данных
                update_user.worker()
            except Exception as e:
                print(e)

    elif selection == '3':
        # показываем подменю
        if show_submenu.show_RD_RDP_submenu():
            print("Constructing RD and RDP files...")
            try:
                # вызываем модуль для обработки данных
                rd_rdp.worker()
            except Exception as e:
                print(e)

    elif selection == '4':
        # показываем подменю
        if show_submenu.show_translate_submenu():
            print("Constructing translation and transformation files...")
            try:
                # вызываем модуль для обработки данных
                tranform_translate.worker()
            except Exception as e:
                print(e)

    elif selection == '5':
        # показываем подменю
        if show_submenu.show_pickup_submenu():
            print("Constructing pickup group files...")
            try:
                # вызываем модуль для обработки данных
                pickup.worker()
            except Exception as e:
                print(e)

    elif selection == '7':
        print("Building list of phones and operators...")
        try:
            # вызываем модуль для обработки данных
            operator_abonents_list.worker()
        except Exception as e:
            print(e)

    elif selection == '8':
        print("Building list of operators, be patient...")
        try:
            # вызываем модуль для обработки данных
            operator_list.worker()
        except Exception as e:
            print(e)

    elif selection == '9':
        print("Backup...")
        try:
            # вызываем модуль для обработки данных
            backup.worker()
        except Exception as e:
            print(e)

    elif selection == '10':
        print("Clear...")
        try:
            # вызываем модуль для обработки данных
            clear.worker()
        except Exception as e:
            print(e)

    # завершает работу ПО
    elif selection == '0':
        print("Goodbye!")
        break
    else:
        print("Unknown Option Selected!")
        #TODO add tests for tasks
        #TODO add tests for workers
        #TODO add travis CI pipeline
        #TODO add docker CD pipeline
        #TODO добавить логирование


