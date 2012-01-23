# -*- encoding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='django-pgsql-interval-field',
    version='0.9',
    author=u'Michał Pasternak - FHU Kagami',
    author_email='michal.dtz@gmail.com',
    url='http://code.google.com/p/django-pgsql-interval-field/',
    license='MIT',
    description='Support for PostgreSQL INTERVAL for Django',
    packages=find_packages(exclude='test_project'),
    package_data={'interval': [
        'static/interval.css',
        'locale/pl/LC_MESSAGES/django.mo',
        'locale/pl/LC_MESSAGES/django.po',
    ]},
    install_requires=['django'],
    zip_safe=False)
