from collections import defaultdict

from hashchecker.core.FileObject import FileObject
from hashchecker.io.parsing.FileObjectParser import FileObjectParser


class Duplicate:
    
    def __init__(self):
        self.__parsed_objs = FileObjectParser().get_file_objects()
        self.__duplicates = list()

    def __get_same_size(self):
        size_dict = defaultdict(lambda: list())

        for file_object in self.__parsed_objs:
            size = file_object.get_size()
            size_dict[size].append(file_object)

        return size_dict

    def __find_duplicates(self, size_dict):
        hash_dict = defaultdict(lambda: list())

        for file_list in size_dict.values():
            hash_dict.clear()
            if len(file_list) > 1:
                for prob_duplicate in file_list:
                    sha1 = prob_duplicate.sha1()
                    # change prob_duplicate.get_name() 
                    # to prob_duplicate for FileObjects, if needed
                    hash_dict[sha1].append(prob_duplicate.get_name())

                for duplicates_list in hash_dict.values():
                    if len(duplicates_list) > 1:
                        self.__duplicates.append(duplicates_list)

    def get_duplicates(self):
        self.__find_duplicates(self.__get_same_size())
        return self.__duplicates
