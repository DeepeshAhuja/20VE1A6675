from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS
import requests

# Flask setup
app = Flask(__name__)
CORS(app)


# Global Variables
BASE_URL = "http://20.244.56.144"

# It can also be setup in Environment Variables
API_CREDENTIALS = {
    "companyName": "Train Central",
    "clientID": "f92d6d77-125c-4bb8-a24d-7e26ccae26d0",
    "clientSecret": "fIflBKdlEaWyDnju",
    "ownerName": "Rahul",
    "ownerEmail": "rahul@abc.edu",
    "rollNo": "20ve1a6675"
}

# Auth Token Data
AUTH_TOKEN_DATA = {}

# REST API's
@app.route("/")
def home():
    return jsonify({"hi":"everyone"})


@app.route("/getAuthToken")
def getAuthToken():
    global AUTH_TOKEN_DATA
    response = requests.post(f'{BASE_URL}/train/auth', json=API_CREDENTIALS)
    AUTH_TOKEN_DATA = response.json()
    return AUTH_TOKEN_DATA

@app.route("/getAllTrains")
def getAllTrains():
    try:
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN_DATA["access_token"]}'
        }
        response = requests.get(f'{BASE_URL}/train/trains', headers=headers)
        return response.json()
    except Exception as e:
        # Enters this block if auth token expires
        getAuthToken()
        return redirect(url_for('getAllTrains'))
        # print("error", e)
    
@app.route("/getTrainByNumber/<int:num>")
def getTrainByNumber(num):
    try:
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN_DATA["access_token"]}'
        }
        response = requests.get(f'{BASE_URL}/train/trains/{num}', headers=headers)
        return response.json()
    except:
        # Enters this block if auth token expires
        getAuthToken()
        return redirect(url_for('getTrainByNumber',num=num))

if __name__=="__main__":
    app.run(debug=True,port=8000)