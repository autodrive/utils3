import os
import unittest

current_path = os.path.abspath(os.curdir)
os.chdir(os.pardir)

import apply_ssh


class TestApplySSH(unittest.TestCase):
    def setUp(self):
        root_path = os.path.abspath(os.curdir)
        file_name_spec = ''
        self.applier = apply_ssh.ApplySSH(root_path, file_name_spec)

    def tearDown(self):
        del self.applier

    def test_is_target(self):
        self.assertTrue(self.applier.is_target('https://bitbucket.org/pyslide.git'))
        self.assertFalse(self.applier.is_target(None))
        self.assertFalse(self.applier.is_target('https://github.com/torch/torch7.git'))

    def test_convert_url_https_to_ssh(self):
        result01 = self.applier.convert_url_https_to_ssh('https://abc@bitbucket.org/pyslide.git')
        expected01 = 'ssh://git@bitbucket.org/pyslide.git'
        self.assertEqual(expected01, result01)


if __name__ == '__main__':
    unittest.main()
