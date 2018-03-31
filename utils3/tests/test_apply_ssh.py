import os
import unittest
from .. import apply_ssh as apply_ssh


current_path = os.getcwd()
# os.chdir(os.pardir)


class TestApplySSHbitbucket(unittest.TestCase):
    def setUp(self):
        root_path = os.getcwd()
        file_name_spec = ''
        self.applier = apply_ssh.ApplySSHbitbucket(root_path, file_name_spec)

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


class TestApplySSHgithub(unittest.TestCase):
    def setUp(self):
        root_path = os.getcwd()
        file_name_spec = ''
        self.applier = apply_ssh.ApplySSHgithub(root_path, file_name_spec)

    def test_convert_url_https_to_ssh(self):
        result01 = self.applier.convert_url_https_to_ssh(r'https://abc@github.com/geekcomputers/Python.git')
        expected01 = 'ssh://git@github.com-abc/geekcomputers/Python.git'
        self.assertEqual(expected01, result01)


if __name__ == '__main__':
    unittest.main()
