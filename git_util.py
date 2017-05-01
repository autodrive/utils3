# -*- coding: utf8 -*-
"""
Git utility with interfaces

Will create a git_util.ini during import if missing (may take some time)

includes other utility functions
"""
import configparser as cp
import logging
import logging.handlers
import os
import re
import subprocess
import sys
import time
import urllib.parse

# TODO : remote info of git-svn

# configuration section names
git_configuration = {
    'config_filename': 'git_util.ini',
    'git_section': 'git',
    'git_section_path': 'path',
    'git_section_sh_path': 'sh_path',

    'log_section': 'log',
    'log_section_this': 'this',
    'log_section_cumulative': 'cumulative',

    'log_this_filename': 'git_this.log',
    'log_cumulative_filename': 'git.log',
}


def initialize(git_config_filename=git_configuration['config_filename']):
    """
    read git.config and initialize parameters
    git.config is expected to have following structure

    [git]
    path =
    sh_path =
    [log]
    this =
    cumulative =
    ...

    :param git_config_filename:
    :return:
    """
    # config parser example, https://wiki.python.org/moin/ConfigParserExamples
    config_parser = init_config_parser(git_config_filename)

    git_path = config_parser.get(git_configuration['git_section'], git_configuration['git_section_path'])
    sh_path = config_parser.get(git_configuration['git_section'], git_configuration['git_section_sh_path'])

    log_this = config_parser.get(git_configuration['log_section'], git_configuration['log_section_this'])
    log_cumulative = config_parser.get(git_configuration['log_section'],
                                       git_configuration['log_section_cumulative'])

    git_logger_under_construction = initialize_logger(log_cumulative)

    return git_path, sh_path, log_this, log_cumulative, git_logger_under_construction


def initialize_logger(log_file_name):
    # http://gyus.me/?p=418
    # https://docs.python.org/3/library/logging.html

    # make logger instance
    git_logger_under_construction = logging.getLogger('git_logger')

    # make log formatter
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # make handlers for stream and file
    file_handler = logging.FileHandler(log_file_name)
    stream_handler = logging.StreamHandler()

    # apply formatter to handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # add handlers to logger
    git_logger_under_construction.addHandler(file_handler)
    git_logger_under_construction.addHandler(stream_handler)

    # set logging level
    git_logger_under_construction.setLevel(logging.DEBUG)

    return git_logger_under_construction


def init_config_parser(git_config_filename):
    """
    Initialize configuration object for git utility.  If the file does not exist, generate a default one and read it.
    :param git_config_filename:
    :return:
    """
    config_parser = cp.ConfigParser()

    if not os.path.exists(git_config_filename):
        generate_config_file()

    config_parser.read(git_config_filename)
    return config_parser


def generate_config_file():
    # prepare configuration file contents
    git_path = recursively_find_git_path()
    sh_path = recursively_find_sh_path()
    log_this = os.path.abspath(os.path.join(os.curdir, git_configuration['log_this_filename']))
    log_cumulative = os.path.abspath(os.path.join(os.curdir, git_configuration['log_cumulative_filename']))

    # prepare configuration object
    config_parser = cp.ConfigParser()
    config_parser.add_section(git_configuration['git_section'])
    config_parser.set(git_configuration['git_section'], git_configuration['git_section_path'], git_path)
    config_parser.set(git_configuration['git_section'], git_configuration['git_section_sh_path'], sh_path)

    config_parser.add_section(git_configuration['log_section'])
    config_parser.set(git_configuration['log_section'], git_configuration['log_section_this'], log_this)
    config_parser.set(git_configuration['log_section'], git_configuration['log_section_cumulative'], log_cumulative)
    # end prepare configuration object

    # write to configuration file
    with open(git_configuration['config_filename'], 'w') as config_file:
        config_parser.write(config_file)


