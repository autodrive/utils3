#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import sys

import find_git_repos
import git_update_all
import git_util


def main(argv):
    repo_path = argv[1]
    updater = ApplySSH(repo_path, 'config')
    updater.recursively_find_in()


class ApplySSH(find_git_repos.RecursiveGitRepositoryFinderBase):
    def __init__(self, root_path, file_name_spec, b_verbose=False, repo_site_name='bitbucket.org'):
        super(ApplySSH, self).__init__(root_path, file_name_spec, b_verbose)
        self.finder = re.compile(r'https://.*' + repo_site_name + '/.+\.git')

    def process_git_folder(self, repo_path):
        if not git_update_all.is_ignore(repo_path):
            # if this repo path is not in the ignore list
            # get remote info dictionary
            remote_info_dict_dict = git_util.git_config_remote_info(repo_path)
            for remote_name, remote_info_dict in remote_info_dict_dict.items():
                remote_url = remote_info_dict.get('url', None)
                print(remote_name, remote_url)


if __name__ == '__main__':
    main(sys.argv)
