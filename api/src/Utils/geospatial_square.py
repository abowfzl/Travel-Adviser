import math


def calculate_square(lat, lon, distance_km=20):
    # Convert distance to degrees
    lat_delta = distance_km / 111.32
    lon_delta = distance_km / (111.32 * math.cos(math.radians(lat)))

    # Calculate the corners of the square
    top_left = (lat + lat_delta, lon - lon_delta)
    bottom_right = (lat - lat_delta, lon + lon_delta)

    return {
        "min_lat": bottom_right[0],
        "max_lat": top_left[0],
        "min_lon": top_left[1],
        "max_lon": bottom_right[1]
    }
