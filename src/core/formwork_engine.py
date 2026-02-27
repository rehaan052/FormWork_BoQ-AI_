from src.ml.predict import predict_formwork
from src.kitting.kitting_engine import FormworkKittingEngine


def run_formwork_engine(payload: dict):
    """
    Central orchestration logic:
    ML prediction + kitting plan
    """

    # ML prediction
    prediction = predict_formwork(payload)

    # Kitting logic
    engine = FormworkKittingEngine(
        inventory_path="data/inventory.csv",
        schedule_path="data/schedule.csv"
    )

    kitting_plan = engine.build_kitting_plan()

    return {
        "predicted_new_units": int(round(prediction)),
        "kitting_summary": {
            "total_tasks": len(kitting_plan),
            "allocated": int((kitting_plan["status"] == "ALLOCATED").sum()),
            "shortages": int((kitting_plan["status"] == "SHORTAGE").sum())
        }
    }