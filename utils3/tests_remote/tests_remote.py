import os
import unittest

from .. import git_util


class TestGitUtilRemotes(unittest.TestCase):
    def test_get_remote_branch_list(self):
        result_list = git_util.get_remote_branch_list()

        filename = 'remote_branch_list.txt'
        pattern_str = 'heads'

        # get sample file
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
        result_set = set(result_list)

        input_file_name = os.path.join(os.path.split(__file__)[0], 'tags_list.txt')

        if os.path.exists(input_file_name):
            with open(input_file_name, 'r') as f:
                tags_list = [tag_str.strip() for tag_str in f.readlines()]
        else:
            Warning('''file %s might be missing
make a list from git ls-remote''' % (input_file_name))
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

        self.assertFalse(expected_set - result_set, msg='''
expected set = %r
result_set = %r
'''%(expected_set, result_set))

    def test_is_branch_in_remote_branch_list(self):
        self.assertTrue(git_util.is_branch_in_remote_branch_list('master', 'origin', False))
        self.assertFalse(git_util.is_branch_in_remote_branch_list('__m_a_s_t_e_r__', 'origin', False))


if __name__ == '__main__':
    unittest.main()
