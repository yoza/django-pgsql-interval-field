# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings

from datetime import time, timedelta

day_seconds = 24 * 60 * 60
miliseconds = 1000000


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
    return (value.days * day_seconds + value.seconds + value.microseconds) * miliseconds



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

        # other database backends:
        return timedelta(seconds = float(value) / miliseconds ) # string form - for json


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

