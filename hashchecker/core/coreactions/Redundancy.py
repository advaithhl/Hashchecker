from hashchecker.core.FileObject import FileObject
from hashchecker.io.parsing.ArgParse import ArgParse

from collections import defaultdict

def get_file_objects():
    file_list = ArgParse().args.redundancy
    if file_list:
        return (FileObject(file) for file in file_list)


"""
1, 2, 3, 4, 5, 6, 7, 8
{
hashdict[135md5]:    [1, 3, 5],
hashdict[68md5] :    [6, 8],
hashdict[2md5]  :    [2],
hashdict[4md5]  :    [4],
hashdict[7md5]  :    [7]
}
"""
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


if __name__ == '__main__':
    duplicates = get_duplicates()
    for l in duplicates:
        print('Duplicates :', l)

