# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='python-music-theory',
    version='0.1.0',
    description='Python Music Theory Library',
    long_description=readme,
    author='David Floegel, Jason Cook, Clemens Westrup',
    author_email='mail@davidfloegel.com',
    url='https://github.com/davidfloegel/python-music-theory',
    packages=find_packages(exclude=('tests', 'docs'))
)
