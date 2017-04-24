# -*- coding: utf8 -*-
"""
Git utility with interfaces

Will create a git_util.ini during import if missing (may take some time)

includes other utility functions
"""
import configparser as cp
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

    return git_path, sh_path, log_this, log_cumulative


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
    config_file = open(git_configuration['config_filename'], 'w')
    config_parser.write(config_file)
    config_file.close()


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


git_path_string, sh_path_string, log_this_global, log_cumulative_global = initialize()

if not os.path.exists(git_path_string.strip('"')):
    print("git not found @ %s. Please update %s" % (git_path_string, __file__))
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
    long_log_filename = log_cumulative_global

    git_cmd = 'git %s' % cmd
    sh_cmd = build_sh_string(git_cmd)

    if b_verbose:
        print(sh_cmd)

    # ref : https://docs.python.org/2/library/subprocess.html#replacing-os-popen-os-popen2-os-popen3
    # ref : https://docs.python.org/2/library/subprocess.html#subprocess.PIPE
    # p = subprocess.Popen(sh_cmd, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # TODO : how to detect if a process hangs?

    with open(local_log_filename, 'w') as f_log:

        # https://docs.python.org/3/library/subprocess.html#subprocess.run
        completed_process = subprocess.run([sh_path_string, '-c', git_cmd, ], stdout=f_log, stderr=f_log)
    # os.system(sh_cmd)

    txt = ''
    if os.path.exists(local_log_filename):
        with open(local_log_filename, 'r') as f:
            txt = f.read()

    with open(long_log_filename, 'a') as f:
        f.write('%s\n%s\n' % (sh_cmd, txt))

    if b_verbose:
        print(txt)

    return txt


def current_branch():
    status = git('status', False)
    status_lines = status.splitlines()
    return status_lines[0].split()[-1]


def checkout_branch(branch_name):
    git('checkout %s' % branch_name)


def checkout_master():
    checkout_branch('master')


def fetch_and_pull(path):
    # store original path
    original_full_path = os.path.abspath(os.curdir)

    # change to path
    os.chdir(path)

    if remote_returns_something():

        if current_branch() != 'master':
            # check out master command
            git('checkout master')

        # fetch command
        git('fetch')

        # execute pull command
        git('pull --verbose --progress')

    # change to stored
    os.chdir(original_full_path)


def fetch_and_rebase(path, remote='origin', branch='master'):
    # store original path
    original_full_path = os.path.abspath(os.curdir)

    # change to path
    os.chdir(path)

    if remote_returns_something():

        if current_branch() != branch:
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
    branch_backup = current_branch()

    if branch_backup != branch:
        # check out master branch
        result.append(git_checkout(branch))

    result.append(git_rebase_verbose(remote_name, branch))

    result.append(git_checkout(branch_backup))

    return result


def fetch_all_and_rebase(path, branch='master'):
    """
    fetch & rebase from multiple repositories

    :param str path: local repository
    :param str branch:
    :return: list[str]
    """

    # store original path
    original_full_path = os.path.abspath(os.curdir)

    # change to path
    os.chdir(path)

    # save current branch
    branch_backup = current_branch()

    result = []

    if branch_backup != branch:
        # check out master branch
        result.append(git_checkout(branch))

    # fetch all branches
    result.append(git('fetch --all'))

    # https://felipec.wordpress.com/2013/09/01/advanced-git-concepts-the-upstream-tracking-branch/
    result.append(git('rebase @{u}'))

    # restore branch
    if branch_backup != branch:
        result.append(git_checkout(branch_backup))

    # change to stored
    os.chdir(original_full_path)

    return result


def recursively_process_path(path):
    for root, dirs, files in os.walk(path):
        if ".git" in dirs:
            if '$RECYCLE.BIN' not in root:
                if os.path.exists(os.path.join(os.path.abspath(root), ".git", "index")):
                    git_path = os.path.abspath(root)
                    print(time.asctime(), git_path)
                    if "tensorflow" == os.path.split(git_path)[-1] and 'DeepLearningStudyKr' not in git_path:
                        print('tensorflow '.ljust(80, '='))
                    if "llvm" == os.path.split(git_path)[-1]:
                        print('llvm '.ljust(80, '+'))
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
        result = fetch_all_and_rebase(git_path, branch)

    return result


def get_remote_list(repo_path, b_verbose=True):
    """
    Get the list of names of remote repositories from `git origin` command

    :param str repo_path: repository to list remotes
    :param bool b_verbose: True by default
    :return: tuple containing remote repository names
    :rtype: tuple(str)
    """
    backup_path = os.path.abspath(os.curdir)
    os.chdir(repo_path)

    result_tuple = tuple(git('remote', b_verbose=b_verbose).splitlines())

    os.chdir(backup_path)

    return result_tuple


def is_upstream_in_remote_list(repo_path, b_verbose=True):
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
    print("please do not use %" % (__file__ + '.' + 'select_path()'))
    raise


def command_returns_something(command):
    result = git(command, False)
    return 0 < len(result.strip())


def detect_submodule():
    return command_returns_something('submodule')


def remote_returns_something():
    # TODO : check overlap (remote_is_remote(), remote_info())
    return command_returns_something('remote')


def update_submodule(path):
    # store original path
    original_full_path = os.path.abspath(os.curdir)

    # change to path
    os.chdir(path)

    if detect_submodule():
        print('update_submodule()')
        git('submodule update --recursive', False)

    # change to stored
    os.chdir(original_full_path)


def git_has_svn_files(root):
    result = False
    svn_path = os.path.join(root, '.git', 'svn')
    if os.path.exists(svn_path):
        if os.listdir(svn_path):
            result = True
    return result


def svn_rebase(path):
    # store original path
    original_full_path = os.path.abspath(os.curdir)

    # change to path
    os.chdir(path)

    result = git('svn rebase')

    # change to stored
    os.chdir(original_full_path)

    return result


def remote_is_remote(remote_info):
    def server_info_url_is_remote(my_server_info):
        return url_is_remote(my_server_info.get('url', ''))

    return any(map(server_info_url_is_remote, iter(remote_info.values())))


def url_is_remote(url):
    parsed_url = urllib.parse.urlparse(url)
    # https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax

    # https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols
    far_remote_scheme_tuple = ('https', 'git', 'ssh')

    return parsed_url.scheme in far_remote_scheme_tuple


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


def get_tag_repo_list(repo_name='origin', b_verbose=False):
    # http://stackoverflow.com/questions/20734181/how-to-get-list-of-latest-tags-in-remote-git
    cmd_remote_txt = 'ls-remote --tags %s' % repo_name
    result_txt = git(cmd_remote_txt, b_verbose=b_verbose)
    result_hash_list = result_txt.splitlines()
    # http://stackoverflow.com/questions/16398471/regex-not-ending-with
    result_list_list = [re.findall(r'refs/tags/(.+)(?<!\^\{\})$', hash_txt) for hash_txt in result_hash_list]
    result_list_list_filtered = [_f for _f in result_list_list if _f]
    result_list = [found_list[0] for found_list in result_list_list_filtered]
    return result_list


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

    repo_tag_list = get_tag_repo_list(repo_name)
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
