import unittest
import pandas as pd
from src.utils import detect_outliers

class TestUtils(unittest.TestCase):
  def setUp(self):
    self.dummy_data = pd.DataFrame({
      'value': [1, 2, 3, 100, 5]
    })

  def test_detect_outliers(self):
    outliers_iqr, outliers_z = detect_outliers(self.dummy_data, 'value')
    # Check if the returned values are integers, indicating counts of outliers
    self.assertIsInstance(outliers_iqr, int)
    self.assertIsInstance(outliers_z, int)

if __name__ == '__main__':
  unittest.main()