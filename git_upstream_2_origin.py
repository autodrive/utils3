import os
import pprint
import sys

import git_util


def main(argv):
    # repo path
    if 1 < len(argv):
        repo_path = argv[1]
    else:
        # default
        repo_path = os.getcwd()

    remotes_list = get_remote_list_from_git_remote(repo_path)
    print(remotes_list)

    branch_remote_list = get_remote_branch_list(repo_path)
    print(branch_remote_list)

    remote_branch_dict = {}

    for remote_branch_name_str in branch_remote_list:
        remote_name = remote_branch_name_str[:remote_branch_name_str.index('/')]
        branch_name = remote_branch_name_str[(remote_branch_name_str.index('/') + 1):]
        remote_branch_dict[remote_name] = remote_branch_dict.get(remote_name, []) + [branch_name]

    pprint.pprint(remote_branch_dict)


def get_remote_branch_list(repo_path):
    branch_remotes_str = git_path('branch -r', repo_path)
    branch_remote_list = splitlines_strip(branch_remotes_str)
    return tuple(branch_remote_list)


def splitlines_strip(string):
    result_list = [line.strip() for line in string.splitlines()]
    return result_list


def get_remote_list_from_git_remote(repo_path=os.getcwd()):
    # make git run on a given path
    remotes_str = git_path('remote', repo_path)

    return tuple(splitlines_strip(remotes_str))


def git_path(cmd, repo_path=os.getcwd()):
    git_path_spec = "-C '%s'" % repo_path
    git_result_str = git_util.git(' '.join((git_path_spec, cmd)))
    return git_result_str


if __name__ == '__main__':
    main(sys.argv)
