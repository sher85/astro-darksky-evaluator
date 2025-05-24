import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load your CSV file (adjust path as needed)
df = pd.read_csv("Texas_Locations_with_Coordinates.csv", skiprows=2)
df = df.rename(columns={"Location": "Location Name"})

# Drop rows without a location
df = df[df["Location Name"].notna()]

# Initialize geocoder
geolocator = Nominatim(user_agent="astro_trip_planner")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Function to get lat/lon for each location
def get_coordinates(location_name):
    try:
        location = geocode(location_name + ", Texas")
        if location:
            return pd.Series([location.latitude, location.longitude])
    except Exception as e:
        print(f"Error with {location_name}: {e}")
    return pd.Series([None, None])

# Apply geocoding
df[["Latitude", "Longitude"]] = df["Location Name"].apply(get_coordinates)

# Save result
df.to_csv("Texas_Locations_with_Coordinates.csv", index=False)
print("✅ Done! File saved as 'Texas_Locations_with_Coordinates.csv'")