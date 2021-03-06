import unittest

from hclib.core.core_actions import calculate, find_duplicates, verify
from hclib.core.core_objects import DirectoryObject, FileObject


class TestActions(unittest.TestCase):
    def setUp(self):
        self.file1 = FileObject(
            'tests/hashchecker_test_files/actions_test/file1')
        self.file2 = FileObject(
            'tests/hashchecker_test_files/actions_test/file2')
        self.file3 = FileObject(
            'tests/hashchecker_test_files/actions_test/.file3')
        self.directory = DirectoryObject(
            'tests/hashchecker_test_files/actions_test')
        self.symdirectory = DirectoryObject(
            'tests/hashchecker_test_files/symlinks')
        self.symlink1 = FileObject(
            'tests/hashchecker_test_files/symlinks/sym_link1')
        self.symlink2 = FileObject(
            'tests/hashchecker_test_files/symlinks/sym_link2')
        self.symfile = FileObject(
            'tests/hashchecker_test_files/symlinks/file.txt')

    def test_calculate(self):
        l = [self.file1, self.file2, self.file3]
        result = calculate(l, 'md5')
        self.assertEqual(
            result[self.file1], '3de8f8b0dc94b8c2230fab9ec0ba0506')
        self.assertEqual(
            result[self.file2], '3de8f8b0dc94b8c2230fab9ec0ba0506')
        self.assertEqual(
            result[self.file3], 'aa019ff43c6fdfa1ceeebca9e4a19dfe')
        with self.assertRaises(TypeError):
            calculate(self.directory, 'md5')

    def test_verify(self):
        l = [self.file1, self.file2, self.file3]
        h = [
            '3de8f8b0dc94b8c2230fab9ec0ba0506',
            '3de8f8b0dc94b8c2230fab9ec0ba0503',
            'aa019ff43c6fdfa1ceeebca9e4a19dfe',
        ]
        result = verify(l, h)
        self.assertTrue(result[self.file1])
        self.assertFalse(result[self.file2])
        self.assertTrue(result[self.file3])
        # Checking for invalid hash
        with self.assertRaises(ValueError):
            verify(
                [self.file1],
                'i am a fake checksum having length not matching any of the '
                'known checksums.')

    def test_find_duplicates(self):
        self.assertDictEqual(
            dict(find_duplicates([], [self.directory])),
            {self.file2: [self.file1]}
        )
        self.assertDictEqual(
            dict(find_duplicates([
                self.file1,
                self.file2,
                self.file3,
            ], [])),
            {self.file1: [self.file2]}
        )
        # Raises FileNotFoundError on non existent file
        with self.assertRaises(FileNotFoundError):
            find_duplicates([FileObject('spam'), FileObject('eggs')], [])

        # Test if symlinks are treated as dupes of original file.
        ret_val = dict(find_duplicates([self.symlink1], [self.symdirectory]))

        # symlink1 is a duplicate of symlink1.
        self.assertIn(self.symlink1, ret_val[self.symlink1])

        # symlink2 is dup of symlink1, because they both point to same file.
        self.assertIn(self.symlink2, ret_val[self.symlink1])

        # symfile must not be a duplicate of any symbolic link which points
        # to it.
        self.assertNotIn(self.symfile, ret_val[self.symlink1])
