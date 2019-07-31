import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import find_in
import git_util


# TODO : git-svn remote info?

class RecursiveGitRepositoryFinderBase(find_in.RecursiveFinderBase):
    """
    Base class for git repository searchers
    """
    def __init__(self, root_path, file_name_spec, b_verbose=False):
        super(RecursiveGitRepositoryFinderBase, self).__init__(root_path)

        self.filename_spec = file_name_spec
        self.found_set = set()
        self.git_path_name = '.git'
        self.b_verbose = b_verbose

    def is_git_repository(self, dir_path, dir_names):
        """
        Check if given dir_path has a sub folder for git with config file
        :param dir_path:
        :param dir_names:
        :return:
        """
        result = False
        if self.git_path_name in dir_names:
            path_to_config = os.path.join(dir_path, self.git_path_name, 'config')
            if os.path.exists(path_to_config):
                if os.path.isfile(path_to_config):
                    result = True

        return result

    def process_folder(self, dir_path, dir_names, filename):
        if self.is_git_repository(dir_path, dir_names):
            self.process_git_folder(dir_path)

    def add_to_found(self, dir_path):
        self.found_set.add(dir_path)

    def process_git_folder(self, dir_path):
        # indicate git repository location & remote info tuple
        self.add_to_found(dir_path)
        if self.b_verbose:
            remote_url_tuple = git_util.get_remote_url_tuple(dir_path)
            git_util.git_logger.info('%s %s' % (dir_path, remote_url_tuple))


class RecursiveGitRepositoryFinder(RecursiveGitRepositoryFinderBase):
    def __init__(self, root_path, file_name_spec, b_verbose=False):
        RecursiveGitRepositoryFinderBase.__init__(self, root_path, file_name_spec, b_verbose)
        self.recursively_find_in()


def find_git_repos(root_path=os.path.expanduser('~'), b_verbose=True):
    """
    Recursively find git repositories
    :param root_path: Where to start search
    :return:
    """

    return RecursiveGitRepositoryFinder(root_path, 'config', b_verbose=b_verbose)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        find_git_repos(sys.argv[1])
    else:
        find_git_repos()
