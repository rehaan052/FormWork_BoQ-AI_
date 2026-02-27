import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# Load dataset
df = pd.read_csv("data/processed/ml_training_data.csv")

# Features & Target
X = df.drop("required_new_units", axis=1)
y = df["required_new_units"]

# Categorical & Numeric columns
categorical_cols = [
    "project_type",
    "element_type",
    "formwork_type"
]

numeric_cols = [
    "floors",
    "area_sqm",
    "quantity",
    "cycle_time_days",
    "total_units",
    "reuse_limit"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols),
    ]
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

# Pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("model", model),
    ]
)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"✅ Model trained successfully")
print(f"📉 Mean Absolute Error: {mae:.2f} units")

# Save model
joblib.dump(pipeline, "models/formwork_demand_model.pkl")

print("💾 Model saved at models/formwork_demand_model.pkl")