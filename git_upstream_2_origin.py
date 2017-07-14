import os
import sys

import git_util


def main(argv):
    # repo path
    if 1 < len(argv):
        repo_path = argv[1]
    else:
        repo_path = os.getcwd()

    remotes_list = get_remote_list_from_git_remote(repo_path)

    print(remotes_list)


def get_remote_list_from_git_remote(repo_path=os.getcwd()):
    # make git run on a given path
    cmd = 'remote'
    git_path_spec = "-C '%s'" % repo_path

    remotes_str = git_util.git(' '.join((git_path_spec, cmd)))
    remotes_list = remotes_str.splitlines()

    return tuple(remotes_list)


if __name__ == '__main__':
    main(sys.argv)
