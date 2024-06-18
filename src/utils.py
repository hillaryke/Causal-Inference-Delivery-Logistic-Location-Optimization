
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Display df in markdown
def display_df(df, n_rows=5, head_or_tail="head"):
    """Displays DataFrame in markdown format."""
    
    if head_or_tail == "head":
        print(df.head(n_rows).to_markdown(index=False, numalign="left", stralign="left"))
    elif head_or_tail == "tail":
        print(df.tail(n_rows).to_markdown(index=False, numalign="left", stralign="left"))


def detect_outliers(dataframe, column, units=''):
  """
  Detects outliers in a specified column of a DataFrame using both visual (box plot) and statistical methods (Z-score and IQR).
  Enhances labeling with a units parameter for the box plot.

  Parameters:
  - dataframe (pd.DataFrame): The DataFrame containing the data.
  - column (str): The name of the column to check for outliers.
  - units (str): Units of measurement for the column, to enhance graph labeling.

  Returns:
  - A tuple containing the number of outliers detected by the IQR method and the Z-score method.
  """
  # Visual Inspection - Box Plot
  plt.figure(figsize=(10, 6))  # Optional: Adjust figure size for better visibility
  sns.boxplot(x=dataframe[column])
  plt.title(f'Box plot of {column} ({units})')  # Include units in the title
  plt.xlabel(f'{column} ({units})')  # Include units in the x-axis label
  plt.show()

  # Statistical Methods
  # Z-score
  z_scores = np.abs(stats.zscore(dataframe[column]))
  outliers_z = np.where(z_scores > 3)

  # IQR
  Q1 = dataframe[column].quantile(0.25)
  Q3 = dataframe[column].quantile(0.75)
  IQR = Q3 - Q1
  outliers_iqr = dataframe[(dataframe[column] < (Q1 - 1.5 * IQR)) | (dataframe[column] > (Q3 + 1.5 * IQR))]

  # Print outlier counts
  print(f"Outliers in {column} ({units}) using IQR method: {len(outliers_iqr)}")
  print(f"Outliers in {column} ({units}) using Z-score: {len(outliers_z[0])}")

  return len(outliers_iqr), len(outliers_z[0])

# Example usage:
# Assuming 'df' is your DataFrame and 'trip_distance' is the column you want to check for outliers
# detect_outliers(df, 'trip_distance', 'km')