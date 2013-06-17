#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

required = ['jsonfield']

setup(
        name='django-changuito',
        version='0.1',
        description='A fork of django-cart with the same simplicity but up-to-date',
        maintainer='Angel Velasquez',
        maintainer_email='angvp@archlinux.org',
        license="LGPL v3",
        url='https://github.com/angvp/django-changuito',
        packages=['changuito'],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: LGPL",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
     )
