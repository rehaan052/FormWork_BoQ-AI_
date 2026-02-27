import pandas as pd
from src.core.formwork_engine import run_formwork_engine


class ScenarioSimulator:
    """
    Runs multiple what-if scenarios and compares results
    """

    def __init__(self, base_payload: dict):
        self.base_payload = base_payload
        self.results = []

    def run_scenario(self, scenario_name: str, overrides: dict):
        payload = self.base_payload.copy()
        payload.update(overrides)

        result = run_formwork_engine(payload)

        self.results.append({
            "scenario": scenario_name,
            "predicted_new_units": result["predicted_new_units"],
            "allocated_tasks": result["kitting_summary"]["allocated"],
            "shortages": result["kitting_summary"]["shortages"]
        })

    def get_comparison_table(self) -> pd.DataFrame:
        return pd.DataFrame(self.results)