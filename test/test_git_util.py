import os
import tempfile
import unittest
import random


# to use git_util.ini of ..
current_path = os.path.abspath(os.curdir)
os.chdir(os.pardir)
import git_util
os.chdir(current_path)


class TestGitUtil(unittest.TestCase):
    # test git util
    def test_initialize(self):
        # check .ini file read correctly
        git_path, sh_path, log_this, log_cumulative = git_util.initialize('git_util.ini')
        self.assertEqual('a', git_path)
        self.assertEqual('b', log_this)
        self.assertEqual('c', log_cumulative)
        self.assertEqual('d', sh_path)

    def test_is_host(self):
        b_host = git_util.is_host('github', os.pardir)
        self.assertTrue(b_host)

    def test_remote_info(self):
        dict_hist_info = git_util.git_config_remote_info(os.pardir)
        self.assertTrue(dict_hist_info)
        expected = eval(open('test_case_host_info.txt', 'r').read().strip())
        self.assertSequenceEqual(expected.items(), dict_hist_info.items())

    def test_is_host(self):
        host_name = open('test_case_is_host.txt', 'rt').read().strip()
        result = git_util.is_host(host_name, os.pardir)
        self.assertTrue(result)

        host_name += '*'
        result = git_util.is_host(host_name, os.pardir)
        self.assertFalse(result)


