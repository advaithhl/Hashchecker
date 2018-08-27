from hashchecker.core.FileObject import FileObject
from hashchecker.io.parsing.FileObjectParser import FileObjectParser


class Verify:

    def __init__(self):
        self.__parsed_objs = FileObjectParser().get_file_objects()
        self.__result = dict()
        # TODO: parse checksum data from file

    def verify_all(self, hash_dict):
        """ 
        hash_dict
        key : FileObject
        value : user provided checksum
        """
        for file_object in hash_dict.keys():
            checksum = hash_dict[file_object]
            self.__result[file_object.get_name()] = file_object.verify(checksum)
        
        return self.__result
