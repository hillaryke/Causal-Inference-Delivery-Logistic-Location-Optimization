import requests
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def calculate_distance_with_ors_concurrent(start_end_pairs, profile='cycling-electric'):
    """
    Calculates distances for multiple pairs of start and end coordinates concurrently.

    Parameters:
    - start_end_pairs (list of tuples): Each tuple contains start and end coordinates in 'longitude,latitude' format.
    - profile (str): The routing profile to use. Default is 'cycling-electric'.

    Returns:
    - List of distances in meters between the coordinates pairs.
    """
    url = 'http://localhost:8080/ors/v2/directions/{}?'.format(profile)
    distances = [np.nan] * len(start_end_pairs)  # Initialize distances with np.nan

    def fetch_distance(start_coords, end_coords):
        params = {'start': start_coords, 'end': end_coords}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            directions = response.json()
            return directions['features'][0]['properties']['segments'][0]['distance']
        except Exception:
            return np.nan

    with ThreadPoolExecutor() as executor:
        future_to_index = {executor.submit(fetch_distance, pair[0], pair[1]): index for index, pair in enumerate(start_end_pairs)}
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                distances[index] = future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')
                distances[index] = np.nan

    return distances

### Example usage with DataFrame
# start_end_pairs = [(row['trip_origin'], row['trip_destination']) for index, row in df.iterrows()]
# distances = calculate_distance_with_ors_concurrent(start_end_pairs)
# df['trip_distance'] = distances

def calculate_estimated_time_with_ors(start_coords, end_coords, profile='cycling-electric'):
    """
    Calculates the estimated travel time between two coordinates using OpenRouteService.

    Parameters:
    - start_coords (str): The starting coordinates in 'longitude,latitude' format.
    - end_coords (str): The ending coordinates in 'longitude,latitude' format.
    - profile (str): The routing profile to use. Default is 'cycling-electric'.

    Returns:
    - Estimated travel time in seconds.
    - np.nan if there is an error.
    """
    url = f'http://localhost:8080/ors/v2/directions/{profile}?'
    params = {
        'start': start_coords,
        'end': end_coords
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        directions = response.json()
        estimated_time = directions['features'][0]['properties']['segments'][0]['duration']
        return estimated_time
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return np.nan  # Return np.nan on error
    except Exception as err:
        print(f"An error occurred: {err}")
        return np.nan  # Return np.nan on error

def calculate_distance_with_ors(start_coords, end_coords, profile='cycling-electric'):
    """
    Calculates the distance between two coordinates using OpenRouteService.

    Parameters:
    - start_coords (str): The starting coordinates in 'longitude,latitude' format.
    - end_coords (str): The ending coordinates in 'longitude,latitude' format.
    - profile (str): The routing profile to use. Default is 'cycling-road'.

    Returns:
    - distance (float): The distance in meters between the two coordinates.
    - None if there is an error.
    """
    url = f'http://localhost:8080/ors/v2/directions/{profile}?'
    params = {
        'start': start_coords,
        'end': end_coords
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        directions = response.json()
        distance = directions['features'][0]['properties']['segments'][0]['distance']
        return distance
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return np.nan  # Return np.nan on error
    except Exception as err:
        print(f"An error occurred: {err}")
        return np.nan  # Return np.nan on error

### Example usage
# start_coords = '3.2766339,6.60104170'  # Latitude, Longitude
# end_coords = '3.3916154,6.45010690'

# distance = calculate_distance_with_ors(start_coords, end_coords)
# print(distance)