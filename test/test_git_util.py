import os
import tempfile
import unittest

current_path = os.path.abspath(os.curdir)
os.chdir(os.pardir)
import git_util

os.chdir(current_path)


class MyTestGitUtilBase(unittest.TestCase):
    def setUp(self):
        # assume this test is running in a subfolder
        self.repo_path = os.path.abspath(os.pardir)

        if os.path.exists('.git'):
            # if not, correct
            self.repo_path = os.getcwd()

        self.test_path = os.path.join(self.repo_path, 'test')

    def tearDown(self):
        self.repo_path = ''


class TestGitUtil(MyTestGitUtilBase):
    # test git util
    def test_initialize(self):
        # check .ini file read correctly

        input_file_name = 'git_util.ini'
        if os.path.exists('.git') and os.path.exists('test'):
            input_file_name = os.path.join('test', input_file_name)

        git_path, sh_path, log_this, log_cumulative = git_util.initialize(input_file_name)
        self.assertEqual('a', git_path)
        self.assertEqual('b', log_this)
        self.assertEqual('c', log_cumulative)
        self.assertEqual('d', sh_path)

    def test_is_host(self):
        b_host = git_util.is_host('github', self.repo_path)
        self.assertTrue(b_host)

    def test_remote_info(self):
        dict_hist_info = git_util.get_remote_info_from_git_config(self.repo_path)
        self.assertTrue(dict_hist_info)
        expected = {}

        filename = os.path.join(self.test_path, 'test_case_host_info.txt')
        if os.path.exists(filename):
            expected = eval(open(filename, 'r').read().strip())
        self.assertDictEqual(expected, dict_hist_info)

    def test_is_host2(self):
        input_file_name = 'test_case_is_host.txt'
        repo_dir = os.path.abspath(os.pardir)

        git_util.logging.info('test_is_host2()', os.getcwd())
        if not os.path.exists(input_file_name):
            input_file_name = os.path.join('test', input_file_name)
            repo_dir = os.getcwd()
        with open(input_file_name, 'rt') as input_file:
            host_name = input_file.read().strip()

        result = git_util.is_host(host_name, repo_dir)
        self.assertTrue(result)

        host_name += '*'
        result = git_util.is_host(host_name, repo_dir)
        self.assertFalse(result)

    def test_get_remote_list(self):
        result = git_util.get_remote_list(os.path.abspath(os.curdir), b_verbose=False)
        expected = ('origin', 'py2_upstream')
        self.assertSequenceEqual(expected, result)

    def test_is_upstream_in_remote_list(self):
        result = git_util.is_upstream_in_remote_list(os.path.abspath(os.curdir), b_verbose=False)
        # currently there is no remote exactly named 'upstream'
        self.assertFalse(result)

    def test_url_is_remote(self):
        self.assertTrue(git_util.url_is_remote('https://github.com/tensorflow/tensorflow'))
        self.assertTrue(git_util.url_is_remote('git://github.com/schacon/ticgit.git'))
        self.assertFalse(git_util.url_is_remote(r'file:///srv/git/project.git'))
        self.assertFalse(git_util.url_is_remote(r'/srv/git/project/'))


class TestGitUtilRemoteInfo(MyTestGitUtilBase):
    def setUp(self):
        super(TestGitUtilRemoteInfo, self).setUp()

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

    def tearDown(self):
        super(TestGitUtilRemoteInfo, self).tearDown()

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

            remote_info_dict = git_util.get_remote_info_from_git_config(temp_folder)

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
        # git_util.logging.info(result_remote_url_tuple)
        expected_remote_url_tuple = ((self.remote_name_01, self.url_01),
                                     (self.remote_name_02, self.url_02))

        self.assertSequenceEqual(expected_remote_url_tuple, result_remote_url_tuple)

    def test_branch_info(self):
        with open(os.path.join(self.test_path, 'test_branch_info.txt'), 'r') as f:
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

    def test_get_tag_local_list(self):
        result_list = git_util.get_tag_local_list()
        expected_set = {'20170313', '20170226'}
        result_set = set(result_list)

        self.assertSetEqual(expected_set, result_set.intersection(expected_set))

    def test_get_remote_branch_list(self):
        result_list = git_util.get_remote_branch_list()

        filename = 'remote_branch_list.txt'
        pattern_str = 'heads'

        try:
            with open(filename, 'r') as f:
                tags_list = [tag_str.strip() for tag_str in f.readlines()]

        except IOError as e:
            # file might be missing
            # make a list from git ls-remote
            result_txt = git_util.git('ls-remote --%s' % pattern_str)
            result_line_list = result_txt.splitlines()

            if result_line_list[0].startswith('From '):
                result_line_list.pop(0)

            tags_list = []
            with open(filename, 'w') as f_out:

                # build list of expected tags
                for line_txt in result_line_list:
                    line_split_list = line_txt.split()
                    # filter remote tags
                    filtered_line_split_list = [txt for txt in line_split_list if
                                                txt.startswith('refs/%s/' % pattern_str)
                                                and (not txt.endswith('^{}'))]
                    if filtered_line_split_list:
                        for tag_item in filtered_line_split_list:
                            tag_items = tag_item.split('/')[2:]
                            tag_txt = '/'.join(tag_items)
                            f_out.write(tag_txt + '\n')
                            tags_list.append(tag_txt)
        # finished making a list from git ls-remote

        expected_set = set(tags_list)
        self.assertSetEqual(expected_set, set(result_list))

    def test_get_remote_tag_list(self):
        result_list = git_util.get_remote_tag_list()
        try:
            with open('tags_list.txt', 'r') as f:
                tags_list = [tag_str.strip() for tag_str in f.readlines()]

        except IOError as e:
            # file might be missing
            # make a list from git ls-remote
            result_txt = git_util.git('ls-remote --tags')
            result_line_list = result_txt.splitlines()

            if result_line_list[0].startswith('From '):
                result_line_list.pop(0)

            tags_list = []
            with open('tags_list.txt', 'w') as f_out:

                # build list of expected tags
                for line_txt in result_line_list:
                    line_split_list = line_txt.split()
                    # filter remote tags
                    filtered_line_split_list = [txt for txt in line_split_list if txt.startswith('refs/tags/')
                                                and (not txt.endswith('^{}'))]
                    if filtered_line_split_list:
                        for tag_item in filtered_line_split_list:
                            tag_items = tag_item.split('/')[2:]
                            tag_txt = '/'.join(tag_items)
                            f_out.write(tag_txt + '\n')
                            tags_list.append(tag_txt)
        # finished making a list from git ls-remote

        expected_set = set(tags_list)
        self.assertSetEqual(expected_set, set(result_list))

    def test_is_branch_in_remote_branch_list(self):
        self.assertTrue(git_util.is_branch_in_remote_branch_list('master', 'origin', False))
        self.assertFalse(git_util.is_branch_in_remote_branch_list('__m_a_s_t_e_r__', 'origin', False))


if __name__ == '__main__':
    unittest.main()
