import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import joblib


# Load training data
data = pd.read_csv("ml/error_dataset.csv")


# Separate code and labels
X = data["code"]
y = data["error_type"]


# Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])


# Train the model
model.fit(X, y)


# Save trained model
joblib.dump(model, "ml/error_model.pkl")


print("Model trained successfully!")
print("Training examples:", len(data))
print("Error categories:", list(model.classes_))