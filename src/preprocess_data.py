import pandas as pd
from datetime import datetime
import os 
from src.feature_engineering import is_holiday

# Define the path to the data
data_dir = 'data'


class GokadaDataPreprocessor:
    def __init__(self, completed_orders_path, drivers_location_path):
        self.completed_orders = pd.read_csv(completed_orders_path)
        self.drivers_location = pd.read_csv(drivers_location_path)

    def preprocess_data(self):
        """Performs all cleaning and preprocessing steps."""

        # Preprocess the DataFrames
        self.preprocess_completed_orders_only()
        self.preprocess_drivers_location()

        # Merge DataFrames
        self.merged_df = pd.merge(self.completed_orders, self.drivers_location, on='order_id', how='inner')
        
        # Drop rows where 'driver_action' is null
        self.merged_df.dropna(subset=['driver_action'], inplace=True)

        # Convert column names to lowercase and replace spaces with underscores
        self.merged_df.columns = self.merged_df.columns.str.lower().str.replace(' ', '_')

        return self.merged_df

    def preprocess_drivers_location(self):
        """Preprocesses the drivers_location DataFrame."""
        # Convert 'order_id' to string
        self.drivers_location['order_id'] = self.drivers_location['order_id'].astype(str)
        
        # Drop unnecessary columns
        self.drivers_location.drop(columns=['created_at', 'updated_at'], inplace=True)
        
        # Rename 'lat' and 'lon' to 'drivers_lat' and 'drivers_lon'
        self.drivers_location = self.drivers_location.rename(columns={'lat': 'drivers_lat', 'lng': 'drivers_lng'})
        
        return self.drivers_location

    def preprocess_completed_orders_only(self):
        """Preprocesses only the completed_orders DataFrame."""
        # Rename 'Trip ID' to 'order_id'
        self.completed_orders = self.completed_orders.rename(columns={'Trip ID': 'order_id'})
        
        # Convert 'order_id' to string
        self.completed_orders['order_id'] = self.completed_orders['order_id'].astype(str)
        
        # Handle missing values in 'Trip Start Time' and 'Trip End Time'
        self.completed_orders = self._handle_missing_times(self.completed_orders)
        
        # Convert timestamps and extract time features
        self._convert_timestamps_and_extract_features()

        # Reverse coordinates in 'Trip Origin' and 'Trip Destination'
        self.completed_orders = self._reverse_coordinates(self.completed_orders, ['Trip Origin', 'Trip Destination'])
  
        self._extract_coordinates(self.completed_orders)

        # Add 'is_holiday' feature
        self._add_is_holiday_feature()
        
        return self.completed_orders

    def _handle_missing_times(self, df, col_name_impute='Trip Start Time'):
        """Imputes missing values in 'Trip Start Time'."""
        df[col_name_impute] = pd.to_datetime(df[col_name_impute])
        median_start_time = df[col_name_impute].median()
        df[col_name_impute].fillna(median_start_time, inplace=True)

        df['Trip End Time'] = pd.to_datetime(df['Trip End Time'])
        median_end_time = df['Trip End Time'].median()
        df['Trip End Time'].fillna(median_end_time, inplace=True)

        return df

    def _convert_timestamps_and_extract_features(self):
        """Converts timestamps to datetime and extracts time features."""
        self.completed_orders['Trip Start Time'] = pd.to_datetime(self.completed_orders['Trip Start Time'])
        self.completed_orders['Trip End Time'] = pd.to_datetime(self.completed_orders['Trip End Time'])
        self.completed_orders['day_of_week'] = self.completed_orders['Trip Start Time'].dt.day_name()
        self.completed_orders['hour_of_day'] = self.completed_orders['Trip Start Time'].dt.hour
        self.completed_orders['day_of_month'] = self.completed_orders['Trip Start Time'].dt.day
        self.completed_orders['month'] = self.completed_orders['Trip Start Time'].dt.month_name()
        self.completed_orders['trip_start_date'] = pd.to_datetime(self.completed_orders['Trip Start Time']).dt.date
        self.completed_orders['trip_end_date'] = pd.to_datetime(self.completed_orders['Trip End Time']).dt.date
        self.completed_orders['trip_duration'] = (pd.to_datetime(self.completed_orders['Trip End Time']) - pd.to_datetime(self.completed_orders['Trip Start Time'])).dt.total_seconds()
      

    def _reverse_coordinates(self, df, columns):
        """
        Reverses the order of coordinates in the specified columns of a DataFrame.

        Parameters:
        - df: pandas.DataFrame containing the data.
        - columns: List of column names to reverse the coordinates in.

        Returns:
        - The DataFrame with the coordinates in the specified columns reversed.
        """
        for column in columns:
            # Splitting each coordinate into two parts, assuming they are separated by a comma
            coords = df[column].str.split(',', expand=True)
            
            # Reversing the order and combining them back into a single string
            df[column] = coords[1] + ',' + coords[0]
        
        return df

    def _calculate_trip_duration_in_seconds(start_time_str, end_time_str, time_format='%Y-%m-%d %H:%M:%S'):
        start_time = datetime.strptime(start_time_str, time_format)
        end_time = datetime.strptime(end_time_str, time_format)
        duration = end_time - start_time
        return duration.total_seconds()

    def _add_is_holiday_feature(self, col_name="Trip Start Time"):
        """Adds a feature indicating whether the trip start date is a holiday."""
        self.completed_orders['is_holiday'] = self.completed_orders[col_name].apply(is_holiday)

    def _extract_coordinates(self, given_df):
        """Extracts latitude and longitude from string columns."""
        for col in ['Trip Origin', 'Trip Destination']:
            for df in [given_df]:
                df[[f'{col}_latitude', f'{col}_longitude']] = df[col].str.split(',', expand=True).astype(float)

    def save_to_csv(self, df, filename):
        """Saves DataFrame to a CSV file."""
        df.to_csv(os.path.join(data_dir, filename), index=False)

    def preprocess_and_save(self, filename):
        """Preprocesses data and saves to CSV."""
        preprocessed_df = self.preprocess_data()
        self.save_to_csv(preprocessed_df, filename)
        return preprocessed_df

# Example usage
# preprocessor = GokadaDataPreprocessor('completed_orders.csv', 'drivers_location_during_request.csv')
# preprocessed_df = preprocessor.preprocess_data()
# print(preprocessed_df.head().to_markdown(index=False, numalign="left", stralign="left"))
