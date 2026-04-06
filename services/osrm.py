import requests

OSRM_BASE = "http://router.project-osrm.org/route/v1/foot/{lng1},{lat1};{lng2},{lat2}"

def fetch_live_distance(lat1, lng1, lat2, lng2):
    url = OSRM_BASE.format(lat1=lat1, lng1=lng1, lat2=lat2, lng2=lng2)
    try:
        r = requests.get(url, params={"overview": "false", "steps": "false"}, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data.get("code") != "Ok":
            return None
        route = data["routes"][0]
        return {
            "distance_meters":  round(route["distance"], 1),
            "duration_minutes": round(route["duration"] / 60, 1),
        }
    except Exception:
        return None