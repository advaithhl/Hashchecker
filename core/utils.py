class BST:
    """ 
    A Binary Search Tree (BST) which is used to find duplicates.

    Each node of the BST holds FileObjects (refer
    `core.core_objects.FileObject`). Each node to the left of a node holds
    FileObjects which are having lower sizes than it. Insertion into the BST
    happens just like any other BST, but the values compared are the file sizes
    of the FileObjects.

    If we try to insert a node with a FileObject which has the same size as the
    FileObjects represented by any of the nodes, the insert method does not add
    anything new to the BST, but rather returns a list of 2 elements, viz., the
    FileObject instance of the conflicting node and the FileObject instance that
    we were trying to insert into the BST.
    """

    def __init__(self, file_object):
        self._file_object = file_object
        self._left = None
        self._right = None

    def insert(self, file_object):
        if self._file_object:
            if file_object.size < self._file_object.size:
                if self._left:
                    return self._left.insert(file_object)
                else:
                    self._left = BST(file_object)
            elif file_object.size > self._file_object.size:
                if self._right:
                    return self._right.insert(file_object)
                else:
                    self._right = BST(file_object)
            else:
                return [self._file_object, file_object]
        else:
            self = BST(file_object)

    def __repr__(self):
        return str(self)
