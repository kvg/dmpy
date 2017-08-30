#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='dmpy',
    version='0.8.2',
    description='Distributed Make for Python',
    author='Kiran Garimella',
    author_email='kiran.garimella@gmail.com',
    packages=find_packages(exclude=('tests', 'docs')),
)
