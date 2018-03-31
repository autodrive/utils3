import logging
import os
import tempfile
import unittest

from .. import git_util


class MyTestGitUtilBase(unittest.TestCase):
    def setUp(self):
        # assume this tests is running in a subfolder
        self.repo_path = os.path.abspath(os.path.join(os.pardir, os.pardir))

        if os.path.exists('.git'):
            # if not, correct
            self.repo_path = os.getcwd()

        self.test_file_path = os.path.split(__file__)[0]

        self.test_path = os.getcwd()

    def tearDown(self):
        self.repo_path = ''

    @staticmethod
    def get_new_input_file_name(test_method_name, input_file_name):
        """
        Try to find a new input file name within the package architecture
        """
        print("%s() : os.getcwd() == %s" % (test_method_name, os.getcwd()))
        print("%s() : unable to find file %s" % (test_method_name, input_file_name))
        if os.path.exists('tests') and os.path.isdir('tests'):
            input_file_name = os.path.join('tests', input_file_name)
            if os.path.exists(input_file_name):
                print("%s() : instead found %s" % (test_method_name, input_file_name))
        else:
            test_path = os.path.join('utils3', 'tests')
            if os.path.exists(test_path) and os.path.isdir(test_path):
                input_file_name = os.path.join(test_path, input_file_name)
            else:
                raise ValueError('Unable to decide test path; test is running at %s' % os.getcwd())
            if os.path.exists(input_file_name):
                print("%s() : instead found %s" % (test_method_name, input_file_name))
        return input_file_name


