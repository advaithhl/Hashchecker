from threading import Thread

from hashchecker.parsing.ArgParse import parse_args
from hashchecker.parsing.FileObjectParser import FileObjectParser


class ChecksumResult:
    def __init__(self, file_object):
        self.file_object = file_object
        self.md5 = None
        self.sha1 = None
        self.sha256 = None
        self.sha512 = None

    def __str__(self):
        return self.file_object.get_name() + '\n' \
            + 'md5: ' + self.md5 + '\n' \
            + 'sha1: ' + self.sha1


class Calculate:

    def __init__(self):
        self.__parsed_objs = FileObjectParser().get_file_objects()
        self.__hashtypes = parse_args().hashtypes
        self.__threads = list()

    @staticmethod
    def md5(file_object, result):
        result.md5 = file_object.md5()

    @staticmethod
    def sha1(file_object, result):
        result.sha1 = file_object.sha1()

    @staticmethod
    def sha256(file_object, result):
        result.sha256 = file_object.sha256()

    @staticmethod
    def sha512(file_object, result):
        result.sha512 = file_object.sha512()

    @staticmethod
    def __add_thread(threads, hash_function, file_object, result):
        threads.append(Thread(target=hash_function, args=(file_object, result, )))

    @staticmethod
    def __start_threads(threads):
        for thread in threads:
            thread.start()

    @staticmethod
    def __join_thread(threads):
        for thread in threads:
            thread.join()

    def __calculate(self, file_object, hashtypes):
        result = ChecksumResult(file_object)
        threads = []
        for hashtype in hashtypes:
            self.__add_thread(threads, hashtype, file_object, result)

        self.__start_threads(threads)
        self.__join_thread(threads)
        return result

    def calculate(self, hashtypes):
        for file_object in self.__parsed_objs:
            yield self.__calculate(file_object, hashtypes)
