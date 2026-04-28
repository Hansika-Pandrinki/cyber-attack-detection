from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model
with open('model.pkl', 'rb') as f:
    model, le = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    duration = int(request.form['duration'])
    protocol = request.form['protocol']
    src_bytes = int(request.form['src_bytes'])

    # Encode protocol
    protocol_encoded = le.transform([protocol])[0]

    # Prediction
    prediction = model.predict([[duration, protocol_encoded, src_bytes]])
    prob = model.predict_proba([[duration, protocol_encoded, src_bytes]])

    confidence = round(max(prob[0]) * 100, 2)

    # Logic
    if prediction[0] == 1:
        status = "Attack Detected"
        display_status = "Attack Detected"
        risk = "High"
        action = "Block suspicious activity"
    else:
        status = "Normal Traffic"
        display_status = "Normal Traffic"
        risk = "Low"
        action = "No action required"

    result = f"{display_status} | Confidence: {confidence}% | Risk: {risk} | Action: {action}"

    # Save logs (NO emojis)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{duration}, {protocol}, {src_bytes} -> {status}\n")

    return render_template('index.html', result=result)

@app.route('/logs')
def logs():
    try:
        with open("logs.txt", "r", encoding="utf-8") as f:
            data = f.readlines()
        return "<br>".join(data)
    except:
        return "No logs yet!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)