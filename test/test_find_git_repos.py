import os
import unittest

test_run_path = os.path.abspath(os.curdir)
os.chdir(os.pardir)
import find_git_repos

os.chdir(test_run_path)


class TestFindGitRepositories(unittest.TestCase):
    def test_find_git_repos(self):
        # None expected
        git_repositories_found = find_git_repos.find_git_repos(
            os.path.abspath(os.pardir)
        )

        self.assertIsNone(git_repositories_found)


if __name__ == '__main__':
    unittest.main()
