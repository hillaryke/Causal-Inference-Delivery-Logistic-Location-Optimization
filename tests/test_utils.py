# FILE: tests/test_utils.py

import unittest
import pandas as pd
from src.utils import display_df, detect_outliers

class TestUtils(unittest.TestCase):
  def setUp(self):
    self.dummy_data = pd.DataFrame({
      'value': [1, 2, 3, 100, 5]
    })

  def test_detect_outliers(self):
    outliers_iqr, outliers_z = detect_outliers(self.dummy_data, 'value')
    self.assertEqual(outliers_iqr, 1)
    self.assertEqual(outliers_z, 1)

if __name__ == '__main__':
  unittest.main()