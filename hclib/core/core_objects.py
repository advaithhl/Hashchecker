import hashlib
from os import listdir as os_listdir
from os import path as os_path
from os import walk as os_walk

from hclib.core.exceptions import IsAFileError

CHECKSUMS = [
    'md5',
    'sha1',
    'sha256',
    'sha512',
]


class FileSystemObject:
    """
    Abstract representation of a filesystem.
    The term filesystem is used to represents file or directory. Properties
    common to files and directories are defined here.
    """

    def __init__(self, fspath):
        self.fspath = fspath

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name

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

    def __eq__(self, other):
        """ Two FileSystemObjects are equal if they point to the same path """
        if isinstance(other, FileSystemObject):
            return self.path == other.path
        return False

    def __hash__(self):
        return hash(self.path)


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


class DirectoryObject(FileSystemObject):
    """
    Represents a directory of files.

    :inherits: FileSystemObject
    """

    def __init__(self, dirpath):
        super().__init__(dirpath)
        if os_path.isfile(dirpath):
            raise IsAFileError(dirpath + 'is a directory!')

    @property
    def size(self):
        """
        Return the total size (bytes) of all files in the directory.
        Courtesy: https://stackoverflow.com/a/1392549
        """
        total_size = 0
        for dpath, dnames, filenames in os_walk(self.path):
            for f in filenames:
                fp = os_path.join(dpath, f)
                # skip if it is symbolic link
                if not os_path.islink(fp):
                    total_size += os_path.getsize(fp)
        return total_size

    @property
    def empty(self):
        """ Checks whether a directory is empty. """
        return not os_listdir(self.path)

    def file_objects(self, show_hidden=False):
        """ Return FileObject generator of every file in this directory. """
        return (FileObject(os_path.join(self.path, fs_object))
                for fs_object in os_listdir(self.path)
                if os_path.isfile(os_path.join(self.path, fs_object))
                and ((not fs_object.startswith('.')) or show_hidden))

    def directory_objects(self, show_hidden=False):
        """ Return DirectoryObject generator of every subdirectory. """
        return (DirectoryObject(os_path.join(self.path, fs_object))
                for fs_object in os_listdir(self.path)
                if os_path.isdir(os_path.join(self.path, fs_object))
                and ((not fs_object.startswith('.')) or show_hidden))
