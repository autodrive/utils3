import os
import sys

import git_util


def main(argv):
    # repo path
    if 1 < len(argv):
        repo_path = argv[1]
    else:
        repo_path = os.getcwd()

    git_path_spec = "-C '%s'" % repo_path

    remotes_list = git_util.git(' '.join((git_path_spec, 'remote')))
    print(remotes_list)


if __name__ == '__main__':
    main(sys.argv)
