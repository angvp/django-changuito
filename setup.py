#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-changuito',
    version='2.0',
    description='A fork of django-cart with the same simplicity but updated',
    maintainer='Angel Velasquez',
    maintainer_email='angvp@archlinux.org',
    license="LGPL v3",
    url='https://github.com/angvp/django-changuito',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
