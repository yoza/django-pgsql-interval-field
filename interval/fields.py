# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings

from datetime import time, timedelta

day_seconds = 24 * 60 * 60
microseconds = 1000000


def timedelta_topgsqlstring(value):
    buf = ''
    if value.microseconds:
        buf += ' %i MICROSECONDS ' % value.microseconds

    if value.seconds:
        buf += ' %i SECONDS ' % value.seconds

    if value.days:
        buf += ' %i DAYS ' % value.days

    if not buf:
        buf = '0'

    return buf


def timedelta_tobigint(value):
    return (value.days * day_seconds + value.seconds + value.microseconds) * microseconds



class IntervalField(models.Field):
    """This is a field, which maps to Python's datetime.timedelta.

    For PostgreSQL, its type is INTERVAL - a native interval type.
    - http://www.postgresql.org/docs/8.4/static/datatype-datetime.html

    For other databases, its type is BIGINT and timedelta value is stored
    as number of seconds * 1000000 . 
    """

    __metaclass__ = models.SubfieldBase

    def db_type(self):
        if settings.DATABASE_ENGINE == 'postgresql_psycopg2':
            return 'INTERVAL'

        return 'BIGINT'
        

    def to_python(self, value):

        if value is None or value is '':
            return None

        if isinstance(value, timedelta):
            # PostgreSQL
            return value

        # string in form like "HH:MM:SS.ms" (can be used in fixture files)
        if (isinstance(value, str) or isinstance(value, unicode)) and value.find(":") >= 0:
            try:
                h, m, s = value.split(":")
            except ValueError, e:
                raise ValueError, "please use HH:MM:SS[.ms] format instead of %r" % value

            try:
                h = int(h)
            except ValueError, e:
                raise ValueError, "hours are not an integer in %r" % value

            try:
                m = int(m)

                if m > 59 or m < 0: 
                    raise ValueError

            except ValueError, e:
                raise ValueError, "minutes are not a positive integer or exceed 59 in %r" % value

            if s.find(".") >= 0:
                s, ms = s.split(".")
            else:
                ms = 0

            try:
                s = int(s)

                if s > 59 or s < 0:
                    raise ValueError

            except ValueError, e:
                raise ValueError, "seconds are not a positive integer or exceed 59 in %r" % value

            try:
                ms = int(ms) * (microseconds/10)
                
                if ms > microseconds or ms < 0:
                    raise ValueError

            except ValueError, e:
                raise ValueError, "microseconds are not a positive integer or exceed %s in %r" % (microseconds, value)

            return timedelta(hours = h, minutes = m, seconds = s, microseconds = ms)

        # other database backends:
        return timedelta(seconds = float(value) / microseconds ) # string form - for json


    def get_db_prep_value(self, value):

        if value is None or value is '': return None

        if settings.DATABASE_ENGINE == 'postgresql_psycopg2':
            return timedelta_topgsqlstring(value)

        return timedelta_tobigint(value)



try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^interval\.fields\.IntervalField"])
except ImportError:
    pass

