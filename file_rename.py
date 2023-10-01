import os
import sys
path = './Cartoon/img'
# 用于给文件重命名


# 加前缀
def add_prefix(s):
    prefix = 's'
    for file_name in os.listdir(path):
        if file_name != sys.argv[0] and file_name.endswith('.jpg'):
            os.rename(os.path.join(path, file_name), os.path.join(path, prefix+file_name))


# 加后缀
def add_suffix(s):
    suffix = 's'
    for file_name in os.listdir(path):
        if file_name != sys.argv[0] and file_name.endswith('.jpg'):
            os.rename(os.path.join(path, file_name), os.path.join(path, file_name+suffix))


# 加后缀
def rename_all(s):
    new_name = 's'
    for file_name in os.listdir(path):
        if file_name != sys.argv[0] and file_name.endswith('.jpg'):
            os.rename(os.path.join(path, file_name), os.path.join(path, new_name))


if __name__ == '__main__':
    add_prefix('s')