class TestGitUtil(MyTestGitUtilBase):
    # tests git util
    def test_initialize(self):
        # check .ini file read correctly

        input_file_name = 'git_util.ini'

        git_path, sh_path, log_this, log_cumulative, git_logger = git_util.initialize(input_file_name)

        with open('git_util.ini', 'r') as f:
            input_txt = f.read()

        self.assertIn(git_path, input_txt)
        self.assertIn(log_this, input_txt)
        self.assertIn(log_cumulative, input_txt)
        self.assertIn(sh_path, input_txt)
        self.assertIsInstance(git_logger, logging.Logger)

    def test_initialize_logger(self):
        log_file_name = 'temp.log'
        logger = git_util.initialize_logger(log_file_name)
        self.assertIsInstance(logger, logging.Logger)

    def test_is_host(self):
        b_host = git_util.is_host('github', self.repo_path)
        self.assertTrue(b_host)

    def test_remote_info(self):
        dict_host_info = git_util.get_remote_info_from_git_config(self.repo_path)
        self.assertTrue(dict_host_info)
        expected = {}

        filename = os.path.join(self.test_file_path, 'test_case_host_info.txt')
        if not os.path.exists(filename):
            print('''test_remote_info() : Unable to find expected file %s
Generating one from the result''' % filename)
            with open(filename, 'wt') as f:
                f.write(str(dict_host_info))
        expected = eval(open(filename, 'r').read().strip())
        self.maxDiff = None
        self.assertDictEqual(expected, dict_host_info)

    def test_is_host2(self):
        input_file_name = 'test_case_is_host.txt'
        repo_dir = os.path.abspath(os.pardir)

        # git_util.git_logger.debug('%s %s' % ('test_is_host2()', os.getcwd()))
        if not os.path.exists(input_file_name):
            input_file_name = self.get_new_input_file_name('test_is_host2', input_file_name)
            repo_dir = os.getcwd()
        with open(input_file_name, 'rt') as input_file:
            host_name = input_file.read().strip()

        result = git_util.is_host(host_name, repo_dir)
        self.assertTrue(result)

        host_name += '*'
        result = git_util.is_host(host_name, repo_dir)
        self.assertFalse(result)

    def test_get_remote_list(self):
        result = git_util.get_remote_list(os.getcwd(), b_verbose=False)
        expected_set = set(('origin',))
        for expected in expected_set:
            self.assertIn(expected, result)

    def test_is_upstream_in_remote_list(self):
        result = git_util.is_upstream_in_remote_list(os.getcwd(), b_verbose=False)
        # currently there is no remote exactly named 'upstream'
        self.assertFalse(result)

    def test_url_is_remote(self):
        self.assertTrue(git_util.url_is_remote('https:/github.com/def/abc'))
        self.assertTrue(git_util.url_is_remote('git://github.com/schacon/ticgit.git'))
        self.assertFalse(git_util.url_is_remote(r'file:///srv/git/project.git'))
        self.assertFalse(git_util.url_is_remote(r'/srv/git/project/'))

    def test_parse_fetch_all_result_00(self):
            input_txt = '''Fetching origin
From https:/github.com/abc/def
   aaaaaaaaa..bbbbbbbbb  master     -> origin/master
Fetching upstream
From https:/github.com/def/abc
   ccccccccc..ddddddddd  master     -> upstream/master
    '''
            result_dict = git_util.parse_fetch_all_result(input_txt)

            expected_dict = {'origin': {'update': True,
                                        'url': 'https:/github.com/abc/def',
                                        'upstream branch': 'origin/master'},
                             'upstream': {'update': True,
                                          'url': 'https:/github.com/def/abc',
                                          'upstream branch': 'upstream/master'}
                             }
            self.assertDictEqual(expected_dict, result_dict)

    def test_parse_fetch_all_result_01(self):
        input_txt = '''Fetching origin
Fetching upstream
'''
        result_dict = git_util.parse_fetch_all_result(input_txt)

        expected_dict = {'origin': {'update': False},
                         'upstream': {'update': False}
                         }
        self.assertDictEqual(expected_dict, result_dict)

    def test_is_git_error(self):
        txt00_false = ''
        self.assertFalse(git_util.is_git_error(txt00_false))

        txt01_true = 'error: something went wrong'
        self.assertTrue(git_util.is_git_error(txt01_true))

        txt02_true = '''fatal: ambiguous argument 'master': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
'''
        self.assertTrue(git_util.is_git_error(txt02_true))

        txt03_true = '''fatal: no such branch: 'master'
invalid upstream @{u}
'''
        self.assertTrue(git_util.is_git_error(txt03_true))

        txt04_true = '''First, rewinding head to replay your work on top of it...
Applying: such and such modifications are made in this commit
Using index info to reconstruct a base tree...
Falling back to patching base and 3-way merge...
Using index info to reconstruct a bast tree...
M              some/path/some/file.txt
error: Failed to merge in the changes.
Falling back to patching base and 3-way merge...
Auto-merging some/path/some/file.txt
CONFLICT (content): Merge conflict in some/path/some/file.txt
Patch failed at 0000 Go back to constructing dashboards via the DOM.
'''
        self.assertTrue(git_util.is_git_error(txt04_true))

    def test_is_git_warning(self):
        text00_true = '''warning: unable to rmdir utils3: Directory not empty
Switched to branch 'master'
'''
        self.assertTrue(git_util.is_git_warning(text00_true))

        text01_true = '''Fetching origin
warning: redirecting to https://cmake.org/cmake.git/
'''
        self.assertTrue(git_util.is_git_warning(text01_true))

        text02_true = 'warning: inexact rename detection was skipped due to too many files.'
        self.assertTrue(git_util.is_git_warning(text02_true))

        text03_true = 'warning: you may want to set your diff.renameLimit variable to at least 3173 and retry the command.'
        self.assertTrue(git_util.is_git_warning(text03_true))


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

        self.assertIn('origin', remote_info_dict)
        self.assertIn('url', remote_info_dict['origin'])

    def test_remote_info_dict_to_url_tuple(self):
        result_remote_url_tuple = git_util.remote_info_dict_to_url_tuple(self.expected_remote_info_dict)
        # git_util.git_logger.info(result_remote_url_tuple)
        expected_remote_url_tuple = ((self.remote_name_01, self.url_01),
                                     (self.remote_name_02, self.url_02))

        self.assertSequenceEqual(expected_remote_url_tuple, result_remote_url_tuple)

    def test_branch_info(self):
        input_file_name = 'test_branch_info.txt'
        if not os.path.exists(os.path.join(self.test_path, input_file_name)):
            input_file_name = self.get_new_input_file_name('test_branch_info', input_file_name)
        with open(input_file_name, 'r') as f:
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


if __name__ == '__main__':
    unittest.main()
