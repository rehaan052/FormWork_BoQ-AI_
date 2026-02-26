import pandas as pd
import numpy as np


class TrainingDataBuilder:
    def __init__(self):
        self.projects = pd.read_csv("data/projects.csv")
        self.boq = pd.read_csv("data/boq_traditional.csv")
        self.inventory = pd.read_csv("data/inventory.csv")
        self.schedule = pd.read_csv("data/schedule.csv")

    def build(self):
        # Merge BoQ with Projects
        df = self.boq.merge(
            self.projects,
            on="project_id",
            how="left"
        )

        # Merge Schedule
        df = df.merge(
            self.schedule[
                ["project_id", "floor_no", "element_type", "cycle_time_days"]
            ],
            on=["project_id", "floor_no", "element_type"],
            how="left"
        )

        # Handle missing cycle time
        if "cycle_time_days" not in df.columns:
            df["cycle_time_days"] = 7
        else:
            df["cycle_time_days"] = df["cycle_time_days"].fillna(
                df["cycle_time_days"].median()
            )

        # Merge Inventory
        df = df.merge(
            self.inventory,
            on="formwork_type",
            how="left"
        )

        # Feature engineering
        df["required_units"] = np.ceil(
            df["area_sqm"] / df["unit_area_sqm"]
        )

        df["max_reusable_units"] = (
            df["total_units"] * df["reuse_limit"]
        )

        # Target variable
        df["required_new_units"] = (
            df["required_units"] - df["max_reusable_units"]
        ).clip(lower=0)

        # Final dataset
        final_df = df[
            [
                "project_type",
                "floors",
                "element_type",
                "formwork_type",
                "area_sqm",
                "quantity",
                "cycle_time_days",
                "total_units",
                "reuse_limit",
                "required_new_units",
            ]
        ]

        return final_df


if __name__ == "__main__":
    builder = TrainingDataBuilder()
    training_data = builder.build()

    training_data.to_csv(
        "data/processed/ml_training_data.csv",
        index=False
    )

    print("✅ ML training dataset created successfully")
    print(training_data.head())