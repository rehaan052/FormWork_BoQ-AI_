import pandas as pd

class BoQComparison:
    def __init__(self, traditional_path, optimized_path):
        self.traditional = pd.read_csv(traditional_path)
        self.optimized = pd.read_csv(optimized_path)

    def compare(self):
        df = pd.merge(
            self.traditional,
            self.optimized,
            on="project_id",
            how="inner"
        )

        df["cost_saved"] = df["total_cost"] - df["optimized_cost"]
        df["cost_saved_pct"] = (df["cost_saved"] / df["total_cost"]) * 100

        df["quantity_saved"] = df["total_quantity"] - df["optimized_quantity"]
        df["quantity_saved_pct"] = (
            df["quantity_saved"] / df["total_quantity"]
        ) * 100

        return df.round(2)

    def save_results(self, output_path):
        comparison_df = self.compare()
        comparison_df.to_csv(output_path, index=False)
        return comparison_df


if __name__ == "__main__":
    comparator = BoQComparison(
        traditional_path="data/traditional_boq_summary.csv",
        optimized_path="data/optimized_boq_summary.csv"
    )

    result = comparator.save_results("data/boq_comparison_summary.csv")

    print("\nBoQ Comparison Summary:\n")
    print(result.head())