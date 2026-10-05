from pathlib import Path
import sys
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from build_analysis import build_dataset


class TestOutputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = build_dataset()

    def test_source_has_all_mexican_states_and_no_duplicates(self):
        self.assertEqual(len(self.df), 32)
        self.assertEqual(self.df["state_code"].nunique(), 32)
        self.assertEqual(self.df["state"].nunique(), 32)

    def test_totals_and_rates_are_valid(self):
        self.assertTrue((self.df["housing_backlog_units"] > 0).all())
        self.assertTrue((self.df["total_housing_units"] == self.df["housing_backlog_units"] + self.df["housing_without_backlog_units"]).all())
        self.assertTrue(self.df["backlog_rate_pct"].between(0, 100).all())

    def test_score_and_ranking_are_complete(self):
        self.assertTrue(self.df["opportunity_score"].between(0, 100).all())
        self.assertEqual(set(self.df["rank"]), set(range(1, 33)))
        self.assertGreaterEqual(self.df.iloc[0]["opportunity_score"], self.df.iloc[-1]["opportunity_score"])

    def test_official_national_backlog_rate(self):
        rate = 100 * self.df["housing_backlog_units"].sum() / self.df["total_housing_units"].sum()
        self.assertEqual(round(rate, 1), 21.9)


if __name__ == "__main__":
    unittest.main()
