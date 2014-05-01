#!/usr/bin/env python

from distutils.core import setup

description = open('README.md').read()

setup(name='y4m',
      version='1.1.1',
      description='YUV4MPEG2 (.y4m) Reader/Writer',
      author='Pierre Gronlier',
      author_email='ticapix@gmail.com',
      url='https://github.com/ticapix/python-y4m',
      packages=['y4m'],
      long_description=description
     )

#python ./setup.py register sdist upload
