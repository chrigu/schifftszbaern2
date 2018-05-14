import unittest
from datetime import datetime, timedelta
from radar.hit import _last_hit_not_relevant, _has_no_last_hit, TIME_THRESHOLD


class HitTests(unittest.TestCase):

    def test_last_hit_relevant(self):
        now_minus_threshold = datetime.now() - timedelta(0, 0, 0, 0, TIME_THRESHOLD - 1)
        last_hit = {"createdAt": now_minus_threshold.isoformat()}
        not_relevant = _last_hit_not_relevant(last_hit)
        self.assertFalse(not_relevant)

    def test_last_hit__not_relevant(self):
        now_minus_threshold = datetime.now() - timedelta(0, 0, 0, 0, TIME_THRESHOLD + 1)
        last_hit = {"createdAt": now_minus_threshold.isoformat()}
        not_relevant = _last_hit_not_relevant(last_hit)
        self.assertTrue(not_relevant)

    def test_has_last_hit(self):
        last_hit = {"intensity": 12}
        has_no_last_hit = _has_no_last_hit([last_hit])
        self.assertFalse(has_no_last_hit)