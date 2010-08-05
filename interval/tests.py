# -*- encoding: utf-8 -*-

from testutil import TestCase

from datetime import timedelta

from interval.fields import IntervalField, microseconds

from django.conf import settings

class TestIntervalField(TestCase):
    def test_functions(self):
        """Test functions of IntervalField without using any 
        specific database backend."""
        
        orig_dbe = settings.DATABASE_ENGINE

        settings.DATABASE_ENGINE = 'postgresql_psycopg2'

        valid_strings = ["00:00:00", "00:00:00.0",
                         "10:10:10", "10:10:10.10"]

        invalid_strings = ["10:-10:10", "10:10:-10",
                           "00:00:00.-100", "00:62:00", 
                           "00:00:61", "00:00:00.1234567890"]

        a = IntervalField()
        self.assertEquals(a.to_python(timedelta(seconds = 5)), timedelta(seconds = 5))
        self.assertEquals(a.to_python("00:00:05.1"), timedelta(seconds = 5, microseconds = 100000))

        for s in valid_strings:
            a.to_python(s)

        for s in invalid_strings:
            self.assertRaises(ValueError, a.to_python, s)

        self.assertEquals(a.to_python(None), None)
        self.assertEquals(a.to_python(10.123 * microseconds), timedelta(seconds = 10, microseconds = 123000))

        self.assertEquals(a.get_db_prep_value(None), None)
        self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), ' 10 SECONDS ')

        settings.DATABASE_ENGINE = 'something_else_than_pgsql'

        a = IntervalField()
        self.assertEquals(a.to_python(timedelta(seconds = 5)), timedelta(seconds = 5))
        self.assertEquals(a.to_python("00:00:05.1"), timedelta(seconds = 5, microseconds = 100000))
        self.assertEquals(a.to_python(None), None)
        self.assertEquals(a.to_python(10.123 * microseconds), timedelta(seconds = 10, microseconds = 123000))

        self.assertEquals(a.get_db_prep_value(None), None)
        self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), 10 * microseconds)

        # Leave everything as it was
        settings.DATABASE_ENGINE = orig_dbe


