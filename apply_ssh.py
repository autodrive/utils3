#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import sys
import urllib.parse

import find_git_repos
import git_update_all
import git_util


def main(argv):
    repo_path = argv[1]
    updater = ApplySSH(repo_path, 'config')
    updater.recursively_find_in()


class ApplySSH(find_git_repos.RecursiveGitRepositoryFinderBase):
    def __init__(self, root_path, file_name_spec, b_verbose=False, repo_site_name='bitbucket.org', b_arm=False):
        super(ApplySSH, self).__init__(root_path, file_name_spec, b_verbose)
        self.finder = re.compile(r'https://.*' + repo_site_name + '/.+\.git')
        # if true, overwrite a new url
        self.b_arm = b_arm

    def is_target(self, url):
        if url is not None:
            result = bool(self.finder.findall(url))
        else:
            result = False
        return result

    def process_git_folder(self, repo_path):
        if not git_update_all.is_ignore(repo_path):
            # if this repo path is not in the ignore list
            # get remote info dictionary
            remote_info_dict_dict = git_util.git_config_remote_info(repo_path)
            for remote_name, remote_info_dict in remote_info_dict_dict.items():
                remote_url = remote_info_dict.get('url', None)
                if self.is_target(remote_url):
                    ssh_url = self.convert_url_https_to_ssh(remote_url)
                    git_cmd = 'remote %s %s' % (remote_name, ssh_url)
                    print(remote_name, remote_url, ssh_url, git_cmd)

    @staticmethod
    def convert_url_https_to_ssh(https_url):
        """
        convert https url to ssh url mainly for bitbucket.org
        see : https://confluence.atlassian.com/bitbucket/set-up-ssh-for-git-728138079.html

        :param str https_url:
        :return:
        """

        parse_result = list(urllib.parse.urlparse(https_url))
        # scheme
        parse_result[0] = 'ssh'

        # netloc
        netloc_split = parse_result[1].split('@')
        parse_result[1] = 'git@' + netloc_split[-1]

        # make ssh url
        ssh_url = urllib.parse.urlunparse(parse_result)
        return ssh_url


if __name__ == '__main__':
    main(sys.argv)
