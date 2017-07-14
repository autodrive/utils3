import os
import pprint
import sys

import git_util


def push_missing_upstream_branches(repo_path=os.getcwd(), b_checkout_force=False):

    remotes_list = get_remote_list_from_git_remote(repo_path)
    print(remotes_list)

    remote_set = set(remotes_list)

    if 1 < len(remote_set):
        if 'upstream' in remote_set:

            branch_remote_list = get_remote_branch_list(repo_path)
            print(branch_remote_list)

            remote_branch_dict = organize_remote_branch_dict(branch_remote_list)

            pprint.pprint(remote_branch_dict)

            if 'upstream' in remote_branch_dict:
                origin_branch_set = set(remote_branch_dict['origin'])
                upstream_branch_set = set(remote_branch_dict['upstream'])
                upstream_branch_set.remove('HEAD')

                delta_set = upstream_branch_set - origin_branch_set

                print('delta_set =')
                pprint.pprint(delta_set)

                for missing_upstream_branch in delta_set:
                    if b_checkout_force:
                        git_util.git_path('checkout %s --force' % missing_upstream_branch, repo_path)
                    else:
                        git_util.git_path('checkout %s' % missing_upstream_branch, repo_path)
                    git_util.git_path('push origin', repo_path)

        else:
            ValueError('upstream not in remote : %r' % remote_set)
    elif 1 == len(remote_set):
        print('only one remote')
    elif 0 == len(remote_set):
        print('no remote')
    else:
        raise ValueError('# repository = %r' % len(remote_set))


def organize_remote_branch_dict(git_branch_r_list):
    remote_branch_dict = {}

    for remote_branch_name_str in git_branch_r_list:
        remote_name, branch_name = remote_branch_name_str.split('/', maxsplit=1)
        remote_branch_dict[remote_name] = remote_branch_dict.get(remote_name, []) + [branch_name]

    return remote_branch_dict


def get_remote_branch_list(repo_path):
    branch_remotes_str = git_util.git_path('branch -r', repo_path)
    branch_remote_list = splitlines_strip(branch_remotes_str)
    return tuple(branch_remote_list)


def splitlines_strip(string):
    result_list = [line.strip() for line in string.splitlines()]
    return result_list


def get_remote_list_from_git_remote(repo_path=os.getcwd()):
    # make git run on a given path
    remotes_str = git_util.git_path('remote', repo_path)

    return tuple(splitlines_strip(remotes_str))


if __name__ == '__main__':
    # repo path
    if 1 < len(sys.argv):
        repository_path = sys.argv[1]
    else:
        # default
        repository_path = os.getcwd()

    if 2 < len(sys.argv):
        b_should_checkout_by_force = sys.argv[2].lower().startswith('true')
    else:
        b_should_checkout_by_force = False

    push_missing_upstream_branches(repository_path, b_should_checkout_by_force)
