import hashlib
from pathlib import Path


class FileObject:

    __BLOCKSIZE = 65536

    def __init__(self, filepath):
        self.path = Path(filepath)
        if self.path.is_dir():
            raise IsADirectoryError(filepath+' is not a file!')
        elif not self.path.exists():    
            raise FileNotFoundError('File named '+filepath+' not found!')

    def get_name(self):
        return self.path.name

    def get_size(self):
        return self.path.stat().st_size

    def get_path(self):
        return self.path.absolute()

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
        with open(self.get_path(), 'rb') as file_handle:
            buffer = file_handle.read(self.__BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file_handle.read(self.__BLOCKSIZE)

        return hasher.hexdigest()

    def verify(self, checksum):
        if len(checksum) == 32:
            return self.md5() == checksum
        elif len(checksum) == 40:
            return self.sha1() == checksum
        elif len(checksum) == 64:
            return self.sha256() == checksum
        elif len(checksum) == 128:
            return self.sha512() == checksum
        else:
            return False

    def __eq__(self, other):
        return self.md5() == other.md5()

    def __str__(self):
        md5 = self.md5()
        sha1 = self.sha1()
        sha256 = self.sha256()
        sha512 = self.sha512()
        return self.get_name()+'\n\n'+'MD5    : '+md5 + \
            '\nSHA1   : '+sha1 + '\nSHA256 : '+sha256 + '\nSHA512 : '+sha512

    def __repr__(self):
        return self.get_name()

    def __hash__(self):
        return super.__hash__(self)
