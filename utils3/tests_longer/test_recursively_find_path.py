# because these tests took relatively longer time than others
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import git_util


class TestRecursivelyFindPath(unittest.TestCase):
    """
    tests in git_util related to recursive search seems taking much longer time than others
    """
    def test_recursively_find_git_path(self):
        # function under tests
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
