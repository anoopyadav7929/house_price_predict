from flask import Flask , render_template , request
import pandas as pd
import pickle
import numpy as np
import webbrowser
from threading import Timer

app = Flask(__name__)
data = pd.read_csv("Cleaned_Data.csv")
pipe = pickle.load(open("RidgeModel.pkl" , "rb"))

# created dropdown menu for returning list of unique locations extracted from the dataset.
@app.route("/")
def index():
    locations = sorted(data["location"].unique( ))
    return render_template("index.html",locations=locations) 

# POST requests. Extracts user input from the form submitted by the user creates a DataFrame from input
@app.route("/predict" , methods=["POST"])
def predict():
    location = request.form.get("location")
    bhk = request.form.get("bhk")
    bath = request.form.get("bath")
    sqft = request.form.get("total_sqft")

    print(location , bhk, bath, sqft) 
    input=pd.DataFrame([[location , sqft , bath , bhk]] , columns=["location" , "total_sqft" , "bath" , "bhk"])
    prediction = pipe.predict(input)[0] * 100000

    if prediction < 0:
        return "---Invalid data"
    else:
        return str(np.round(prediction , 2))

# Starts the Flask web app on port 5001 and opens a web browser to view the application after a delay of 1 second
if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5001")).start()
    app.run(port=5001)

# debug mode , if app dosen't run
if __name__=="__main__":
    app.run(debug=True , port=5001)