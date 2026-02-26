import pandas as pd

class OptimizedBoQCalculator:
    def __init__(self, projects_path, boq_path):
        self.projects = pd.read_csv(projects_path)
        self.boq = pd.read_csv(boq_path)

    def select_formwork_type(self, area):
        if area >= 120:
            return "Aluminum", 50
        elif area >= 60:
            return "Steel", 30
        else:
            return "Timber", 8

    def calculate_project_boq(self, project_id):
        project_boq = self.boq[self.boq["project_id"] == project_id].copy()

        optimized_cost = 0
        optimized_quantity = 0

        for _, row in project_boq.iterrows():
            formwork_type, reuse_cycles = self.select_formwork_type(row["area_sqm"])

            effective_quantity = (row["quantity"] * 1.03) / reuse_cycles
            cost = effective_quantity * row["cost_per_sqm"]

            optimized_quantity += effective_quantity
            optimized_cost += cost

        return {
            "project_id": project_id,
            "optimized_quantity": round(optimized_quantity, 2),
            "optimized_cost": round(optimized_cost, 2)
        }

    def calculate_all_projects(self):
        results = []

        for project_id in self.projects["project_id"].unique():
            results.append(self.calculate_project_boq(project_id))

        return pd.DataFrame(results)


if __name__ == "__main__":
    calculator = OptimizedBoQCalculator(
        projects_path="data/projects.csv",
        boq_path="data/boq_traditional.csv"
    )

    results = calculator.calculate_all_projects()
    print("\nOptimized BoQ Results:\n")
    print(results.head())

    results.to_csv("data/optimized_boq_summary.csv", index=False)