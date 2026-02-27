import joblib
import pandas as pd

MODEL_PATH = "models/formwork_demand_model.pkl"

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


# 🔒 SAFE DEFAULTS — MUST MATCH TRAINING VALUES
CATEGORICAL_DEFAULTS = {
    "project_type": "Residential",
    "element_type": "Slab",
    "formwork_type": "Aluminium",
}

NUMERIC_DEFAULTS = {
    "floors": 1,
    "area_sqm": 100.0,
    "quantity": 1,
    "cycle_time_days": 7,
    "total_units": 0,
    "reuse_limit": 10,
}


def predict_formwork(payload: dict) -> float:
    """
    Robust ML inference with categorical safety
    """
    model = load_model()

    # Model was trained with pandas
    required_columns = list(model.feature_names_in_)

    final_payload = {}

    for col in required_columns:
        if col in payload and payload[col] is not None:
            final_payload[col] = payload[col]
        else:
            # Fill categorical safely
            if col in CATEGORICAL_DEFAULTS:
                final_payload[col] = CATEGORICAL_DEFAULTS[col]
            else:
                final_payload[col] = NUMERIC_DEFAULTS.get(col, 0)

    input_df = pd.DataFrame([final_payload])[required_columns]

    # 🔐 Ensure no NaN survives
    input_df = input_df.fillna({
        **CATEGORICAL_DEFAULTS,
        **NUMERIC_DEFAULTS
    })

    prediction = model.predict(input_df)[0]
    return float(prediction)