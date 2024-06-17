import pandas as pd
import holidays

def is_holiday(datetime_obj, country_code='NG'):
  """Checks if the trip start time is on a holiday."""
  if pd.isnull(datetime_obj):
    return 0
  # Ensure datetime_obj is a datetime object
  datetime_obj = pd.to_datetime(datetime_obj)
  country_holidays = holidays.country_holidays(country_code)
  return 1 if datetime_obj.date() in country_holidays else 0

def is_weekend(df, feature_col="is_weekend", date_col='trip_start_time'):
  """Checks if the trip start time is on a weekend."""
  # Ensure datetime_obj is a datetime object
  datetime_obj = pd.to_datetime(datetime_obj)
  # return datetime_obj.dayofweek in [5, 6]

  df[feature_col] = pd.to_datetime(df[date_col]).dt.dayofweek.isin([5, 6]).astype(int)

  return df