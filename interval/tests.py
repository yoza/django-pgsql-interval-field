# -*- encoding: utf-8 -*-

from testutil import TestCase
from datetime import timedelta
from interval.fields import IntervalField

class TestIntervalField(TestCase):
    def test_functions(self):
        """Testuje poszczególne funkcje klasy IntervalField,
        bez użycia jakiegoś konkretnego backendu bazodanowego."""

        a = IntervalField()
        self.assertEquals(a.to_python(timedelta(seconds = 5)), timedelta(seconds = 5))
        self.assertEquals(a.to_python(None), None)
        self.assertEquals(a.to_python(10.123), timedelta(seconds = 10, microseconds = 123000))

        self.assertEquals(a.get_db_prep_value(None), None)
        self.assertEquals(a.get_db_prep_value(timedelta(seconds = 10)), ' 10 SECONDS ')

