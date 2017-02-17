import unittest

import config_util


class TestConfigUtilGeneric(unittest.TestCase):
    def setUp(self):
        self.filename = 'generic_config'

    def test_file_read_line_strip(self):
        f = config_util.FileReadLineStrip(self.filename)

        txt = f.readline()
        result = [txt]
        while txt:
            txt = f.readline()
            if txt:
                result.append(txt)
        # reading done

        for line in result:
            self.assertEqual(line[:-1], line.strip())

    def test_my_config_util_read(self):
        config_parser = config_util.MyRawConfigParser()
        config_parser.read(self.filename)

        self.check_generic_config(config_parser)

    def test_my_config_util_readfp(self):
        fp = open(self.filename)
        config_parser = config_util.MyRawConfigParser()
        config_parser.readfp(fp)

        self.check_generic_config(config_parser)

    def check_generic_config(self, config_parser):
        result_c = config_parser.get('a', 'b')
        self.assertEqual('c', result_c)
        result_f = config_parser.get('d', 'e')
        self.assertEqual('f', result_f)
        result_i = config_parser.get('g', 'h')
        self.assertEqual('i', result_i)


class TestConfigUtilGitUtil(TestConfigUtilGeneric):
    def setUp(self):
        self.filename = 'git_util.ini'

    def check_generic_config(self, config_parser):
        result_a = config_parser.get('git', 'path')
        self.assertEqual('a', result_a)
        result_c = config_parser.get('log', 'cumulative')
        self.assertEqual('c', result_c)
        result_b = config_parser.get('log', 'this')
        self.assertEqual('b', result_b)
