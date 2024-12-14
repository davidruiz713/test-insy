## For this API I'm using fast API, I installed : pip install fastapi uvicorn

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, model_validator, Field
from fastapi.responses import JSONResponse

import pickle
import numpy as np

app = FastAPI()


# Convert numpy int64 or float64 to native Python types (int, float)
def convert_numpy_types(obj):
    if isinstance(obj, np.generic):
        return obj.item()  # Convert numpy scalar (int64 or float64) to native type
    elif isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert numpy array to a list
    return obj

# Load the saved model from the .pkl file
with open('hit_song_predictor_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the input data schema using Pydantic
class SongData(BaseModel):
    artist_count: int
    released_year: int
    released_month: int
    released_day: int
    in_spotify_playlists: int
    in_spotify_charts: int
    streams: int
    in_apple_playlists: int
    in_apple_charts: int
    in_deezer_playlists: int
    in_deezer_charts: int
    in_shazam_charts: int
    bpm: float
    danceability: float
    valence: float
    energy: float
    acousticness: float
    instrumentalness: float
    liveness: float
    speechiness: float
    key_0: int
    key_A: int
    key_AA: int
    key_B: int
    key_C: int
    key_D: int
    key_DD: int
    key_E: int
    key_F: int
    key_FF: int
    key_G: int
    key_GG: int
    mode_Major: int
    mode_Minor: int

    @model_validator(mode='before')
    def check_valid_data(cls, values):
        # Validate year is within reasonable bounds
        if not (1900 <= values.get('released_year', 0) <= 2024):
            raise ValueError("released_year must be between 1900 and 2024")
        
        # Validate streams must be positive
        if values.get('streams', 0) < 0:
            raise ValueError("streams must be a positive integer")
        
        # Validate BPM (beats per minute) within a reasonable range
        if not (40 <= values.get('bpm', 0) <= 200):
            raise ValueError("bpm must be between 40 and 200")
        
        # Validate percentages to be between 0 and 100
        for field in ['danceability_pct', 'valence_pct', 'energy_pct', 'acousticness_pct', 'instrumentalness_pct', 'liveness_pct', 'speechiness_pct']:
            if not (0 <= values.get(field, 0) <= 100):
                raise ValueError(f"{field} must be between 0 and 100")
        
        return values

# Create an endpoint to predict the popularity
@app.post("/predict")
async def predict(song_data: SongData):
    # Prepare the input data as a numpy array
    input_data = np.array([[song_data.artist_count,
                            song_data.released_year,
                            song_data.released_month,
                            song_data.released_day,
                            song_data.in_spotify_playlists,
                            song_data.in_spotify_charts,
                            song_data.streams,
                            song_data.in_apple_playlists,
                            song_data.in_apple_charts,
                            song_data.in_deezer_playlists,
                            song_data.in_deezer_charts,
                            song_data.in_shazam_charts,
                            song_data.bpm,
                            song_data.danceability, 
                            song_data.valence, 
                            song_data.energy, 
                            song_data.acousticness, 
                            song_data.instrumentalness, 
                            song_data.liveness, 
                            song_data.speechiness, 
                            song_data.key_0, 
                            song_data.key_A, 
                            song_data.key_AA, 
                            song_data.key_B, 
                            song_data.key_C, 
                            song_data.key_D, 
                            song_data.key_DD, 
                            song_data.key_E, 
                            song_data.key_F, 
                            song_data.key_FF, 
                            song_data.key_G, 
                            song_data.key_GG, 
                            song_data.mode_Major, 
                            song_data.mode_Minor]], dtype=object)

    # Convert numpy types (int64, float64) to native Python types
    input_data = np.vectorize(convert_numpy_types)(input_data)

    try:
        # Get prediction from model
        prediction = model.predict(input_data)
    except Exception as e:
        # If an error occurs during prediction, return a helpful message
        raise HTTPException(
            status_code=500,
            detail=f"Error during model prediction: {str(e)}"
        )
    
    # Convert the prediction to a native Python type before returning it
    prediction = prediction.tolist() 

    # Return the prediction result
    #return {"prediction": prediction[0]}

    # Return different messages based on prediction result
    if prediction[0] == 1:
        return {"prediction": 1, "message": "This song is predicted to be a hit!"}
    else:
        return {"prediction": 0, "message": "This song is not predicted to be a hit."}


# Data model for the POST request
class ColorRequest(BaseModel):
    color: str

# Global variable to store the color
selected_color = "no color selected"

@app.get("/")
def read_root():
    return {"message": f"Hello, World!", "color": selected_color}

@app.post("/set-color")
def set_color(color_request: ColorRequest):
    global selected_color
    selected_color = color_request.color
    return {"message": "Color updated successfully", "new_color": selected_color}

# Custom handler for undefined routes
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "This URL is not defined. Try a good one", "path": str(request.url)},
    )
