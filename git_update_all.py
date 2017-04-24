#!/usr/bin/env python
# -*- coding: utf8 -*-
import codecs
import os

import find_git_repos
import git_util


def init_ignore(fname='.git_update_all_ignore'):

    ignore_set = set(['.cache', '.git', '$RECYCLE.BIN',])

    if os.path.exists(fname):
        f = codecs.open(fname, 'r', encoding='utf8')

        additional_list = list(filter(len, list(map(str.strip, f.readlines()))))
        f.close()

        additional_set = set(additional_list)
        ignore_set = ignore_set.union(additional_set)

    ignore_list = tuple(sorted(list(ignore_set)))

    return ignore_list


ignore_list_global = init_ignore()


# TODO : check success / failure of git updates and summarize at the end


class GitRepositoryUpdater(find_git_repos.RecursiveGitRepositoryFinderBase):
    def process_git_folder(self, repo_path):
        if not is_ignore(repo_path):
            # if this repo path is not in the ignore list
            # get remote info dictionary
            remote_info = git_util.get_remote_info_from_git_config(repo_path)
            self.add_remote_url_to_found(repo_path, remote_info)

            remote_name_list = git_util.get_far_remote_name_list(remote_info)
            if remote_name_list:
                # http://stackoverflow.com/questions/7634715/python-decoding-unicode-is-not-supported
                try:
                    path_string = repo_path.encode('cp949')
                except UnicodeEncodeError:
                    path_string = repo_path.encode('utf8')

                message_string = "*** updating %s ***" % path_string
                print(message_string)

                # if repository does not have the branch 'master' try to set a different one
                branch_info_dict = git_util.git_config_branch_info(repo_path)
                branch = 'master'
                if (branch_info_dict) and ('master' not in branch_info_dict):
                    branch = list(branch_info_dict.keys())[0]

                git_util.update_repository(repo_path, remote_list=remote_name_list, branch=branch)

    def add_remote_url_to_found(self, repo_path, remote_info):
        remote_info_items = []
        if remote_info:
            for key, item in remote_info.items():
                remote_info_items.append((key, item.get('url', '')))

        self.found_set.add((repo_path, tuple(remote_info_items)))

    @staticmethod
    def is_remote_bitbucket(remote_info):
        b_remote_is_bitbucket = False
        for server_info in remote_info.values():
            url = server_info.get('url', '')
            if 'bitbucket.org' in url:
                b_remote_is_bitbucket = True
                break
        return b_remote_is_bitbucket

    @staticmethod
    def is_remote_naver(remote_info):
        b_remote_is_naver = False
        for server_info in remote_info.values():
            url = server_info.get('url', '')
            if 'naver.com' in url:
                b_remote_is_naver = True
                break
        return b_remote_is_naver


def git_update_all(root_path=os.path.expanduser('~')):
    """
    Recursively locate git repositories and update
    :param root_path:
    :return:
    """

    updater = GitRepositoryUpdater(root_path, 'config')
    updater.recursively_find_in()


def is_ignore(repo_path, ignore_list=ignore_list_global):
    """
    If any of ignore_list is included in repo_path

    :param repo_path:
    :param ignore_list:
    :return:
    """

    def includes(ignore):
        result_ignore = False
        if ignore in repo_path:
            result_ignore = ignore
        return result_ignore

    result_map = list(map(includes, ignore_list))

    if any(result_map):
        result = result_map
    else:
        result = False

    # print("%r, %r" % (repo_path, result))

    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        git_update_all(sys.argv[1])
