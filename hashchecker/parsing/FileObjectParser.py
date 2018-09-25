from hashchecker.core.FileObject import FileObject
from hashchecker.parsing.ArgParse import parse_args


class FileObjectParser:

    def __init__(self):
        self.__args = parse_args()

    @property
    def action_name(self):
        return self.__args.main_action.name

    def __get_file_list(self):
        return self.__args.parsed_files

    def get_file_objects(self):
        return (FileObject(file) for file in self.__get_file_list())

    def get_parsed_file_name(self):
        return (file_name for file_name in self.__get_file_list())

    def get_short_file_name(self):
        return (FileObject(file).get_name() for file in self.__get_file_list())

    def get_long_file_name(self):
        return (FileObject(file).get_path() for file in self.__get_file_list())
