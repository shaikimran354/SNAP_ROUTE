import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"]  = "2"

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import numpy as np
import cv2

from models import RouteRequest, RouteResult, ClassifyResult
from services.classifier import classify_image
from services.osrm import fetch_live_distance
from services.routes import load_routes, load_locations, lookup_route, get_coords

app = FastAPI(title="Snap Route API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

routes_df    = None
locations_df = None

# ✅ Load data AFTER server starts — not during import
@app.on_event("startup")
async def startup():
    global routes_df, locations_df
    routes_df    = load_routes()
    locations_df = load_locations()
    print("Routes and locations loaded")

def calc_steps(d): return round(d / 0.762)
def calc_calories(d): return round(d * 0.06)

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

@app.get("/locations")
def get_locations():
    if locations_df is not None:
        return {"locations": sorted(locations_df["Location Name"].tolist())}
    if routes_df is not None:
        return {"locations": sorted(routes_df["start_location"].dropna().unique().tolist())}
    return {"locations": []}

@app.post("/classify", response_model=ClassifyResult)
async def classify_location(file: UploadFile = File(...)):
    contents  = await file.read()
    img_array = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    if img_array is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    img_rgb   = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    predicted = classify_image(img_rgb)
    return {"predicted_location": predicted}

@app.post("/route", response_model=RouteResult)
def get_route(req: RouteRequest):
    if req.source == req.destination:
        raise HTTPException(status_code=400, detail="Already at destination")

    result = lookup_route(routes_df, req.source, req.destination)

    if result is None:
        lat1, lng1 = get_coords(locations_df, req.source)
        lat2, lng2 = get_coords(locations_df, req.destination)
        if not (lat1 and lat2):
            raise HTTPException(status_code=404, detail="Route not found")
        result = fetch_live_distance(lat1, lng1, lat2, lng2)
        if result is None:
            raise HTTPException(status_code=503, detail="Live routing unavailable")

    d = result["distance_meters"]
    return RouteResult(
        source           = req.source,
        destination      = req.destination,
        distance_meters  = d,
        duration_minutes = result["duration_minutes"],
        steps            = calc_steps(d),
        calories         = calc_calories(d),
    )