#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

from . import find_git_repos
from . import git_update_all
from . import git_util


def main(argv):
    repo_path = argv[1]
    updater = GrepRemoteRepo(repo_path, 'config')
    updater.recursively_find_in()


class GrepRemoteRepo(find_git_repos.RecursiveGitRepositoryFinderBase):
    def process_git_folder(self, repo_path):
        if not git_update_all.is_ignore(repo_path):
            # if this repo path is not in the ignore list
            # get remote info dictionary
            remote_info_dict_dict = git_util.get_remote_info_from_git_config(repo_path)
            for remote_name, remot_info_dict in remote_info_dict_dict.items():
                git_util.git_logger.info((repo_path, remote_name, remot_info_dict.get('url', "No URL")))


if __name__ == '__main__':
    main(sys.argv)
