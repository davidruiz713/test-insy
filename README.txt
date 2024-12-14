*** Notes

I have deployed this API in Koyeb, but also the files could be run locally.
The url to run in Koyeb is this one: http://silent-charin-eci-f3343bab.koyeb.app/predict/ 

This github repo is : https://github.com/davidruiz713/test-insy/ 

------


To run this API on local, it can be run with:  uvicorn main:app --reload
The runnable API is on the main.py file. 

The model has been already compiled to produce the file hit_song_predictor_model.pkl, 
this file will be used to predict the data. The model uses Spotify Most Streamed Songs.csv to train it. 

The model prediction can be called via an API, Attached is the postman collection to test the API directly.

The API could be deployed also locally and it should be accessible at : http://127.0.0.1:8000/

The intent of the API is to pass data to the prediction model and stablish
 if a song will be a hit or not in the spotify lists. 
