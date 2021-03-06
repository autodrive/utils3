#!/usr/bin/env python
# -*- coding: utf8 -*-
import codecs
import os
import pickle
import random
import time

from . import find_git_repos
from . import git_util


def init_ignore(ignore_filename='.git_update_all_ignore'):

    ignore_set = {'.cache', '.git', '$RECYCLE.BIN',}

    if os.path.exists(ignore_filename):
        f = codecs.open(ignore_filename, 'r', encoding='utf8')

        additional_list = list(filter(len, list(map(str.strip, f.readlines()))))
        f.close()

        additional_set = set(additional_list)
        ignore_set = ignore_set.union(additional_set)
    else:
        with open(ignore_filename, 'w', encoding='utf8') as f_out:
            for ignore_item in ignore_set:
                f_out.write('%s\n' % ignore_item)

    ignore_list = tuple(sorted(list(ignore_set)))

    return ignore_list


ignore_list_global = init_ignore()


# TODO : check success / failure of git updates and summarize at the end


class GitRepositoryUpdater(find_git_repos.RecursiveGitRepositoryFinderBase):
    def __init__(self, root_path, file_name_spec, b_verbose=False, processing_indication_str='adding'):
        super(GitRepositoryUpdater, self).__init__(root_path, file_name_spec, b_verbose)

        self.processing_indication_template = '*** ' + processing_indication_str + ' %s ***'

    def process_git_folder(self, repo_path):
        if not is_ignore(repo_path):
            # if this repo path is not in the ignore list
            # get remote info dictionary
            remote_info, submodule_info = git_util.get_remote_submodule_from_git_config(repo_path)
            self.add_remote_url_to_found(repo_path, remote_info)

            remote_name_list = git_util.get_far_remote_name_list(remote_info)
            if remote_name_list:
                # http://stackoverflow.com/questions/7634715/python-decoding-unicode-is-not-supported
                path_string = repo_path

                message_string = self.processing_indication_template % path_string
                git_util.git_logger.info(message_string)

                # if repository does not have the branch 'master' try to set a different one
                branch_info_dict = git_util.git_config_branch_info(repo_path)
                branch = 'master'
                if (branch_info_dict) and ('master' not in branch_info_dict):
                    branch = list(branch_info_dict.keys())[0]

                self.act_on_repo(repo_path, branch, submodule_info)

    def act_on_repo(self, repo_path, branch, submodule_info):
        git_util.update_repository(repo_path, branch=branch, submodule_info=submodule_info)

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

    start_time_sec = time.time()
    git_util.git_logger.info('git_update_all() : start')
    updater = GitRepositoryUpdater(root_path, 'config')
    updater.recursively_find_in()
    git_util.git_logger.info('git_update_all() : end')
    git_util.git_logger.info('git_update_all() : elapsed time = %g (sec)' % (time.time() - start_time_sec))


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

    # git_util.git_logger.info("%r, %r" % (repo_path, result))

    return result


class RepoListUpdater(GitRepositoryUpdater):
    def __init__(self, root_path, file_name_spec='config', b_verbose=False, repo_list_dict=None):
        super(RepoListUpdater, self).__init__(root_path, file_name_spec, b_verbose=b_verbose)
        if repo_list_dict is None:
            self.repo_list_dict = dict()
        else:
            self.repo_list_dict = dict(repo_list_dict)

        # when a repo_path is visited, added to this set
        self.visited_set = set()

    def act_on_repo(self, repo_path, branch, submodule_info):
        self.visited_set.add(repo_path)
        if repo_path not in self.repo_list_dict:
            self.repo_list_dict[repo_path] = {'branch': branch,
                                              'submodule_info': submodule_info}

    def run_this(self):
        # recursively visit paths
        # this call may take some time
        self.recursively_find_in()

        existing_set = set(self.repo_list_dict.keys())
        unvisited_set = existing_set - self.visited_set

        # remove unvisited repository info from the database
        for unvisited_repo_path in unvisited_set:
            del self.repo_list_dict[unvisited_repo_path]

        return self.repo_list_dict


