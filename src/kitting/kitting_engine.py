import pandas as pd


class FormworkKittingEngine:
    def __init__(self, inventory_path, schedule_path):
        self.inventory = pd.read_csv(inventory_path)
        self.schedule = pd.read_csv(schedule_path)

    def build_kitting_plan(self):
        kits = []

        for _, inv in self.inventory.iterrows():
            formwork_type = inv["formwork_type"]
            total_units = inv["total_units"]
            reuse_limit = inv["reuse_limit"]

            for kit_id in range(1, total_units + 1):
                kits.append({
                    "formwork_type": formwork_type,
                    "kit_id": f"{formwork_type[:3].upper()}-KIT-{kit_id}",
                    "available_from_day": 0,
                    "reuse_left": reuse_limit
                })

        kits_df = pd.DataFrame(kits)

        allocation_log = []

        for _, task in self.schedule.iterrows():
            eligible_kits = kits_df[
                (kits_df["available_from_day"] <= task["planned_start_day"]) &
                (kits_df["reuse_left"] > 0)
            ]

            if eligible_kits.empty:
                allocation_log.append({
                    "project_id": task["project_id"],
                    "floor_no": task["floor_no"],
                    "element_type": task["element_type"],
                    "status": "SHORTAGE"
                })
                continue

            selected_kit = eligible_kits.iloc[0]

            start_day = task["planned_start_day"]
            end_day = start_day + task["cycle_time_days"]

            allocation_log.append({
                "project_id": task["project_id"],
                "floor_no": task["floor_no"],
                "element_type": task["element_type"],
                "kit_id": selected_kit["kit_id"],
                "start_day": start_day,
                "end_day": end_day,
                "status": "ALLOCATED"
            })

            kits_df.loc[
                kits_df["kit_id"] == selected_kit["kit_id"],
                ["available_from_day", "reuse_left"]
            ] = [end_day, selected_kit["reuse_left"] - 1]

        return pd.DataFrame(allocation_log)