class TestGitUtilRemoteInfo(unittest.TestCase):
    def setUp(self):
        self.remote_name_01 = 'origin'
        self.remote_name_02 = 'upstream'

        self.url_01 = 'abc'
        self.url_02 = 'jkl'

        self.fetch_01 = 'def'
        self.fetch_02 = 'mno'

        self.pushurl_01 = 'ghi'
        self.pushurl_02 = 'pqr'

        self.expected_remote_info_dict = {
            self.remote_name_01: {'url': self.url_01, 'fetch': self.fetch_01, 'pushurl': self.pushurl_01, },
            self.remote_name_02: {'url': self.url_02, 'fetch': self.fetch_02, 'pushurl': self.pushurl_02, },
        }

    def test_remote_info(self):
        temp_folder = tempfile.mkdtemp()
        config_file_name = None
        git_dir_name = None
        try:
            # write a (fake) config file
            git_dir_name = os.path.join(temp_folder, '.git')
            os.mkdir(git_dir_name)
            config_file_name = os.path.join(git_dir_name, 'config')
            with open(config_file_name, 'w') as f:
                txt = '''[remote "%s"]
        url = %s
        fetch = %s
        pushurl = %s
[remote "%s"]
        url = %s
        fetch = %s
        pushurl = %s
''' % (
                    self.remote_name_01, self.url_01, self.fetch_01, self.pushurl_01,
                    self.remote_name_02, self.url_02, self.fetch_02, self.pushurl_02,
                )
                f.write(txt)
                f.close()

            remote_info_dict = git_util.git_config_remote_info(temp_folder)

        except:
            if os.path.exists(config_file_name):
                os.remove(config_file_name)
            if os.path.exists(git_dir_name):
                os.rmdir(git_dir_name)
            if os.path.exists(temp_folder):
                os.rmdir(temp_folder)
            raise

        if os.path.exists(config_file_name):
            os.remove(config_file_name)
        if os.path.exists(git_dir_name):
            os.rmdir(git_dir_name)
        if os.path.exists(temp_folder):
            os.rmdir(temp_folder)

        self.assertSequenceEqual(self.expected_remote_info_dict, remote_info_dict)

    def test_remote_info_dict_to_url_tuple(self):
        result_remote_url_tuple = git_util.remote_info_dict_to_url_tuple(self.expected_remote_info_dict)
        # print(result_remote_url_tuple)
        expected_remote_url_tuple = ((self.remote_name_01, self.url_01),
                                     (self.remote_name_02, self.url_02))

        self.assertSequenceEqual(expected_remote_url_tuple, result_remote_url_tuple)

    def test_branch_info(self):
        with open('test_branch_info.txt', 'r') as f:
            txt = f.read()

        temp_folder = tempfile.mkdtemp()
        config_file_name = None
        git_dir_name = None
        try:
            # write a (fake) config file
            git_dir_name = os.path.join(temp_folder, '.git')
            os.mkdir(git_dir_name)
            config_file_name = os.path.join(git_dir_name, 'config')
            with open(config_file_name, 'w') as f:
                f.write(txt)
                f.close()

            branch_info_dict = git_util.git_config_branch_info(temp_folder)

        except:
            if os.path.exists(config_file_name):
                os.remove(config_file_name)
            if os.path.exists(git_dir_name):
                os.rmdir(git_dir_name)
            if os.path.exists(temp_folder):
                os.rmdir(temp_folder)
            raise

        if os.path.exists(config_file_name):
            os.remove(config_file_name)
        if os.path.exists(git_dir_name):
            os.rmdir(git_dir_name)
        if os.path.exists(temp_folder):
            os.rmdir(temp_folder)

        expected_branch_info_dict = {'feature/git': {'merge': 'refs/heads/feature/git', 'remote': 'origin'},
                                     'develop': {'merge': 'refs/heads/develop', 'remote': 'origin'},
                                     'master': {'merge': 'refs/heads/master', 'remote': 'origin'}}

        self.assertSequenceEqual(expected_branch_info_dict, branch_info_dict)

    def test_remote_is_remote(self):
        remote_info_dict = {
            self.remote_name_01: {'url': 'https://www.naver.com', 'fetch': self.fetch_01, 'pushurl': self.pushurl_01, },
            self.remote_name_02: {'url': 'file:/user/binary/', 'fetch': self.fetch_02, 'pushurl': self.pushurl_02, },
        }
        self.assertTrue(git_util.remote_is_remote(remote_info_dict))

        local_info_dict = {
            self.remote_name_01: {'url': 'file:/user/text/', 'fetch': self.fetch_01, 'pushurl': self.pushurl_01, },
            self.remote_name_02: {'url': 'file:/user/binary/', 'fetch': self.fetch_02, 'pushurl': self.pushurl_02, },
        }
        self.assertFalse(git_util.remote_is_remote(local_info_dict))

    def test_get_far_remote_name_list(self):
        remote_info_dict = {
            self.remote_name_01: {'url': 'https://www.naver.com', 'fetch': self.fetch_01, 'pushurl': self.pushurl_01, },
            self.remote_name_02: {'url': 'file:/user/binary/', 'fetch': self.fetch_02, 'pushurl': self.pushurl_02, },
        }

        result = git_util.get_far_remote_name_list(remote_info_dict)
        self.assertSequenceEqual([self.remote_name_01], result)

        local_info_dict = {
            self.remote_name_01: {'url': 'file:/user/text/', 'fetch': self.fetch_01, 'pushurl': self.pushurl_01, },
            self.remote_name_02: {'url': '/user/binary/', 'fetch': self.fetch_02, 'pushurl': self.pushurl_02, },
            'not_far': {'url': 'z:/user/binary/', 'fetch': self.fetch_02, 'pushurl': self.pushurl_02, },
        }
        self.assertFalse(git_util.get_far_remote_name_list(local_info_dict))

    def test_get_tag_list(self):
        result_list = git_util.get_tag_local_list()
        expected_set = {'bug/finish/found_set', 'bug/finish/repo_finder_moved', 'bug/start/found_set',
                        'bug/start/repo_finder_moved'}
        result_set = set(result_list)

        self.assertSetEqual(expected_set, result_set.intersection(expected_set))

    def test_get_tag_repo_list(self):
        result_list = git_util.get_tag_repo_list()
        expected_set = set()
        self.assertSetEqual(expected_set, set(result_list))

    def test_git_tag_local_repo(self):
        tag_name = 'del_this_%d' % random.randint(1, 100)
        repo_name = 'origin'
        result_dict = git_util.git_tag_local_repo(tag_name, repo_name)

        try:
            local_tag_list = git_util.get_tag_local_list()
            self.assertTrue(tag_name in local_tag_list, msg='%s not in local tag list' % tag_name)

            repo_tag_list = git_util.get_tag_repo_list(repo_name)
            self.assertTrue(tag_name in repo_tag_list, msg='%s not in repo %s tag list' % (tag_name, repo_name))
        except AssertionError as e:
            git_util.delete_a_tag_local_repo(tag_name, repo_name)
            raise e

        git_util.delete_a_tag_local_repo(tag_name, repo_name)


if __name__ == '__main__':
    unittest.main()
