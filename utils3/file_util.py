# -*- coding: utf8 -*-


def read_txt(filename):
    with open(filename, 'rt') as f:
        txt = f.read()
    return txt


def read_txt_lines(filename):
    with open(filename, 'rt') as f:
        txt_lines = f.readlines()
    # return result
    return txt_lines
