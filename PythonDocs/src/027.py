import time
import os
from contextlib import contextmanager


@contextmanager
def to_folder(path):
    oldpath = os.getcwd()
    try:
        os.chdir(path)
        yield oldpath
    finally:
        os.chdir(oldpath)


def walk(path=".", exclude=None):
    if exclude is None:
        exclude = []

    global_folders = []

    def __func(path):
        dirpath = os.getcwd()
        folders = []
        filenames = []

        to_path = os.path.join(dirpath, path)
        with to_folder(to_path):
            dirpath = os.getcwd()
            for folder_or_file in os.listdir(path):
                if folder_or_file in exclude:
                    continue
                if os.path.isdir(os.path.join(to_path, folder_or_file)):
                    folders.append(folder_or_file)
                    global_folders.append(os.path.join(to_path,
                                                       folder_or_file))
                else:
                    filenames.append(folder_or_file)
            return dirpath, folders, filenames

    yield __func(path)

    for folder in global_folders:
        yield __func(folder)


exclude = ['.git', "env", ".vscode"]

node01 = time.time()
for dirpath, folders, filenames in os.walk("."):
    # print(dirpath, folders, filenames)
    pass
node02 = time.time()
for dirpath, folders, filenames in walk(exclude=exclude):
    # print(dirpath, folders, filenames)
    pass
node03 = time.time()
print(node02-node01, node03-node02)