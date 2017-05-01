# because these tests took relatively longer time than others
import os
import unittest

import git_util


class TestRecursivelyFindPath(unittest.TestCase):
    """
    tests in git_util related to recursive search seems taking much longer time than others
    """
    def test_recursively_find_git_path(self):
        # function under test
        git_path = git_util.recursively_find_git_path()
        if git_path:
            self.assertTrue(os.path.exists(git_path))
            self.assertTrue(os.path.isfile(git_path))

    def test_recursively_find_sh_path(self):
        sh_path = git_util.recursively_find_sh_path()
        if sh_path:
            self.assertTrue(os.path.exists(sh_path))
            self.assertTrue(os.path.isfile(sh_path))


if __name__ == '__main__':
    unittest.main()