def recursively_find_git_path():
    root = os.path.join(os.sep)
    if 2 == len(sys.argv):
        root = sys.argv[1]
    git_path = ''
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            name = os.path.splitext(filename)[0]
            if 'git' == name:
                full_path = os.path.join(dirpath, filename)
                # test a file is executable http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    git_path = full_path
                    return git_path
    return git_path


def recursively_find_sh_path():
    root = os.path.join(os.sep)
    if 2 == len(sys.argv):
        root = sys.argv[1]
    sh_path = ''
    for dir_path, dir_names, file_names in os.walk(root):
        for filename in file_names:
            name = os.path.splitext(filename)[0]
            if 'sh' == name:
                full_path = os.path.join(dir_path, filename)
                # test a file is executable http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    sh_path = full_path
                    return sh_path
    return sh_path


git_path_string, sh_path_string, log_this_global, log_cumulative_global, git_logger = initialize()

if not os.path.exists(git_path_string.strip('"')):
    git_logger.info("git not found @ %s. Please update %s" % (git_path_string, __file__))
    sys.exit(-1)


def build_sh_string(git_cmd):
    """
    running the return string will start a sh invoking git
    :param git_cmd:
    :return:
    """
    sh_cmd = '"%s" -c %r > %s' % (sh_path_string, git_cmd, log_this_global)

    return sh_cmd


