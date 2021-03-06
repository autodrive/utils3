import os
import unittest
from .. import git_update_all


class TestGitUpdateAll(unittest.TestCase):
    def test_init_ignore(self):
        ignore_path = os.path.join(os.path.split(__file__)[0], 'test_init_ignore.txt')
        result_set = set(git_update_all.init_ignore(ignore_path))

        expected_base_set = set(['.cache', '.git', '$RECYCLE.BIN',])

        # better way to tests than this?
        if os.path.exists(ignore_path):
            with open(ignore_path, 'rt', encoding='utf8') as input_file:
                expected_set = expected_base_set.union(set([line.strip() for line in input_file]))
        else:
            expected_set = expected_base_set
        self.assertSetEqual(expected_set, result_set)

    def test_init_ignore_blank_line(self):
        result = git_update_all.init_ignore(os.path.join(os.path.split(__file__)[0], 'git_update_ignore_sample.txt'))

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
