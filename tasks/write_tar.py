import tarfile


def write_tar(tarname, file_dict):
    with tarfile.open(tarname, 'w') as tar_handler:
        for file in file_dict:
            tar_handler.add(file, arcname=file_dict[file])
    tar_handler.close()
