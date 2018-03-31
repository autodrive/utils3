# -*- coding: utf-8 -*-
# @kennethreitz, setup.py, https://github.com/kennethreitz/samplemod
# @kennethreitz, setup.py, https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='utils3',
    version='0.1.0',
    description='My utilities for python',
    long_description=readme,
    author='autodrive',
    author_email='',
    url='https://github.com/autodrive/utils3',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
