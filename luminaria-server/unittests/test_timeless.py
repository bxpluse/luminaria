import unittest

from common.timeless import Interval


class TestTimelessMethods(unittest.TestCase):

    def test_interval_15(self):
        # Standard incrementing test
        self.assertEqual(inc_15(Interval(hour=17, minute=0)), Interval(hour=17, minute=15))
        self.assertEqual(inc_15(Interval(hour=17, minute=15)), Interval(hour=17, minute=30))
        self.assertEqual(inc_15(Interval(hour=17, minute=30)), Interval(hour=17, minute=45))
        self.assertEqual(inc_15(Interval(hour=17, minute=45)), Interval(hour=18, minute=0))
        self.assertEqual(inc_15(Interval(hour=18, minute=0)), Interval(hour=18, minute=15))

        # Test minute increments
        self.assertEqual(inc_15(Interval(hour=1, minute=15)), Interval(hour=1, minute=30))
        self.assertEqual(inc_15(Interval(hour=1, minute=10)), Interval(hour=1, minute=25))
        self.assertEqual(inc_15(Interval(hour=1, minute=45)), Interval(hour=2, minute=0))
        self.assertEqual(inc_15(Interval(hour=1, minute=47)), Interval(hour=2, minute=2))

        # Test when hour wraps around
        self.assertEqual(inc_15(Interval(hour=23, minute=30)), Interval(hour=23, minute=45))
        self.assertEqual(inc_15(Interval(hour=23, minute=45)), Interval(hour=0, minute=0))

        # Test strings
        self.assertEqual(inc_15(Interval(hour='17', minute='0')), Interval(hour=17, minute=15))
        self.assertEqual(inc_15(Interval(hour='17', minute='15')), Interval(hour=17, minute=30))
        self.assertEqual(inc_15(Interval(hour='17', minute='30')), Interval(hour=17, minute=45))
        self.assertEqual(inc_15(Interval(hour='17', minute='45')), Interval(hour=18, minute=0))
        self.assertEqual(inc_15(Interval(hour='18', minute='0')), Interval(hour=18, minute=15))

        # Test errors
        self.assertRaises(Exception, inc_15, Interval(hour=-1, minute=15))
        self.assertRaises(Exception, inc_15, Interval(hour=-1, minute=-1))


def inc_15(interval):
    interval.increment_15_mins()
    return interval


if __name__ == '__main__':
    unittest.main()
