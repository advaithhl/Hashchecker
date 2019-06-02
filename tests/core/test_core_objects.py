import unittest
from os import path as os_path

from core.core_objects import DirectoryObject, FileObject, FileSystemObject


class TestFileSystemObject(unittest.TestCase):
    def setUp(self):
        self.fsobject1 = FileSystemObject(
            'tests/hashchecker_test_files/file_with_some_text.txt')
        self.fsobject2 = FileSystemObject('tests/hashchecker_test_files')
        self.non_existent_fsobject = FileSystemObject('spam')

    def test_name(self):
        self.assertEqual(self.fsobject1.name, 'file_with_some_text.txt')
        self.assertEqual(self.fsobject2.name, 'hashchecker_test_files')

    def test_path(self):
        self.assertEqual(
            self.fsobject1.path, os_path.abspath('tests/hashchecker_test_files/file_with_some_text.txt'))
        self.assertEqual(
            self.fsobject2.path, os_path.abspath('tests/hashchecker_test_files'))

    def test_exists(self):
        self.assertTrue(self.fsobject1.exists)
        self.assertTrue(self.fsobject2.exists)
        self.assertFalse(self.non_existent_fsobject.exists)


class TestFileObject(unittest.TestCase):
    def setUp(self):
        self.fobject = FileObject(
            'tests/hashchecker_test_files/file_with_some_text.txt')
        self.non_existent_fobject = FileObject('spam')

    def test_size(self):
        self.assertEqual(self.fobject.size, 46)
        with self.assertRaises(FileNotFoundError):
            self.non_existent_fobject.size

    def test_md5(self):
        self.assertEqual(self.fobject.md5(),
                         'ce90a5f32052ebbcd3b20b315556e154')
        with self.assertRaises(FileNotFoundError):
            self.non_existent_fobject.md5()

    def test_sha1(self):
        self.assertEqual(self.fobject.sha1(),
                         'bae5ed658ab3546aee12f23f36392f35dba1ebdd')
        with self.assertRaises(FileNotFoundError):
            self.non_existent_fobject.sha1()

    def test_sha256(self):
        self.assertEqual(self.fobject.sha256(),
                         '40d5c6f7fe5672fb52269f651c2b985867dfcfa4a5c5258e3d4'
                         'f8736d5095037')
        with self.assertRaises(FileNotFoundError):
            self.non_existent_fobject.sha256()

    def test_sha512(self):
        self.assertEqual(self.fobject.sha512(),
                         '1bb6557a6b5bbd39241a6417b0300a78e5e1cf9fe9abb7dd63e36be5df3c2a1ac242'
                         '8134ede695e2238e6afcee3b405845b2e543991a3dc29d3dc1793b4cfa77')
        with self.assertRaises(FileNotFoundError):
            self.non_existent_fobject.sha512()


class TestDirectoryObject(unittest.TestCase):
    def setUp(self):
        self.dobject = DirectoryObject(
            'tests/hashchecker_test_files/test_directory')
        self.non_existent_dobject = DirectoryObject('spam')

    def test_size(self):
        self.assertEqual(self.dobject.size, 64)
        self.assertEqual(self.non_existent_dobject.size, 0)

    def test_empty(self):
        self.assertFalse(self.dobject.empty)
        with self.assertRaises(FileNotFoundError):
            self.non_existent_dobject.empty
