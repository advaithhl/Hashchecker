import hashlib

from core.core_objects import DirectoryObject
from core.utils import BST


def calculate(file_objects, checksum):
    """
    Calculate the specified checksum of FileObjects given as a list.

    Params
    ------

    `file_objects`:  List of FileObjects whose checksum must be found.

    `checksum`:  Hash function to use for checksum calculation.
    """
    hasher = hashlib.new(checksum)
    return {
        f: f._find_checksum(hasher)
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
    hashers = {
        32: hashlib.new('md5'),
        40: hashlib.new('sha1'),
        64: hashlib.new('sha256'),
        128: hashlib.new('sha512'),
    }
    return {
        f: f._find_checksum(hashers[len(c)]) == c
        for (f, c) in zip(file_objects, correct_checksums)
    }


def find_duplicates(fs):
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

    Params
    ------

    `fs`:  A list of FileObjects OR a DirectoryObject.
    """
    if isinstance(fs, DirectoryObject):
        fs = list(fs.file_objects(show_hidden=True))

    duplicates = []
    t = BST(fs[0])
    for f in fs[1:]:
        d = t.insert(f)
        if d:
            if d[0].sha1() == d[1].sha1():
                duplicates.append(d)
    return duplicates
