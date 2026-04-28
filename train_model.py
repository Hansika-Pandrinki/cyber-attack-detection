import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB

# Sample dataset (you can later replace with real dataset)
data = pd.DataFrame({
    "duration": [10, 20, 5, 15, 30, 2, 50, 1],
    "protocol": ["tcp", "udp", "tcp", "icmp", "tcp", "udp", "icmp", "tcp"],
    "src_bytes": [100, 200, 50, 300, 500, 20, 1000, 10],
    "label": ["normal", "attack", "normal", "attack", "attack", "normal", "attack", "normal"]
})

# Encode protocol
le = LabelEncoder()
data["protocol"] = le.fit_transform(data["protocol"])

# Encode label
data["label"] = data["label"].map({"normal": 0, "attack": 1})

# Features & target
X = data[["duration", "protocol", "src_bytes"]]
y = data["label"]

# Train model
model = GaussianNB()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump((model, le), f)

print("Model trained and saved as model.pkl")