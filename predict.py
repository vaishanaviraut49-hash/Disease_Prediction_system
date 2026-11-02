import joblib
import pandas as pd


# Load trained model
model_data = joblib.load("disease_model.pkl")

model = model_data["model"]
features = model_data["features"]


def predict_disease(symptoms):

    input_data = pd.DataFrame(
        [symptoms],
        columns=features
    )

    prediction = model.predict(input_data)

    return prediction[0]