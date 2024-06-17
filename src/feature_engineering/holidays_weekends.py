# FILE: holidays_weekends.py
import pandas as pd
import holidays

def is_holiday(datetime_obj, country_code='NG'):
  """Checks if the trip start time is on a holiday."""
  if pd.isnull(datetime_obj):
    return 0
  country_holidays = holidays.country_holidays(country_code)
  return 1 if datetime_obj.date() in country_holidays else 0