import os


def make_dir_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
