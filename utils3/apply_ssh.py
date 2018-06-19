#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re
import sys
import urllib.parse

try:
    from . import find_git_repos
    from . import git_update_all
    from . import git_util

except SystemError:
    # To accomodate both testing and running
    import find_git_repos
    import git_update_all
    import git_util


def run_apply_ssh(argv):
    """
    Run https -> ssh converter
    """
    repo_path = argv[1]

    remote_type = argv[2]

    remote_dict = {'bitbucket': ApplySSHbitbucket,
                   'github': ApplySSHgithub}

    if 4 > len(argv):
        b_arm = False
    else:
        b_arm = get_true_or_false(argv[3])

    updater = remote_dict[remote_type](repo_path, 'config', b_arm=b_arm)
    updater.recursively_find_in()


def get_true_or_false(tf_string):
    if 'false' in tf_string.lower():
        b_arm = False
    elif 'True' == tf_string:
        b_arm = True
    else:
        b_arm = False
    return b_arm


class ApplySSHbitbucket(find_git_repos.RecursiveGitRepositoryFinderBase):
    def __init__(self, root_path, file_name_spec, b_verbose=False, repo_site_name='bitbucket.org', b_arm=False):
        super(ApplySSHbitbucket, self).__init__(root_path, file_name_spec, b_verbose)
        pattern_string = self.get_pattern_string(repo_site_name)
        self.finder = re.compile(pattern_string)
        # if true, overwrite a new url
        self.b_arm = b_arm
        self.start_path = os.getcwd()

    @staticmethod
    def get_pattern_string(repo_site_name):
        pattern_string = r'https://.*' + repo_site_name + '/.+\.git'
        return pattern_string

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
            remote_info_dict_dict = git_util.get_remote_info_from_git_config(repo_path)
            for remote_name, remote_info_dict in remote_info_dict_dict.items():
                remote_url = remote_info_dict.get('url', None)
                if self.is_target(remote_url):
                    os.chdir(repo_path)
                    ssh_url = self.convert_url_https_to_ssh(remote_url)
                    git_cmd, git_cmd_push = self.get_git_cmd_remote_set_url(remote_name, ssh_url, remote_url)
                    if not self.b_arm:
                        git_util.git_logger.info(remote_name, remote_url, ssh_url)
                        git_util.git_logger.info(git_cmd)
                        git_util.git_logger.info(git_cmd_push)
                    else:
                        git_util.git_logger.info("** updating %r **" % repo_path)
                        git_util.git_logger.info(remote_name, remote_url)
                        git_util.git(git_cmd)
                        git_util.git(git_cmd_push)
                    os.chdir(self.start_path)
                elif remote_url is not None:
                    if ('@github.com' in remote_url) and ('http' in remote_url):
                        git_util.git_logger.info('skipping remote_url = %s' % remote_url)

    @staticmethod
    def get_git_cmd_remote_set_url(remote_name, ssh_url, https_url):
        """
        usage: git remote [-v | --verbose]
           or: git remote add [-t <branch>] [-m <master>] [-f] [--tags | --no-tags] [--mirror=<fetch|push>] <name> <url>
           or: git remote rename <old> <new>
           or: git remote remove <name>
           or: git remote set-head <name> (-a | --auto | -d | --delete | <branch>)
           or: git remote [-v | --verbose] show [-n] <name>
           or: git remote prune [-n | --dry-run] <name>
           or: git remote [-v | --verbose] update [-p | --prune] [(<group> | <remote>)...]
           or: git remote set-branches [--add] <name> <branch>...
           or: git remote get-url [--push] [--all] <name>
           or: git remote set-url [--push] <name> <newurl> [<oldurl>]
           or: git remote set-url --add <name> <newurl>
           or: git remote set-url --delete <name> <url>

            -v, --verbose         be verbose; must be placed before a subcommand

        :param remote_name:
        :param ssh_url:
        :return:
        """
        git_cmd = 'remote -v set-url %s %s %s' % (remote_name, ssh_url, https_url)
        git_cmd_push = 'remote -v set-url --push %s %s %s' % (remote_name, ssh_url, https_url)
        return git_cmd, git_cmd_push

    @staticmethod
    def convert_url_https_to_ssh(https_url):
        """
        convert https url to ssh url mainly for bitbucket.org
        see : https://confluence.atlassian.com/bitbucket/set-up-ssh-for-git-728138079.html
              https://<accountname>@bitbucket.org/< accountname>/<reponame>.git
              ssh://git@bitbucket.org /< accountname>/<reponame>.git

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


class ApplySSHgithub(ApplySSHbitbucket):
    def __init__(self, root_path, file_name_spec, b_verbose=False, repo_site_name='github.com', b_arm=False):
        super(ApplySSHgithub, self).__init__(root_path, file_name_spec, b_verbose, repo_site_name, b_arm)

    @staticmethod
    def get_pattern_string(repo_site_name):
        if not repo_site_name.startswith('@'):
            repo_site_name = '@' + repo_site_name
        pattern_string = r'https://.+?' + repo_site_name + '/.+'
        return pattern_string


    @staticmethod
    def convert_url_https_to_ssh(https_url):
        """
        convert https url to ssh url for github.com
        see : https://gist.github.com/jexchan/2351996
              https://help.github.com/articles/connecting-to-github-with-ssh/

        :param str https_url:
        :return:
        """

        parse_result = urllib.parse.urlparse(https_url)
        parse_result_list = list(parse_result)

        # scheme 
        parse_result_list[0] = 'ssh'


        # netloc
        parse_result_list[1] = 'git@' + parse_result.hostname + '-' + parse_result.username

        # path
        if not parse_result_list[2].endswith('.git'):
            parse_result_list[2] += '.git'

        # make ssh url
        ssh_url = urllib.parse.urlunparse(parse_result_list)
        return ssh_url


def main(argv):
    d = list_ssh_repos(argv[1])
   
    n_max_key_width = 0
    for key in d:
        if len(str(key)) > n_max_key_width:
            n_max_key_width = len(str(key))
    
    formatter = '{k:3d} {key:%ds} {path}' % n_max_key_width

    for k, key in enumerate(d):
        print(formatter.format(k=k, key=key, path=d[key]['path']))


def list_ssh_repos(root):
    result_dict = {}
    for repo_path, dir_list, file_list in gen_all_repo_paths(root):
        repo_name = os.path.split(repo_path)[-1]
        result_dict[repo_name] = {'path':repo_path}

    return result_dict


def gen_all_repo_paths(root):
    """
    A generator for all repository paths
    Would pass if .git or igore path
    """

    for root_path, dir_list, file_list in os.walk(root):
        if '.git' not in root_path.split(os.sep):
            if '.git' in dir_list:
                yield root_path, dir_list, file_list


if __name__ == '__main__':
    main(sys.argv)
