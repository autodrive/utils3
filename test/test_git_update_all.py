import os
import unittest

test_run_path = os.path.abspath(os.curdir)
os.chdir(os.pardir)
import git_update_all
os.chdir(test_run_path)


class TestGitUpdateAll(unittest.TestCase):
    def test_init_ignore(self):
        result = git_update_all.init_ignore()

        self.assertSequenceEqual(('$RECYCLE.BIN', '.cache', '.git'), result)

    def test_init_ignore_blank_line(self):
        result = git_update_all.init_ignore('git_update_ignore_sample.txt')

        result_set = set(result)
        expected_set = set(('a', 'b', 'c', '$RECYCLE.BIN', '.cache', '.git'))

        self.assertSequenceEqual(expected_set, result_set)

    def test_add_remote_url_to_found(self):
        updater = git_update_all.GitRepositoryUpdater(os.path.abspath(os.pardir), 'config')

        path = 'path'
        remote_name = 'remote_name'
        remote_url = 'remote_url'

        remote_info = {remote_name: {'a': 'b', 'c': 'd', 'url': remote_url}}

        updater.add_remote_url_to_found(path, remote_info)
        expected_sequence = set()
        expected_sequence.add((path, ((remote_name, remote_url),)))

        self.assertSetEqual(expected_sequence, updater.found_set)

    def test_is_ignore(self):
        ignore_list = ('regex',)
        repo_path_to_ignore = 'path_to_reject/regex'

        result = git_update_all.is_ignore(repo_path_to_ignore, ignore_list)

        self.assertTrue(result)

        repo_path_not_to_ignore = 'path_to_accept/redex'

        result = git_update_all.is_ignore(repo_path_not_to_ignore, ignore_list)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
