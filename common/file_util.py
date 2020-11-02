import os
import errno


def get_filepath_exist(*args):
    path = os.path.join(*args)
    if not os.path.isfile(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    return path
    
def get_filepath_noexist(*args):
    path = os.path.join(*args)
    if os.path.isfile(path):
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), path)
    return path
