import hashlib
from os import path as os_path

CHECKSUMS = (
    'MD5',
    'SHA1',
    'SHA256',
    'SHA512',
)


class FileSystemObject:
    """
    Abstract representation of a filesystem.
    The term filesystem is used to represents file or directory. Properties
    common to files and directories are defined here.
    """

    def __init__(self, fspath):
        self.fspath = fspath

    @property
    def name(self) -> str:
        """ Return the name of the filesystem """
        return os_path.basename(self.fspath)

    @property
    def path(self) -> str:
        """ Return the absolute path of the filesystem object """
        return os_path.abspath(self.fspath)

    @property
    def exists(self) -> bool:
        """ Return whether the filesystem object exists """
        return os_path.exists(self.fspath)


class FileObject(FileSystemObject):
    """
    Represents a single file.
    :inherits: FileSystemObject
    """
    _BLOCKSIZE = 65536

    def __init__(self, filepath):
        super().__init__(filepath)
        if os_path.isdir(filepath):
            raise IsADirectoryError(filepath + ' is a directory!')

    @property
    def size(self):
        """ Return the size of file in bytes """
        return os_path.getsize(self.fspath)

    def md5(self):
        """ Calculate MD5 of the file and return it """
        hasher = hashlib.md5()
        return self._find_checksum(hasher)

    def sha1(self):
        """ Calculate SHA1 of the file and return it """
        hasher = hashlib.sha1()
        return self._find_checksum(hasher)

    def sha256(self):
        """ Calculate SHA256 of the file and return it """
        hasher = hashlib.sha256()
        return self._find_checksum(hasher)

    def sha512(self):
        """ Calculate SHA512 of the file and return it """
        hasher = hashlib.sha512()
        return self._find_checksum(hasher)

    def _find_checksum(self, hasher):
        """
        Reads binary data from file and updates hash values, given a hasher.

        :params: hasher     _hashlib.HASH object to use for calculating hash.
        :returns: Hexdigest of the file represented by the object.
        """
        with open(self.fspath, 'rb') as file_handle:
            buffer = file_handle.read(self._BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file_handle.read(self._BLOCKSIZE)

        return hasher.hexdigest()
