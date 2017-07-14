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

    branch_remotes_str = git_path('branch -r', repo_path)
    branch_remote_list = tuple([branch_name.strip() for branch_name in branch_remotes_str.splitlines()])
    print(branch_remote_list)


def get_remote_list_from_git_remote(repo_path=os.getcwd()):
    # make git run on a given path
    cmd = 'remote'
    remotes_str = git_path(cmd, repo_path)
    remotes_list = remotes_str.splitlines()

    return tuple(remotes_list)


def git_path(cmd, repo_path=os.getcwd()):
    git_path_spec = "-C '%s'" % repo_path
    git_result_str = git_util.git(' '.join((git_path_spec, cmd)))
    return git_result_str


if __name__ == '__main__':
    main(sys.argv)
