import pandas as pd

class TraditionalBoQCalculator:
    def __init__(self, projects_path, boq_path):
        self.projects = pd.read_csv(projects_path)
        self.boq = pd.read_csv(boq_path)

    def calculate_project_boq(self, project_id):
        """
        Calculates total quantity and cost for a single project
        using traditional (non-optimized) logic
        """
        project_boq = self.boq[self.boq["project_id"] == project_id]

        total_quantity = project_boq["quantity"].sum()
        total_cost = project_boq["total_cost"].sum()   # ✅ FIXED

        return {
            "project_id": project_id,
            "total_quantity": round(total_quantity, 2),
            "total_cost": round(total_cost, 2)
        }

    def calculate_all_projects(self):
        """
        Calculates BoQ for all projects
        """
        results = []

        for project_id in self.projects["project_id"].unique():
            result = self.calculate_project_boq(project_id)
            results.append(result)

        return pd.DataFrame(results)


if __name__ == "__main__":
    calculator = TraditionalBoQCalculator(
        projects_path="data/projects.csv",
        boq_path="data/boq_traditional.csv"
    )

    results = calculator.calculate_all_projects()
    print("\nTraditional BoQ Results:\n")
    print(results.head())

    results.to_csv("data/traditional_boq_summary.csv", index=False)