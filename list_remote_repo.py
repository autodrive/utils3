#!/usr/bin/env python
# -*- coding: utf8 -*-

import find_git_repos
import git_update_all
import git_util
import sys


def main(argv):
    repo_path = argv[1]
    updater = GrepRemoteRepo(repo_path, 'config')
    updater.recursively_find_in()


class GrepRemoteRepo(find_git_repos.RecursiveGitRepositoryFinderBase):
    def process_git_folder(self, repo_path):
        if not git_update_all.is_ignore(repo_path):
            # if this repo path is not in the ignore list
            # get remote info dictionary
            remote_info_dict_dict = git_util.git_config_remote_info(repo_path)
            for remote_name, remot_info_dict in remote_info_dict_dict.iteritems():
                print(repo_path, remote_name, remot_info_dict.get('url', "No URL"))


if __name__ == '__main__':
    main(sys.argv)
