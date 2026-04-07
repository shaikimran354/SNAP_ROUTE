# Snap Route

Snap Route is a FastAPI-based backend application that provides image classification for location identification and route calculation features. It acts as an API for clients to upload images to identify a location and find routes/distances between locations.

## Features

- **Location Classification**: Upload an image of a landmark/location, and the application uses a pre-trained ML model (TensorFlow + OpenCV) to predict the location name.
- **Route Tracking**: Calculate distances, estimated time, required steps, and calories burned between two locations using pre-loaded coordinate data and OSRM (Open Source Routing Machine).
- **FastAPI Framework**: Robust, high-performance API backend.


  
## Dataset :
https://drive.google.com/drive/folders/1mjxdYdAGYKVRA9fJZo8Pd1Tb12j-nHCM



## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shaikimran354/SNAP_ROUTE.git
   cd SNAP_ROUTE
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

- `GET /`: Serves the base UI.
- `GET /locations`: Returns a sorted list of all available locations for routing.
- `POST /classify`: Upload an image file. The server processes it and returns the predicted location name.
- `POST /route`: Provide a source and destination. Returns distance, duration, steps, and calories.

## Project Structure

- `main.py`: The entry point for the FastAPI application. Includes all API endpoints.
- `models.py`: Pydantic data models for API requests and responses.
- `requirements.txt`: Python package dependencies.
- `services/`: Contains core logic modules.
  - `classifier.py`: Connects to model components to run ML inference on images.
  - `osrm.py`: Fetches live distances between geographical coordinates.
  - `routes.py`: Loads offline routes and location datasets.
- `data/`: Datasets, pre-trained `.h5` ML models, and reference files.
- `training/`: Jupyter notebooks used for data preprocessing and model training.

## Output Result
<img width="1206" height="577" alt="image" src="https://github.com/user-attachments/assets/2b27cd4a-d368-41d8-9fe2-374ef9e8b573" />
<img width="1091" height="564" alt="image" src="https://github.com/user-attachments/assets/20331e61-d2e5-4d38-8739-2f4953837ee7" />
<img width="1081" height="491" alt="image" src="https://github.com/user-attachments/assets/86a45c73-0174-491b-bb80-b12fb4cb1767" />




## License

This project is created by [shaikimran354](https://github.com/shaikimran354).
