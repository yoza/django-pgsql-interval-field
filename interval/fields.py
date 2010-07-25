# -*- encoding: utf-8 -*-

from django.db import models

from datetime import time, timedelta


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



class IntervalField(models.Field):
    """PostgreSQL's INTERVAL type; maps to Python datetime.timedelta
    """

    __metaclass__ = models.SubfieldBase

    def db_type(self):
        return "INTERVAL"


    def to_python(self, value):

        if value is None or value is '':
            return None

        if isinstance(value, timedelta):
            return value

        return timedelta(seconds = float(value)) # string form - for json


    def get_db_prep_value(self, value):
        if value is None or value is '': return None
        return timedelta_topgsqlstring(value)



try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^interval\.fields\.IntervalField"])
except ImportError:
    pass

