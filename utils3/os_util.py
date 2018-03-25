import os


def my_mkdir(path_string):
    """
    recursively make path
    :param path:
    :return:
    """
    base, new = os.path.split(os.path.abspath(path_string))
    if not os.path.exists(base):
        my_mkdir(base)

    if not os.path.exists(path_string):
        os.mkdir(path_string)
