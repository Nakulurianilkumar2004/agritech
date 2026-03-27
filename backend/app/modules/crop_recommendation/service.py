# app/modules/crop_recommendation/service.py
import os
import joblib
import numpy as np

from app.core.dependencies import require_role

# ---------------- LOAD MODELS ----------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models")
XGB_MODEL_FILE = os.path.join(MODEL_PATH, "final_xgb_model.pkl")
LABEL_ENCODER_FILE = os.path.join(MODEL_PATH, "label_encoder.pkl")
FEATURES_FILE = os.path.join(MODEL_PATH, "feature_names.pkl")

model = None
label_encoder = None
feature_names = None

def load_crop_model():
    global model, label_encoder, feature_names
    try:
        model = joblib.load(XGB_MODEL_FILE)
        label_encoder = joblib.load(LABEL_ENCODER_FILE)
        feature_names = joblib.load(FEATURES_FILE)
        print("✅ Crop Recommendation model loaded successfully.")
    except Exception as e:
        print("❌ Error loading crop model:", e)


# ---------------- PREDICTION ----------------
def predict_crop(data: dict):
    if model is None:
        raise ValueError("Model not loaded")

    try:
        # Ensure features are in correct order
        inputs = [data[f] for f in ['N','P','K','temperature','humidity','ph','rainfall']]
        features = np.array([inputs])
        pred_encoded = model.predict(features)
        pred_label = label_encoder.inverse_transform(pred_encoded)[0]
        return pred_label
    except Exception as e:
        raise ValueError(f"Prediction error: {e}")