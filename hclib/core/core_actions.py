import hashlib
import random
import string
from collections import defaultdict
from tempfile import NamedTemporaryFile

from hclib.core.core_objects import DirectoryObject, FileObject
from hclib.core.utils import BST


def calculate(file_objects, checksum):
    """
    Calculate the specified checksum of FileObjects given as a list.

    Params
    ------

    `file_objects`:  List of FileObjects whose checksum must be found.

    `checksum`:  Hash function to use for checksum calculation.
    """
    return {
        f: f._find_checksum(hashlib.new(checksum))
        for f in file_objects
    }


def verify(file_objects, correct_checksums) -> dict:
    """
    Verify the file integrity of FileObjects given as a list.

    This is done by comparing the checksums of each FileObject and checking
    their match with the corresponding checksums provided by the second
    parameter. The given checksum is determined to belong to a certain hash
    function on the basis of their length.

    For example, a given hexdigest of a checksum of length 32 characters is of
    type MD5, as it is the only supported hash function with 32 characters.

    Params
    ------

    `file_objects`:  List of FileObjects whose checksums must be verified.

    `correct_checksums`:  List of correct/valid checksums corresponding to each
    `file_object`.
    """
    def get_hasher(l):
        if l == 32:
            return hashlib.new('md5')
        elif l == 40:
            return hashlib.new('sha1')
        elif l == 64:
            return hashlib.new('sha256')
        elif l == 128:
            return hashlib.new('sha512')
        else:
            raise ValueError('Input format does not match known checksums.')

    return {
        f: f._find_checksum(get_hasher(len(c))) == c
        for (f, c) in zip(file_objects, correct_checksums)
    }


def find_duplicates(file_objects, directory_objects):
    """
    Find duplicate files.

    A file2 is a duplicate/copy of file1 if they have the same cryptographic
    hash. However, instead of comparing hashes of each and every single file
    with each and every other file, we first compare the sizes of file1 and
    file2, i.e., the hashes (SHA1) of file1 and file2 are computed and
    calculated if and only if their file sizes are the same. This brings down
    reduntant checksum calculations to nearly none.

    For comparing the file sizes, a modified BST is used. Refer
    `core.utils.BST`.

    We add `FileObjects` from file_objects and those found by performing DFS on
    directories in direcory_objects. All files in all directories are thus added
    and compared recursively.

    Params
    ------

    `file_objects`:         A list of `FileObject`s
    `directory_objects`:    A list of `DirectoryObject`s
    """
    duplicates = defaultdict(list)
    with NamedTemporaryFile(delete=True) as dummy_file:
        t = BST(FileObject(dummy_file.name))
        for file_object in file_objects:
            d = t.insert(file_object)
            if d and not d[0].islink ^ d[1].islink:
                if d[0].sha1() == d[1].sha1():
                    duplicates[d[0]].append(d[1])

        for directory_object in directory_objects:
            for file_object in directory_object.file_objects(
                    show_hidden=True, recursive=True):
                d = t.insert(file_object)
                if d and not d[0].islink ^ d[1].islink:
                    if d[0].sha1() == d[1].sha1():
                        duplicates[d[0]].append(d[1])

    return duplicates
