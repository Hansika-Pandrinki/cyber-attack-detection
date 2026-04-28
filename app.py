from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model safely
try:
    with open("model.pkl", "rb") as f:
        model, le = pickle.load(f)
except:
    model = None
    le = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return "App is working!"

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return "Model not loaded"

    duration = int(request.form["duration"])
    protocol = request.form["protocol"]
    src_bytes = int(request.form["src_bytes"])

    protocol_encoded = le.transform([protocol])[0]

    prediction = model.predict([[duration, protocol_encoded, src_bytes]])
    prob = model.predict_proba([[duration, protocol_encoded, src_bytes]])

    confidence = round(max(prob[0]) * 100, 2)

    if prediction[0] == 1:
        status = "Attack Detected"
        risk = "High"
        action = "Block suspicious activity"
    else:
        status = "Normal Traffic"
        risk = "Low"
        action = "No action required"

    result = f"{status} | Confidence: {confidence}% | Risk: {risk} | Action: {action}"

    return render_template("index.html", result=result)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))