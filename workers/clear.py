import os


def worker():
    folder_list = ['.\\data\\', '.\\output\\']
    for folder in folder_list:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #print(file)
            except Exception as e:
                print(e)
