# -*- encoding: utf-8 -*-

import os

setupdict = dict(
    name = 'django-pgsql-interval-field',
    version = '0.2',
    author = u'Michał Pasternak - FHU Kagami',
    author_email = 'michal.dtz@gmail.com',
    url = 'http://fhu-kagami.pl/',
    license = 'MIT',
    packages = ['interval'])

try:
    from setuptools import setup
    setupdict['include_package_data'] = True
    setupdict['install_requires'] = ['django']
    setupdict['zip_safe'] = False

except ImportError:
    from distutils.core import setup
    setupdict['requires'] = ['django']

setup(**setupdict)
