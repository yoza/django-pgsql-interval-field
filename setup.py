# -*- encoding: utf-8 -*-

from setuptools import setup

setup(
    name='django-pgsql-interval-field',
    version='0.9',
    author=u'Michał Pasternak - FHU Kagami',
    author_email='michal.dtz@gmail.com',
    url='http://code.google.com/p/django-pgsql-interval-field/',
    license='MIT',
    description='Support for PostgreSQL INTERVAL for Django',
    packages=['interval', 'interval.static'],
    install_requires=['django'],
    zip_safe=False)
