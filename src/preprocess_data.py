import pandas as pd
import os 

# Define the path to the data
data_dir = 'data'


class GokadaDataPreprocessor:
    def __init__(self, completed_orders_path, drivers_location_path):
        self.completed_orders = pd.read_csv(completed_orders_path)
        self.drivers_location = pd.read_csv(drivers_location_path)

    def preprocess_data(self):
        """Performs all cleaning and preprocessing steps."""

        # Rename 'Trip ID' to 'order_id' in completed_orders
        self.completed_orders = self.completed_orders.rename(columns={'Trip ID': 'order_id'})
        
        # Convert 'order_id' to string in both DataFrames
        self.completed_orders['order_id'] = self.completed_orders['order_id'].astype(str)
        self.drivers_location['order_id'] = self.drivers_location['order_id'].astype(str)
        
        # Drop unnecessary columns
        self.drivers_location.drop(columns=['created_at', 'updated_at'], inplace=True)

        # Merge DataFrames
        self.merged_df = self.completed_orders.merge(self.drivers_location, on='order_id', how='left')

        # Drop rows where 'driver_action' is null
        self.merged_df.dropna(subset=['driver_action'], inplace=True)

        # Filter for accepted orders
        # self.merged_df_accepted = self.merged_df[self.merged_df['driver_action'] == 'accepted'].copy()

        # Handle missing values
        self._handle_missing_times()
        
        # Convert to datetime and extract time features
        self._convert_timestamps_and_extract_features()

        # Extract latitude and longitude
        self._extract_coordinates()

        return self.merged_df

    def _handle_missing_times(self):
      """Imputes missing values in 'Trip Start Time'."""
      self.merged_df['Trip Start Time'] = pd.to_datetime(self.merged_df['Trip Start Time'])
      median_start_time = self.merged_df['Trip Start Time'].median()
      self.merged_df['Trip Start Time'].fillna(median_start_time, inplace=True)

    def _convert_timestamps_and_extract_features(self):
        """Converts time columns to datetime and extracts features."""
        for df in [self.merged_df]:
            df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'])
            df['Trip End Time'] = pd.to_datetime(df['Trip End Time'])
            df['day_of_week'] = df['Trip Start Time'].dt.day_name()
            df['hour_of_day'] = df['Trip Start Time'].dt.hour
            df['day_of_month'] = df['Trip Start Time'].dt.day
            df['month'] = df['Trip Start Time'].dt.month_name()

    def _extract_coordinates(self):
        """Extracts latitude and longitude from string columns."""
        for col in ['Trip Origin', 'Trip Destination']:
            for df in [self.merged_df]:
                df[[f'{col}_latitude', f'{col}_longitude']] = df[col].str.split(',', expand=True).astype(float)


# Example usage
# preprocessor = GokadaDataPreprocessor('completed_orders.csv', 'drivers_location_during_request.csv')
# preprocessed_df = preprocessor.preprocess_data()
# print(preprocessed_df.head().to_markdown(index=False, numalign="left", stralign="left"))
