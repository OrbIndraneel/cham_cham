"""
Flood Prediction Model — Person A's deliverable
Trains an XGBoost classifier on the flood risk dataset, evaluates it,
and saves the model so it can be loaded by the API layer (Person B).

Run:
    python train_flood_model.py
Outputs:
    flood_model.json   -> trained XGBoost model
    encoders.pkl        -> label encoders for categorical columns (needed at inference time)
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)
from xgboost import XGBClassifier

DATA_PATH = "flood_risk_india_synthetic.csv"  # swap with real Kaggle CSV if you get it
MODEL_PATH = "flood_model.json"
ENCODERS_PATH = "encoders.pkl"

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
print(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------
# 2. Encode categoricals
# ---------------------------------------------------------------
categorical_cols = ["Land_Cover", "Soil_Type"]
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Region is high-cardinality and mostly informational — drop for training,
# keep it only for reporting/demo readability
feature_cols = [
    "Rainfall_mm", "Temperature_C", "Humidity_pct", "River_Discharge_m3s",
    "Water_Level_m", "Elevation_m", "Land_Cover", "Soil_Type",
    "Population_Density", "Infrastructure", "Historical_Floods",
]
X = df[feature_cols]
y = df["Flood_Occurred"]

# ---------------------------------------------------------------
# 3. Train/test split (stratified, since classes are imbalanced ~24%)
# ---------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------------
# 4. Handle class imbalance -> scale_pos_weight
# ---------------------------------------------------------------
neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
scale_pos_weight = neg / pos
print(f"Class balance -> neg:{neg} pos:{pos}  scale_pos_weight={scale_pos_weight:.2f}")

# ---------------------------------------------------------------
# 5. Train XGBoost
# ---------------------------------------------------------------
model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.08,
    subsample=0.85,
    colsample_bytree=0.85,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
)
model.fit(X_train, y_train)

# ---------------------------------------------------------------
# 6. Evaluate
# ---------------------------------------------------------------
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n--- Evaluation ---")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred):.3f}")
print(f"F1       : {f1_score(y_test, y_pred):.3f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, y_proba):.3f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ---------------------------------------------------------------
# 7. Feature importance (good for your slides/demo)
# ---------------------------------------------------------------
importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nFeature Importance:")
print(importances)

# ---------------------------------------------------------------
# 8. Save model + encoders
# ---------------------------------------------------------------
model.save_model(MODEL_PATH)
with open(ENCODERS_PATH, "wb") as f:
    pickle.dump(encoders, f)

print(f"\nSaved model -> {MODEL_PATH}")
print(f"Saved encoders -> {ENCODERS_PATH}")
