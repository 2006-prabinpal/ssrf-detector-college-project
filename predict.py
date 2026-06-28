import joblib
import numpy as np
from detector.features import extract_features  # Ensure this function is importable

# 1. Load the saved model and scaler
model = joblib.load('model/logistic_model.pkl')
scaler = joblib.load('model/scaler.pkl')

def classify_url(url):
    # 2. Extract the same 6 features
    features = np.array(extract_features(url)).reshape(1, -1)
    
    # 3. Apply the same scaling
    features_scaled = scaler.transform(features)
    
    # 4. Predict
    prediction = model.predict(features_scaled)
    probability = model.predict_proba(features_scaled)
    
    label = "SSRF" if prediction[0] == 1 else "SAFE"
    confidence = np.max(probability[0]) * 100
    
    return label, confidence

# --- Example Usage ---
if __name__ == "__main__":
    new_urls = [
        "http://internal.service.local/api/v1",
        "https://www.google.com/search?q=test",
        "http://169.254.169.254/metadata/v1/user-data"
    ]
    
    print(f"{'PREDICTION':<10} | {'CONFIDENCE':<10} | {'URL'}")
    print("-" * 60)
    for url in new_urls:
        label, conf = classify_url(url)
        print(f"{label:<10} | {conf:>8.2f}% | {url}")