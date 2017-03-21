# -*- coding: utf8 -*-
"""
Recursively Find in Files
"""
import os
import sys


class RecursiveFinderBase(object):
    def __init__(self, root_path):
        # constructor
        self.root = root_path

        # for os dependent Korean encoding
        # http://www.stackoverflow.com/questions/1854/how-to-check-what-os-am-i-running-on-in-python
        self.path_encoding_dict = {'posix': 'utf8', 'nt': 'cp949'}
        self.path_encoding = self.path_encoding_dict[os.name]

    def recursively_find_in(self):
        # major function
        for dir_path, dir_names, file_names in os.walk(self.root):
            self.process_folder(unicode(dir_path, self.path_encoding), dir_names, file_names)

    def process_folder(self, dir_path, dir_names, file_names):
        for filename in file_names:
            self.process_file(dir_path, filename)

    def process_file(self, dir_path, filename):
        # find in file and process if found
        raise NotImplementedError


class RecursiveFinder(RecursiveFinderBase):
    def __init__(self, root_path, ext, target):
        # constructor
        super(RecursiveFinder, self).__init__(root_path)
        self.ext = ext
        self.target = target

        self.recursively_find_in()

    def is_ext(self, filename):
        # file extension check
        return os.path.splitext(filename)[-1].endswith(self.ext)

    def process_file(self, dir_path, filename):
        # find in file and process if found
        if self.is_ext(filename):
            found = False
            with open(os.path.join(dir_path, filename), 'r') as f:
                txt = f.read()
                found = self.target in txt

            if found:
                print("%s" % os.path.join(dir_path, filename))


def main():
    if 4 == len(sys.argv):

        root_path = sys.argv[1]
        ext = sys.argv[2]
        target = sys.argv[3]

        do_it = RecursiveFinder(root_path, ext, target)


if __name__ == '__main__':
    main()
