import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import find_git_repos


class TestFindGitRepositories(unittest.TestCase):
    def test_find_git_repos(self):
        # function under test
        # try to find repositories on the same level as this one
        git_repositories_found = find_git_repos.find_git_repos(os.path.abspath(os.path.join(os.pardir, os.pardir)),
                                                               b_verbose=False)

        # sample file in the test script folder
        sample_file_name = os.path.join(os.path.split(__file__)[0], 'test_find_git_repos.txt')

        # if sample file missing
        if not os.path.exists(sample_file_name):
            print('''test_find_git_repos() : File %s is missing
Generating one''' % sample_file_name)

            with open(sample_file_name, 'wt') as f:
                # trying to find a git path checking folders in the higher levels
                possible_path = __file__
                counter = 0
                # if possible_path becomes too short, stop
                while 1 < len(possible_path):
                    # to debug
                    # print('test_find_git_repos() : possible_path =', possible_path)

                    # go up one level in the path
                    new_possible_path = os.path.split(possible_path)[0]
                    if new_possible_path == possible_path:
                        break
                    else:
                        possible_path = new_possible_path
                        # if possible_path is a git repository, following folder should exist
                        possible_git_path = os.path.join(possible_path, '.git')
                        if os.path.exists(possible_git_path) and os.path.isdir(possible_git_path):
                            # to know how many found
                            counter += 1
                            # write the repository path
                            f.write(possible_path + '\n')
                            # guess one repository might be enough for now?
                # if found none: print warning
                if 1 > counter:
                    print("test_find_git_repos() : Could not find a git repository; please manually add to %s" % (sample_file_name))

        expected_set = set()

        with open(sample_file_name, 'rt') as sample_file:
            for item in sample_file:
                expected_set.add(item.strip())

        self.assertFalse(expected_set - git_repositories_found.found_set,
        msg='''test_find_git_repos() : expected_set = %r
result_set = %r
''' % (expected_set, git_repositories_found.found_set))


if __name__ == '__main__':
    unittest.main()
