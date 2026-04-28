import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
import pickle

# Sample dataset
data = pd.DataFrame({
    'duration': [0, 2, 3, 1, 5, 2, 6, 1],
    'protocol': ['tcp', 'udp', 'tcp', 'icmp', 'tcp', 'udp', 'icmp', 'tcp'],
    'src_bytes': [491, 146, 232, 199, 420, 300, 1000, 50],
    'label': ['normal', 'attack', 'normal', 'attack', 'normal', 'attack', 'attack', 'normal']
})

# Encode protocol
le = LabelEncoder()
data['protocol'] = le.fit_transform(data['protocol'])

# Convert labels
data['label'] = data['label'].map({'normal': 0, 'attack': 1})

X = data[['duration', 'protocol', 'src_bytes']]
y = data['label']

# Train model
model = GaussianNB()
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump((model, le), f)

print("Model trained successfully!")