#!/usr/bin/env python3
import unittest


def timeToMS(time):
    """input: hours, minutes, seconds, milliseconds"""
    if len(time) == 4: return ((time[0] * 60 + time[1]) * 60 + time[2]) * 1000 + time[3]
    return


class TimeToMSTest(unittest.TestCase):
    def test_returns(self):
        from random import randint, uniform
        self.assertRegex(str(timeToMS((randint(0, 24), randint(0, 60), randint(0, 60), randint(0, 1000)))), "\d+")
        self.assertRegex(str(timeToMS((uniform(0, 24), uniform(0, 60), uniform(0, 60), uniform(0, 1000)))),
                         "\d+(\.\d+)?")
        self.assertEqual(timeToMS((0, 0, 0)), None)

    def test_ms(self):
        self.assertEqual(timeToMS((0, 0, 0, 0)), 0)
        self.assertEqual(timeToMS((0, 0, 0, 1)), 1)

    def test_sec(self):
        self.assertEqual(timeToMS((0, 0, 1, 0)), 1000)
        self.assertEqual(timeToMS((0, 0, 1, 1)), 1001)

    def test_min(self):
        self.assertEqual(timeToMS((0, 1, 0, 0)), 60000)
        self.assertEqual(timeToMS((0, 1, 0, 1)), 60001)
        self.assertEqual(timeToMS((0, 1, 1, 0)), 61000)
        self.assertEqual(timeToMS((0, 1, 1, 1)), 61001)

    def test_hour(self):
        self.assertEqual(timeToMS((1, 0, 0, 0)), 3600000)
        self.assertEqual(timeToMS((1, 0, 0, 1)), 3600001)
        self.assertEqual(timeToMS((1, 0, 1, 0)), 3601000)
        self.assertEqual(timeToMS((1, 0, 1, 1)), 3601001)
        self.assertEqual(timeToMS((1, 1, 0, 0)), 3660000)
        self.assertEqual(timeToMS((1, 1, 0, 1)), 3660001)
        self.assertEqual(timeToMS((1, 1, 1, 0)), 3661000)
        self.assertEqual(timeToMS((1, 1, 1, 1)), 3661001)


if __name__ == '__main__': unittest.main()
