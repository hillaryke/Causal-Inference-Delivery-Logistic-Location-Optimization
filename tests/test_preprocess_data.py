# FILE: tests/test_preprocess_data.py

import unittest
from src.preprocess_data import GokadaDataPreprocessor
import pandas as pd
from datetime import datetime

class TestGokadaDataPreprocessor(unittest.TestCase):
    def setUp(self):
        # Create dummy data for testing
        self.dummy_completed_orders = pd.DataFrame({
            'Trip ID': ['1', '2'],
            'Trip Start Time': ['2021-01-01 10:00:00', '2021-01-02 11:00:00'],
            'Trip End Time': ['2021-01-01 11:00:00', '2021-01-02 12:00:00'],
            'Trip Origin': ['34.0522,-118.2437', '40.7128,-74.0060'],
            'Trip Destination': ['36.7783,-119.4179', '34.0522,-118.2437']
        })
        self.dummy_drivers_location = pd.DataFrame({
            'order_id': ['1', '2'],
            'lat': ['34.0522', '40.7128'],
            'lng': ['-118.2437', '-74.0060'],
            'created_at': ['2021-01-01 09:00:00', '2021-01-02 10:00:00'],
            'updated_at': ['2021-01-01 10:00:00', '2021-01-02 11:00:00']
        })
        self.processor = GokadaDataPreprocessor(None, None)
        self.processor.completed_orders = self.dummy_completed_orders
        self.processor.drivers_location = self.dummy_drivers_location

    def test_preprocess_drivers_location(self):
        processed = self.processor.preprocess_drivers_location()
        self.assertTrue('driver_location' in processed.columns)
        self.assertEqual(processed['driver_location'].iloc[0], '-118.2437,34.0522')

    def test_preprocess_completed_orders_only(self):
        processed = self.processor.preprocess_completed_orders_only()
        self.assertTrue('order_id' in processed.columns)
        self.assertEqual(processed['order_id'].dtype, object)  # Check if 'order_id' is string

    def test_reverse_coordinates(self):
        processed = self.processor._reverse_coordinates(self.dummy_completed_orders, ['Trip Origin', 'Trip Destination'])
        self.assertEqual(processed['Trip Origin'].iloc[0], '-118.2437,34.0522')

if __name__ == '__main__':
    unittest.main()