import pandas as pd

def load_routes():
    try:
        df = pd.read_excel("data/routes.xlsx", sheet_name="All Routes")
        df.columns = [c.strip() for c in df.columns]
        return df.rename(columns={
            "Start Location": "start_location",
            "End Location": "end_location",
            "Distance (m)": "distance_meters",
            "Duration (min)": "duration_minutes",
        })
    except FileNotFoundError:
        return pd.read_csv("data/routes.csv") if __import__('os').path.exists("data/routes.csv") else None

def load_locations():
    try:
        df = pd.read_excel("data/locations.xlsx", sheet_name="Campus Locations")
        df.columns = [c.strip() for c in df.columns]
        df = df.dropna(subset=["Location Name", "Latitude", "Longitude"])
        df["Location Name"] = df["Location Name"].str.strip()
        return df
    except FileNotFoundError:
        return None

def lookup_route(routes_df, source, destination):
    if routes_df is None:
        return None
    match = routes_df[
        (routes_df["start_location"] == source) &
        (routes_df["end_location"]   == destination)
    ]
    if match.empty:
        return None
    row = match.iloc[0]
    dist = row.get("distance_meters")
    if dist is None or not pd.notna(dist) or float(dist) <= 0:
        return None
    return {
        "distance_meters":  float(dist),
        "duration_minutes": float(row.get("duration_minutes", 0)),
    }

def get_coords(locations_df, name):
    if locations_df is None:
        return None, None
    row = locations_df[locations_df["Location Name"] == name]
    if row.empty:
        return None, None
    return float(row.iloc[0]["Latitude"]), float(row.iloc[0]["Longitude"])