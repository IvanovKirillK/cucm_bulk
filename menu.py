import input_data_parser
import update_user
import rd_rdp

menu = {}
menu['1']="Construct phones files."
menu['2']="Construct user_update and line_appearance files."
menu['3']="Construct RD and RDP files"
menu['4']="Construct translation and transformation files"
menu['5']="Construct pickup group files"
menu['0']="Exit"

while True:
    options=menu.keys()
    sorted(options)
    for entry in options:
      print(entry, menu[entry])

    selection=input("Please Select:")
    if selection =='1':
        print("Constructing phones files...")
        try:
            input_data_parser.import_data_parse()
        except Exception as e:
            print(e)
    elif selection == '2':
        print("Constructing user_update and line_appearance files...")
        try:
            update_user.worker()
        except Exception as e:
            print(e)
    elif selection == '3':
        print("Constructing RD and RDP files...")
        try:
            rd_rdp.worker()
        except Exception as e:
            print(e)
    elif selection == '4':
        print("Constructing translation and transformation files...")
    elif selection == '5':
        print("Constructing pickup group files...")
    elif selection == '0':
        print("Goodbuy!")
        break
    else:
        print("Unknown Option Selected!")