def build_or_update_repo_list(repo_list_path, root):
    """

    :param str repo_list_path:
    :param str root:
    :return:
    :rtype: list(dict)
    """

    ''' read existing repository list '''
    if os.path.exists(repo_list_path):
        with open(repo_list_path, 'rb') as repo_list_read:
            repo_list_dict = pickle.load(repo_list_read)
    else:
        repo_list_dict = dict()

    # architecture of repo_list_dict
    # repo_list_dict = { <repo_path> : {
    #                                    'branch' : default_branch_str,
    #                                    'submodule_info' : submodule_info_dict,
    #                                  }
    #                  }

    ''' update repository list '''
    updater = RepoListUpdater(root, repo_list_dict)
    updated_repo_list_dict = updater.run_this()

    ''' write repository list '''
    with open(repo_list_path, 'wb') as repo_list_write:
        pickle.dump(updated_repo_list_dict, repo_list_write)

    return updated_repo_list_dict


def process_repo_info(repo_info):
    git_util.git_logger.info('### process_repo_info(%r) ###' % repo_info['path'])

    git_util.update_repository(repo_info['path'], branch=repo_info['branch'],
                               submodule_info=repo_info['submodule_info'])


def process_repo_list(repo_list_dict):
    repo_list = [{'path': key, 'branch': repo_list_dict[key]['branch'],
                  'submodule_info': repo_list_dict[key]['submodule_info']}
                 for key in repo_list_dict]
    random.shuffle(repo_list)

    return list(map(process_repo_info, repo_list))


def updater_processor(argv):
    # no argument : process [default filename].pickle
    # one argument : if path, update under the path and save to the default filename,
    #                if pickle file, process the paths in the file
    # two arguments : (usually) one path and one pickle file :  update below the path. overwrite to the pickle file.
    width = 40
    git_util.git_logger.debug('=== updater_processor() start '.ljust(width, '='))
    start_time_sec = time.time()
    repo_list_path = 'repo_list.pickle'

    b_fetch_rebase = True

    if 1 == len(argv):
        repo_list_dict = load_repo_dict(repo_list_path)
    elif 2 == len(argv):
        script, root = argv
        repo_list_dict = process_arguments(repo_list_path, root)
    elif 3 == len(argv):
        script, repo_list_path, root = argv
        repo_list_dict = process_arguments(repo_list_path, root)
    elif 4 == len(argv):
        script, repo_list_path, root, cmd = argv
        repo_list_dict = process_arguments(repo_list_path, root)

        if 'False' == cmd:
            b_fetch_rebase = False
    else:
        raise ValueError(str(argv))

    if b_fetch_rebase:
        process_repo_list(repo_list_dict)
    end_time_sec = time.time()
    git_util.git_logger.debug('elapsed time = %g(sec)' % (end_time_sec - start_time_sec))
    git_util.git_logger.debug('=== updater_processor() end '.ljust(width, '='))


def load_repo_dict(repo_list_path):
    if not os.path.exists(repo_list_path):
        if os.path.isfile(repo_list_path):
            with open(repo_list_path, 'rb') as repo_list_read:
                repo_list_dict = pickle.load(repo_list_read)
        else:
            raise ValueError('%s is not a file' % repo_list_path)
    else:
        raise ValueError('%s does not exist' % repo_list_path)
    return repo_list_dict


def process_arguments(repo_list_path, root):
    if os.path.exists(root):
        if os.path.isdir(root):
            repo_list_dict = build_or_update_repo_list(repo_list_path, root)
        elif os.path.isfile(root):
            with open(root, 'rb') as repo_list_read:
                repo_list_dict = pickle.load(repo_list_read)
        else:
            raise ValueError('%s type not supported for now' % root)
    else:
        raise ValueError('%s does not exist' % root)
    return repo_list_dict


if __name__ == '__main__':
    import sys

    updater_processor(sys.argv)
