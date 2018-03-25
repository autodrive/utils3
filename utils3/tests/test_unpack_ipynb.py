import unittest
from utils3.utils3.tests.test_git_util import MyTestGitUtilBase
import os

import utils3.utils3.unpack_ipynb as unpack
import math


class TestUnpackIpythonNotebookOneFile(MyTestGitUtilBase):
    def setUp(self):
        super(TestUnpackIpythonNotebookOneFile, self).setUp()

        self.test_file_name = tuple([os.path.join(self.test_path, filename) for filename in ('test_unpack_00', 'test_unpack_01')])
        self.sample_file_indicator = 'sample'
        self.python_ext = 'py'
        self.notebook_ext = 'ipynb'
        self.sample_ext = 'txt'

        self.del_py_if_exists()

    def del_py_if_exists(self):
        for test_file_name in self.test_file_name:
            expected_py_name = self.make_py_full_path(test_file_name)
            if os.path.exists(expected_py_name):
                os.remove(expected_py_name)

    def make_py_full_path(self, test_file_name):
        return os.path.abspath('.'.join((test_file_name, self.python_ext)))

    def make_sample_file_name(self, test_file_name):
        return '_'.join((test_file_name, self.sample_file_indicator))

    def test_unpack(self):
        for test_file_name in self.test_file_name:
            expected_py_name = self.make_py_full_path(test_file_name)
            test_sample_file_name = self.make_sample_file_name(test_file_name)
            expected_py_sample_name = os.path.abspath('.'.join((test_sample_file_name, self.sample_ext)))
            expected_nb_name = os.path.abspath('.'.join((test_file_name, self.notebook_ext)))

            if not os.path.exists(expected_nb_name):
                raise IOError("File %.150s missing" % expected_nb_name)

            # function under tests
            unpack.unpack(expected_nb_name, b_verbose=True)

            with open(expected_py_name, encoding='utf8') as py_file:
                py_txt = py_file.readlines()

                with open(expected_py_sample_name, encoding='utf8') as py_sample_file:
                    py_sample_txt = py_sample_file.readlines()

                    formatter = '%0' + str(int(math.log10(max(len(py_txt), len(py_sample_txt)))) + 1) +'d] %r != %r'

                    line_counter = 0
                    for py, sample in zip(py_txt, py_sample_txt):
                        line_counter += 1
                        message = formatter % (line_counter, py, sample)
                        self.assertEqual(py, sample, msg=message)

                    self.assertEqual(len(py_txt), len(py_sample_txt))

    def test_convert_heading(self):
        cd = {'source': ["Fraud detection with Benford's law"], 'cell_type': 'heading', 'level': 1, 'metadata': {}}
        result = unpack.convert_heading(cd)
        expected = '''############################################################
# Fraud detection with Benford's law
############################################################
'''
        for member in cd['source']:
            self.assertIn(member, result)

    def test_find_py_name_from_run_magic_cmd(self):
        code = '%run phugoid.py'
        result = unpack.find_py_name_from_run_magic_cmd(code)
        expected = 'phugoid'
        self.assertEqual(expected, result)

    def tearDown(self):
        self.del_py_if_exists()


if __name__ == '__main__':
    unittest.main()
