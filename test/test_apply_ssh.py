import os
import unittest

current_path = os.path.abspath(os.curdir)
os.chdir(os.pardir)

import apply_ssh


class TestApplySSH(unittest.TestCase):
    def test_init(self):
        root_path = os.path.abspath(os.curdir)
        file_name_spec = ''
        applier = apply_ssh.ApplySSH(root_path, file_name_spec)
        self.assertTrue(applier.finder.findall('https://bitbucket.org/pyslide.git'))


if __name__ == '__main__':
    unittest.main()
