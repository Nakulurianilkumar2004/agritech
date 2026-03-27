import pandas as pd
import pickle
import traceback
import os

# ---------------- MODELS ----------------
rf_model = preprocessor = le = None

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

def load_models():
    """Load RandomForest, Preprocessor, and LabelEncoder for fertilizer prediction"""
    global rf_model, preprocessor, le
    try:
        rf_model = pickle.load(open(os.path.join(MODEL_DIR, "random_forest_modelferti.pkl"), "rb"))
        preprocessor = pickle.load(open(os.path.join(MODEL_DIR, "preprocessorferti.pkl"), "rb"))
        le = pickle.load(open(os.path.join(MODEL_DIR, "label_encoderferti.pkl"), "rb"))
        print("✅ Fertilizer models loaded successfully")
    except Exception as e:
        print("❌ Error loading fertilizer models:", e)
        traceback.print_exc()

# ---------------- PREDICTION ----------------
def predict_fertilizer(data: dict):
    if rf_model is None or preprocessor is None or le is None:
        return {"error": "Fertilizer model not loaded"}
    
    try:
        # Convert input dictionary to DataFrame
        input_df = pd.DataFrame([data])

        # Transform features
        X_processed = preprocessor.transform(input_df)

        # Predict and decode
        pred_encoded = rf_model.predict(X_processed)
        prediction_label = le.inverse_transform(pred_encoded)[0]

        return {"result": prediction_label}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

# Load models automatically at import
load_models()