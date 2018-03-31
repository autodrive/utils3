import os
import sys

from . import git_util


def push_missing_upstream_branches(repo_path=os.getcwd(), b_checkout_force=False):
    git = git_util.Git(repo_path)

    remotes_list = git.get_remote_list_from_git_remote()

    remote_set = set(remotes_list)

    if 1 < len(remote_set):
        if 'upstream' in remote_set:

            branch_remote_list = git.get_remote_branch_list()

            remote_branch_dict = organize_remote_branch_dict(branch_remote_list)

            if 'upstream' in remote_branch_dict:
                origin_branch_set = set(remote_branch_dict['origin'])
                upstream_branch_set = set(remote_branch_dict['upstream'])
                if 'HEAD' in upstream_branch_set:
                    upstream_branch_set.remove('HEAD')

                delta_set = upstream_branch_set - origin_branch_set

                for missing_upstream_branch in delta_set:
                    if b_checkout_force:
                        git.checkout_branch_force(missing_upstream_branch)
                    else:
                        git.checkout_branch(missing_upstream_branch)
                    git.push_origin()

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