def git(cmd, b_verbose=True):
    """
    Interface to git
    :param cmd: rest of the command after git
    :param b_verbose: True by default.  print command and results to std-out and std-err
    :return:
    """

    local_log_filename = log_this_global

    git_cmd = 'git %s' % cmd

    if b_verbose:
        git_logger.info(git_cmd)

    # ref : https://docs.python.org/2/library/subprocess.html#replacing-os-popen-os-popen2-os-popen3
    # ref : https://docs.python.org/2/library/subprocess.html#subprocess.PIPE
    # p = subprocess.Popen(sh_cmd, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # TODO : how to detect if a process hangs?

    try:
        with open(local_log_filename, 'w') as f_log:
            txt = ''

            # https://docs.python.org/3/library/subprocess.html#subprocess.run
            completed_process = subprocess.run([sh_path_string, '-c', git_cmd, ], stdout=f_log, stderr=f_log)

        if os.path.exists(local_log_filename):
            with open(local_log_filename, 'r', encoding='utf8') as f:
                txt = f.read()
    except UnicodeDecodeError:
        completed_process = subprocess.run([sh_path_string, '-c', git_cmd, ], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        txt = '%s %s' % (completed_process.stdout, completed_process.stderr)

    if b_verbose:
        # http://stackoverflow.com/questions/9348326/regex-find-word-in-the-string
        b_error = is_git_error(txt)
        if b_error:
            git_logger.error(txt)
        else:
            git_logger.info(txt)

    return txt


def is_git_error(txt):
    """
    Whether response from the git command includes error

    :param str txt:
    :return:
    :rtype: bool
    """
    b_error = re.findall(r'^(.*?(\bfatal\b)[^$]*)$', txt, re.I) \
              or re.findall(r'^(.*?(\bCONFLICT\b)[^$]*)$', txt, re.I | re.MULTILINE) \
              or re.findall(r'^(.*?(\berror\b)[^$]*)$', txt, re.I)
    return b_error


def get_current_branch_from_status():
    status_lines = get_git_status_lines()
    return status_lines[0].split()[-1]


def get_git_status_lines(b_verbose=False):
    status = get_git_status(b_verbose)
    status_lines = status.splitlines()
    return status_lines


def get_git_status(b_verbose=False):
    status = git('status', b_verbose)
    return status


def get_behind_from_status(b_verbose=False):
    status_lines = get_git_status_lines(b_verbose)
    # typical response:
    # [0]: On branch master
    # [1]: Your branch is behind 'origin/master' by 9832 commits, and can be fast-forwarded.
    # [2]:   (use "git pull" to update your local branch)
    # [3]: nothing to commit, working tree clean
    second_line = status_lines[1].strip()
    b_start = second_line.startswith('Your branch is behind')
    b_end = second_line.endswith('can be fast-forwarded.')
    return b_start and b_end


def checkout_branch(branch_name):
    git('checkout %s' % branch_name)


def checkout_master():
    checkout_branch('master')


def fetch_and_pull(path):
    """

    :param str path:
    :return:
    :rtype: tuple(str)
    """
    # change to path
    original_full_path = chdir(path)

    result_list = []

    if remote_returns_something():

        if get_current_branch_from_status() != 'master':
            # check out master command
            git('checkout master')

        # fetch command
        result_list.append(git('fetch'))

        # execute pull command
        result_list.append(git('pull --verbose --progress'))

    # change to stored
    os.chdir(original_full_path)

    return tuple(result_list)


def fetch_and_rebase(path, remote='origin', branch='master'):
    # change to path
    original_full_path = chdir(path)

    if remote_returns_something():

        if get_current_branch_from_status() != branch:
            # check out master command
            git('checkout %s' % branch)

        # fetch command
        git_fetch(remote)

        # execute pull branch
        git_rebase_verbose(remote, branch)

    # change to stored
    os.chdir(original_full_path)


def git_fetch(remote_name):
    return git('fetch %s' % remote_name)


def git_fetch_all():
    return git_fetch('--all')


def git_rebase_verbose(remote, branch):
    return git('rebase --verbose %s/%s' % (remote, branch))


def git_checkout(branch):
    return git('checkout %s' % branch)


def git_switch_and_rebase_verbose(remote_name='origin', branch='master'):
    """
    switch to given branch and rebase verbosely

    :param str remote_name:
    :param str branch:
    :return:
    :rtype list[str]
    """
    result = []
    branch_backup = get_current_branch_from_status()

    if branch_backup != branch:
        # check out master branch
        result.append(git_checkout(branch))

    result.append(git_rebase_verbose(remote_name, branch))

    result.append(git_checkout(branch_backup))

    return result


def git_update_mine(path, branch='master', upstream_name='upstream'):
    """

    :param str path:
    :param str branch: 'master' by default
    :param str upstream_name: 'upstream' by default
    :return: responses from git
    :rtype: list(str)
    """
    branch_backup, original_full_path, result = chdir_checkout(path, branch)  # fetch all branches
    git_fetch_result_str = git_fetch_all()

    # possible fetch result:
    # Fetching origin
    # From <scheme>://<netloc>/<path>(.git)
    #    50a80b6e6..b7d2fa35a  master     -> origin/master

    result.append(git_fetch_result_str)

    # if submodule detected, recursively update
    result.append(update_submodule(path))

    # if diff with origin/branch seems to have some content, rebase
    if get_behind_from_status(True):
        # https://felipec.wordpress.com/2013/09/01/advanced-git-concepts-the-upstream-tracking-branch/
        result.append(git('rebase @{u}'))

    if is_upstream_in_remote_list(path):
        if is_branch_in_remote_branch_list(branch, upstream_name):
            upstream_branch = '%s/%s' % (upstream_name, branch)
            diff_upstream_branch = git_diff(branch, upstream_branch)
            result.append(diff_upstream_branch)
            # if diff with upstream/branch seems to have some content, try to rebase
            if diff_upstream_branch:
                result.append(git('rebase %s' % upstream_branch))

    branch_master, git_path_full, result_restore = checkout_chdir(original_full_path, branch_backup)
    result += result_restore

    return result


def git_diff_summary(obj1, obj2):
    return git('diff --summary %s %s' % (obj1, obj2)).strip()


def git_diff(obj1, obj2):
    return git('diff %s %s' % (obj1, obj2)).strip()


def fetch_all_and_rebase(path, branch='master'):
    """
    fetch & rebase from multiple repositories

    :param str path: local repository
    :param str branch:
    :return: list[str]
    """

    branch_backup, original_full_path, result = chdir_checkout(path, branch)# fetch all branches
    result.append(git_fetch_all())

    # https://felipec.wordpress.com/2013/09/01/advanced-git-concepts-the-upstream-tracking-branch/
    result.append(git('rebase @{u}'))

    checkout_chdir(original_full_path, branch_backup)

    return result


def rebase_upstream_branch(path, branch='master', upstream_name='upstream'):
    branch_backup, original_full_path, result = chdir_checkout(path, branch)  # fetch all branches

    if is_upstream_in_remote_list(path):
        if is_branch_in_remote_branch_list(branch, upstream_name):
            result.append(git('rebase %s/%s' % (upstream_name, branch)))

    checkout_chdir(original_full_path, branch_backup)

    return result


def chdir_checkout(path, branch):
    # change to path
    original_full_path = chdir(path)

    # save current branch
    branch_backup = get_current_branch_from_status()
    result = []
    if branch_backup != branch:
        # check out master branch
        result.append(git_checkout(branch))

    return branch_backup, original_full_path, result


def checkout_chdir(original_path, original_branch):
    result = []
    # save current branch
    branch_backup = get_current_branch_from_status()
    if branch_backup != original_branch:
        # check out master branch
        result.append(git_checkout(original_branch))

    # change to path
    current_full_path = chdir(original_path)

    return branch_backup, current_full_path, result


def recursively_process_path(path):
    for root, dirs, files in os.walk(path):
        if ".git" in dirs:
            if '$RECYCLE.BIN' not in root:
                if os.path.exists(os.path.join(os.path.abspath(root), ".git", "index")):
                    git_path = os.path.abspath(root)
                    git_logger.info(time.asctime(), git_path)
                    if "tensorflow" == os.path.split(git_path)[-1] and 'DeepLearningStudyKr' not in git_path:
                        git_logger.info('tensorflow '.ljust(80, '='))
                    if "llvm" == os.path.split(git_path)[-1]:
                        git_logger.info('llvm '.ljust(80, '+'))
                    # todo : if any submodule exist, fetch may be more effective than update?
                    update_submodule(git_path)

                    # begin : skip url
                    if is_host('bitbucket.org', git_path):
                        continue
                    # end skip host url

                    update_repository(git_path)


def update_repository(git_path, remote_list=('origin',), branch='master'):
    """
    if SVN, rebase.  Otherwise fetch_all_and_rebase

    :param str git_path:
    :param list[str] remote_list:
    :param str branch:
    :return:
    """
    """
    :param git_path:
    :return:
    """
    result = None

    if git_has_svn_files(git_path):
        result = svn_rebase(git_path)
    else:
        result = git_update_mine(git_path, branch)

    return result


def get_remote_list(repo_path, b_verbose=True):
    """
    Get the list of names of remote repositories from `git origin` command

    :param str repo_path: repository to list remotes
    :param bool b_verbose: True by default
    :return: tuple containing remote repository names
    :rtype: tuple(str)
    """
    backup_path = chdir(repo_path)

    result_tuple = tuple(git('remote', b_verbose=b_verbose).splitlines())

    os.chdir(backup_path)

    return result_tuple


def is_upstream_in_remote_list(repo_path, b_verbose=False):
    """

    :param str repo_path: repository to list remotes
    :param bool b_verbose: True by default
    :return:
    :rtype: bool
    """
    return 'upstream' in get_remote_list(repo_path, b_verbose=b_verbose)


def get_remote_info_from_git_config(repo_path):
    """
    Return dictionary of remotes of a repository

    {remote_name: {'url'          : url_to_remote_repository,
                   'puttykeyfile' : puttykeyfile_name,
                   'fetch'        : fetch_info}}

    :param string repo_path:
    :return: remote_info_dict
    :rtype: dict

    """
    config_parser = get_git_config_parser(repo_path)

    result = get_section_key(config_parser, 'remote')

    return result


def git_config_branch_info(repo_path):
    """
    Return dictionary of branches of a repository
    :param repo_path: str to repository path
    :return:
    """
    config_parser = get_git_config_parser(repo_path)

    result = get_section_key(config_parser, 'branch')

    return result


def get_section_key(config_parser, section_key):
    """
    from [git config file config parser] object, obtain info with section_key
    :param config_parser:
    :param section_key:
    :return:
    """
    sections = config_parser.sections()
    section_info_dict = {}
    for section in sections:
        if section.startswith(section_key):
            remote_section_name = section[6:].strip().strip('"')

            section_info_dict[remote_section_name] = dict(config_parser.items(section))
    return section_info_dict


def get_git_config_parser(repo_path):
    git_config_path = os.path.join(repo_path, '.git')
    config_file_path = os.path.join(git_config_path, 'config')
    # config parser example, https://wiki.python.org/moin/ConfigParserExamples
    config_parser = cp.ConfigParser(strict=False)
    try:
        config_parser.read(config_file_path, encoding='utf8')
    except UnicodeDecodeError as e:
        config_parser.read(config_file_path, encoding='cp949')

    return config_parser


def get_remote_url_tuple(dir_path):
    remote_info_dict = get_remote_info_from_git_config(dir_path)
    remote_url_tuple = remote_info_dict_to_url_tuple(remote_info_dict)
    return remote_url_tuple


def remote_info_dict_to_url_tuple(remote_info_dict):
    """
    from a dictionary with remote info, find url, and store into a tuple
    :param remote_info_dict:
    :return:
    """
    return tuple(
        map(
            remote_info_item_to_url_item_tuple, iter(remote_info_dict.items())
        )
    )


def remote_info_item_to_url_item_tuple(remote_info_item):
    remote, info_dict = remote_info_item
    remote_info_item_tuple = (remote, info_dict.get('url', None))
    return remote_info_item_tuple


def is_host(host_url, repo_path):
    """
    If the configuration file contains specific url in remote origin, return True
    :param host_url:
    :param repo_path:
    :return:
    """
    def is_host_url_in_info(info_tuple):
        return host_url in info_tuple[1]

    return any(
        map(
            is_host_url_in_info,
            get_remote_url_tuple(repo_path)
        )
    )


def select_path(arg, directory_name, file_name):
    git_logger.info("please do not use %" % (__file__ + '.' + 'select_path()'))
    raise DeprecationWarning


def command_returns_something(command):
    result = git(command, False)
    return 0 < len(result.strip())


def detect_submodule():
    return command_returns_something('submodule')


def remote_returns_something():
    # TODO : check overlap (remote_is_remote(), remote_info())
    return command_returns_something('remote')


def get_submodule_tuple(path):
    git_result = git('submodule').strip().splitlines()
    return tuple(git_result)


def update_submodule(path):
    original_full_path = chdir(path)

    result = ''

    if detect_submodule():
        # git_logger.info('update_submodule()')
        result = git('submodule update --recursive', True)

    # change to stored
    os.chdir(original_full_path)
    return result


def chdir(path):
    # store original path
    original_full_path = os.getcwd()
    # change to path
    os.chdir(path)
    return original_full_path


def git_has_svn_files(root):
    result = False
    svn_path = os.path.join(root, '.git', 'svn')
    if os.path.exists(svn_path):
        if os.listdir(svn_path):
            result = True
    return result


def svn_rebase(path):
    # change to path
    original_full_path = chdir(path)

    result = git('svn rebase')

    # change to stored
    chdir(original_full_path)

    return result


def remote_is_remote(remote_info):
    def server_info_url_is_remote(my_server_info):
        return url_is_remote(my_server_info.get('url', ''))

    return any(map(server_info_url_is_remote, iter(remote_info.values())))


def url_is_remote(url):
    parsed_url = urllib.parse.urlparse(url)
    # https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax

    # https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols
    far_remote_scheme_set = {'https', 'git', 'ssh', 'http'}

    return parsed_url.scheme in far_remote_scheme_set


def get_remote_url_list(remote_info):
    def get_url(my_server_info):
        return my_server_info.get('url', '')

    return list(map(get_url, iter(remote_info.values())))


def get_far_remote_name_list(remote_info):
    def remote_url_is_remote(remote_name):
        return url_is_remote(remote_info[remote_name].get('url', ''))

    return list(filter(remote_url_is_remote, iter(remote_info.keys())))


def get_tag_local_list(b_verbose=False):
    result_txt = git('tag', b_verbose=b_verbose)
    result_list = result_txt.splitlines()
    return result_list


def get_ls_remote_list(pattern_str, repo_name='origin', b_verbose=False):
    cmd_remote_txt = 'ls-remote --%s %s' % (pattern_str, repo_name)
    result_txt = git(cmd_remote_txt, b_verbose=b_verbose)
    result_hash_list = result_txt.splitlines()
    # http://stackoverflow.com/questions/16398471/regex-not-ending-with
    re_pattern = re.compile(r'refs/%s/(.+)(?<!\^\{\})$' % pattern_str)
    result_list_list = [re_pattern.findall(hash_txt) for hash_txt in result_hash_list]
    result_list_list_filtered = [_f for _f in result_list_list if _f]
    result_list = [found_list[0] for found_list in result_list_list_filtered]
    return result_list


def get_remote_tag_list(repo_name='origin', b_verbose=False):
    # http://stackoverflow.com/questions/20734181/how-to-get-list-of-latest-tags-in-remote-git
    return get_ls_remote_list('tags', repo_name, b_verbose)


def get_remote_branch_list(repo_name='origin', b_verbose=False):
    # http://stackoverflow.com/questions/3471827/how-do-i-list-all-remote-branches-in-git-1-7
    return get_ls_remote_list('heads', repo_name, b_verbose)


def is_branch_in_remote_branch_list(branch_name, repo_name='origin', b_verbose=False):
    return branch_name in get_remote_branch_list(repo_name, b_verbose)


def git_tag_local_repo(tag_name_txt, repo_name='origin', b_verbose=False):
    # http://minsone.github.io/git/git-addtion-and-modified-delete-tag
    cmd_local_txt = 'tag %s' % tag_name_txt
    cmd_remote_txt = 'push %s %s' % (repo_name, tag_name_txt)
    result_local = git(cmd_local_txt, b_verbose=b_verbose)
    result_remote = git(cmd_remote_txt, b_verbose=b_verbose)
    result = {'local': result_local,
              'remote': result_remote}
    return result


def delete_a_tag_local_repo(tag_name_txt, repo_name='origin', b_verbose=False):
    # https://nathanhoad.net/how-to-delete-a-remote-git-tag
    cmd_local_txt = 'tag -d %s' % tag_name_txt
    cmd_remote_txt = 'push %s :refs/tags/%s' % (repo_name, tag_name_txt)
    result_local = git(cmd_local_txt, b_verbose=b_verbose)

    repo_tag_list = get_remote_tag_list(repo_name)
    result_remote = '(tag %s not in repository %s tag list)' % (tag_name_txt, repo_name)

    if tag_name_txt in repo_tag_list:
        result_remote = git(cmd_remote_txt, b_verbose=b_verbose)

    result = {'local': result_local,
              'remote': result_remote}
    return result


def delete_all_tags_local_repo(repo_name='origin', b_verbose=False):
    local_tag_list = get_tag_local_list(b_verbose)
    result = []
    for tag_name_txt in local_tag_list:
        result_tag_dict = delete_a_tag_local_repo(tag_name_txt, repo_name, b_verbose)
        result_tag_dict['tag_name'] = tag_name_txt
        result.append(result_tag_dict)

    return result


if "__main__" == __name__:
    git('log')
