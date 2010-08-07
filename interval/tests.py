# -*- encoding: utf-8 -*-

from testutil import TestCase

from datetime import timedelta

from interval.fields import IntervalField, microseconds

from django.conf import settings

class TestIntervalField(TestCase):
    def test_functions(self):
        """Test functions of IntervalField without using any 
        specific database backend."""
        
        def do_some_tests():
            """We don't actually touch the DB in those tests."""

            valid_strings = ["00:00:00", "00:00:00.0",
                             "10:10:10", "10:10:10.10",
                             "5 days, 22:22:22.22",
                             "5 days, 22:22:22",
                             "1 day, 0:00:00",
                             "00:00:00.22",
                             "00:00:00.222",
                             "00:00:00.2222",
                             "00:00:00.22222",
                             "00:00:00.22222",
                             "00:00:00.222222",
                             "00:00:00.12345672930923890"]

            invalid_strings = ["10:-10:10", "10:10:-10",
                               "00:00:00.-100", "00:62:00", 
                               "00:00:61", 
                               "xx days, 12:12:12.123",
                               "12 dayz, 00:00:00"]

            a = IntervalField()
            self.assertEquals(a.to_python(timedelta(seconds = 5)), timedelta(seconds = 5))
            self.assertEquals(a.to_python("00:00:05.1"), timedelta(seconds = 5, microseconds = 100000))
            self.assertEquals(a.to_python("2 days, 00:00:05.1"), 	timedelta(days = 2, seconds = 5, microseconds = 100000))
            self.assertEquals(a.to_python("2 days, 00:00:05.01"), 	timedelta(days = 2, seconds = 5, microseconds = 10000))
            self.assertEquals(a.to_python("2 days, 00:00:05.001"), 	timedelta(days = 2, seconds = 5, microseconds = 1000))
            self.assertEquals(a.to_python("2 days, 00:00:05.0001"), 	timedelta(days = 2, seconds = 5, microseconds = 100))
            self.assertEquals(a.to_python("2 days, 00:00:05.00001"), 	timedelta(days = 2, seconds = 5, microseconds = 10))
            self.assertEquals(a.to_python("2 days, 00:00:05.000001"), 	timedelta(days = 2, seconds = 5, microseconds = 1))

            for s in valid_strings:
                a.to_python(s)

            for s in invalid_strings:
                self.assertRaises(ValueError, a.to_python, s)

            self.assertEquals(a.to_python(None), None)
            self.assertEquals(a.to_python(10.123 * microseconds), timedelta(seconds = 10, microseconds = 123000))

            self.assertEquals(a.get_db_prep_value(None), None)

            if settings.DATABASE_ENGINE == 'postgresql_psycopg2':
                self.assertEquals(a.db_type(), 'INTERVAL')
                self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), ' 10 SECONDS ')
            else:
                self.assertEquals(a.db_type(), 'BIGINT')
                self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), 10 * microseconds)


        
        orig_dbe = settings.DATABASE_ENGINE

        settings.DATABASE_ENGINE = 'postgresql_psycopg2'
        do_some_tests()

        settings.DATABASE_ENGINE = 'something_else_than_pgsql'
        do_some_tests()

        # Leave everything as it was
        settings.DATABASE_ENGINE = orig_dbe


