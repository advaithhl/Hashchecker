from threading import Thread

from hashchecker.io.parsing.FileObjectParser import FileObjectParser


class Calculate:
    # FIXME: sloppy code; make this independent of interface

    def __init__(self):
        self.__parsed_objs = FileObjectParser().get_file_objects()
        self.__threads = list()

    def __call_md5(self, file_object):
        print('\n\rMD5 : (calculating)', end='')
        print('\rMD5 : ' + file_object.md5(), end='')

    def __call_sha1(self, file_object):
        print('\n\rSHA 1 : (calculating)', end='')
        print('\rSHA 1 : ' + file_object.sha1(), end='')

    def __call_sha256(self, file_object):
        print('\n\rSHA 256 : (calculating)', end='')
        print('\rSHA 256 : ' + file_object.sha256(), end='')

    def __call_sha512(self, file_object):
        print('\n\rSHA 512 : (calculating)', end='')
        print('\rSHA 512 : ' + file_object.sha512(), end='')

    def calculate_all(self):
        for file_object in self.__parsed_objs:
            threads = []
            print('\n\n' + file_object.get_name())
            md5_thread = Thread(target=self.__call_md5, args=(file_object, ))
            threads.append(md5_thread)

            sha1_thread = Thread(target=self.__call_sha1, args=(file_object, ))
            threads.append(sha1_thread)

            sha256_thread = Thread(target=self.__call_sha256, args=(file_object, ))
            threads.append(sha256_thread)

            sha512_thread = Thread(target=self.__call_sha512, args=(file_object, ))
            threads.append(sha512_thread)

            for thread in threads:
                thread.start()
                thread.join()

        print('\n')
