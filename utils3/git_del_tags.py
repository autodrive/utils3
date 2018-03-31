import os
import pprint
import sys

from . import git_util as git


def main(argv):
    if 2 <= len(argv):
        original_path = os.getcwd()

        path_name = argv[1]
        os.chdir(path_name)

        repo_name = 'origin'

        if 3 <= len(argv):
            repo_name = argv[2]

        result_list = git.delete_all_tags_local_repo(repo_name)
        pprint.pprint(result_list)

        os.chdir(original_path)


if __name__ == '__main__':
    # command line
    main(sys.argv)
