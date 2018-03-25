# because these tests took relatively longer time than others
import random
import unittest
import re

import utils3.utils3.git_util as git_util


class TestRecursivelyFindPath(unittest.TestCase):
    def test_git_tag_local_repo(self):
        tag_name = 'del_this_%d' % random.randint(1, 100)
        repo_name = 'origin'
        result_dict = git_util.git_tag_local_repo(tag_name, repo_name)

        self.assertFalse(re.findall('Permission to .+? denied to .+?$', result_dict['remote']))

        try:
            local_tag_list = git_util.get_tag_local_list()
            self.assertIn(tag_name, local_tag_list, msg='%s not in local tag list' % tag_name)

            repo_tag_list = git_util.get_remote_tag_list(repo_name)
            self.assertIn(tag_name, repo_tag_list, msg='%s not in repo %s tag list' % (tag_name, repo_name))
        except AssertionError as e:
            git_util.delete_a_tag_local_repo(tag_name, repo_name)
            raise e

        git_util.delete_a_tag_local_repo(tag_name, repo_name)


if __name__ == '__main__':
    unittest.main()
