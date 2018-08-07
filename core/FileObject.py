import hashlib
from os import path


class FileObject:

    __BLOCKSIZE = 65536

    def __init__(self, filepath):
        if path.exists(filepath):
            if path.isfile(filepath):
                self.filepath = filepath
                self.modified_time = path.getmtime(self.filepath)
            else:
                raise IsADirectoryError(filepath+' is not a file!')
        else:
            raise FileNotFoundError('File named '+filepath+' not found!')

    def get_name(self):
        return path.basename(self.filepath)

    def get_size(self):
        return path.getsize(self.filepath)

    def get_path(self):
        return self.filepath

    def md5(self):
        hasher = hashlib.md5()
        return self.__find_checksum(hasher)

    def sha1(self):
        hasher = hashlib.sha1()
        return self.__find_checksum(hasher)

    def sha256(self):
        hasher = hashlib.sha256()
        return self.__find_checksum(hasher)

    def sha512(self):
        hasher = hashlib.sha512()
        return self.__find_checksum(hasher)

    def __find_checksum(self, hasher):
        with open(self.filepath, 'rb') as file_handle:
            buffer = file_handle.read(self.__BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file_handle.read(self.__BLOCKSIZE)

        return hasher.hexdigest()
