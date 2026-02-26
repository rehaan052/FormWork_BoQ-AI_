import pandas as pd


class InventoryOptimizer:
    def __init__(self, inventory_path, optimized_boq_path):
        self.inventory = pd.read_csv(inventory_path)
        self.optimized_boq = pd.read_csv(optimized_boq_path)

    def calculate_inventory_impact(self):
        results = []

        for _, inv in self.inventory.iterrows():
            formwork_type = inv["formwork_type"]

            # Total reusable area available
            available_area = (
                inv["total_units"]
                * inv["unit_area_sqm"]
                * inv["reuse_limit"]
            )

            # Total required area from optimized BoQ
            required_area = self.optimized_boq[
                self.optimized_boq["formwork_type"] == formwork_type
            ]["area_sqm"].sum()

            shortage_area = max(0, required_area - available_area)
            surplus_area = max(0, available_area - required_area)

            results.append({
                "formwork_type": formwork_type,
                "available_area_sqm": round(available_area, 2),
                "required_area_sqm": round(required_area, 2),
                "shortage_area_sqm": round(shortage_area, 2),
                "surplus_area_sqm": round(surplus_area, 2),
                "inventory_status": (
                    "Sufficient"
                    if shortage_area == 0
                    else "Purchase Required"
                )
            })

        return pd.DataFrame(results)


if __name__ == "__main__":
    optimizer = InventoryOptimizer(
        inventory_path="data/inventory.csv",
        optimized_boq_path="data/boq_optimized.csv"
    )

    inventory_summary = optimizer.calculate_inventory_impact()

    print("\nInventory Impact Summary:\n")
    print(inventory_summary)

    inventory_summary.to_csv(
        "data/inventory_impact_summary.csv",
        index=False
    )

    print("\nSaved → data/inventory_impact_summary.csv")