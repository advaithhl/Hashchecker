from hashchecker.core.FileObject import FileObject
from hashchecker.io.parsing.ArgParse import ArgParse

from collections import defaultdict

def get_file_objects():
    file_list = ArgParse().args.duplicate
    if file_list:
        return (FileObject(file) for file in file_list)


def get_duplicates():
    hashdict = defaultdict(lambda:list())
    duplicates = list()
    for file_object in get_file_objects():
        md5 = file_object.md5()
        hashdict[md5].append(file_object.get_name())
    for dup_list in hashdict.values():
        if len(dup_list) != 1:
            duplicates.append(dup_list)
    return duplicates
