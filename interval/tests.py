# -*- encoding: utf-8 -*-

from testutil import TestCase

from datetime import timedelta

from interval.fields import IntervalField, miliseconds

from django.conf import settings

class TestIntervalField(TestCase):
    def test_functions(self):
        """Test functions of IntervalField without using any 
        specific database backend."""
        
        orig_dbe = settings.DATABASE_ENGINE

        settings.DATABASE_ENGINE = 'postgresql_psycopg2'

        a = IntervalField()
        self.assertEquals(a.to_python(timedelta(seconds = 5)), timedelta(seconds = 5))
        self.assertEquals(a.to_python(None), None)
        self.assertEquals(a.to_python(10.123 * miliseconds), timedelta(seconds = 10, microseconds = 123000))

        self.assertEquals(a.get_db_prep_value(None), None)
        self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), ' 10 SECONDS ')

        settings.DATABASE_ENGINE = 'something_else_than_pgsql'

        a = IntervalField()
        self.assertEquals(a.to_python(timedelta(seconds = 5)), timedelta(seconds = 5))
        self.assertEquals(a.to_python(None), None)
        self.assertEquals(a.to_python(10.123 * miliseconds), timedelta(seconds = 10, microseconds = 123000))

        self.assertEquals(a.get_db_prep_value(None), None)
        self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), 10 * miliseconds)

        # Leave everything as it was
        settings.DATABASE_ENGINE = orig_dbe


