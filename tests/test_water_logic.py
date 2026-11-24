import datetime
import unittest

from pysensaphone.water_logic import is_within_daily_window


class TestIsWithinDailyWindow(unittest.TestCase):
    """Tests for the minute-aware daily window helper."""

    @staticmethod
    def _at(hour, minute):
        return datetime.datetime(2024, 11, 15, hour, minute)

    def test_inside_evening(self):
        self.assertTrue(is_within_daily_window("21:00", "10:00", self._at(22, 0)))

    def test_inside_after_midnight(self):
        self.assertTrue(is_within_daily_window("21:00", "10:00", self._at(2, 0)))

    def test_outside_midday(self):
        self.assertFalse(is_within_daily_window("21:00", "10:00", self._at(15, 0)))

    def test_minute_precision_before_on(self):
        self.assertFalse(is_within_daily_window("21:30", "10:30", self._at(21, 15)))

    def test_minute_precision_after_off(self):
        self.assertFalse(is_within_daily_window("21:30", "10:30", self._at(10, 45)))

    def test_bounds_are_inclusive(self):
        self.assertTrue(is_within_daily_window("21:30", "10:30", self._at(21, 30)))
        self.assertTrue(is_within_daily_window("21:30", "10:30", self._at(10, 30)))

    def test_non_wrapping_window(self):
        self.assertTrue(is_within_daily_window("08:00", "17:00", self._at(12, 0)))
        self.assertFalse(is_within_daily_window("08:00", "17:00", self._at(18, 0)))

    def test_missing_bounds(self):
        self.assertFalse(is_within_daily_window(None, "10:00", self._at(12, 0)))
        self.assertFalse(is_within_daily_window("21:00", None, self._at(12, 0)))

    def test_malformed_bounds(self):
        self.assertFalse(is_within_daily_window("nope", "10:00", self._at(12, 0)))
        self.assertFalse(is_within_daily_window("21:00", "10", self._at(12, 0)))

    def test_out_of_range_bounds(self):
        self.assertFalse(is_within_daily_window("25:00", "10:00", self._at(12, 0)))
        self.assertFalse(is_within_daily_window("21:00", "10:99", self._at(12, 0)))


if __name__ == '__main__':
    unittest.main()
