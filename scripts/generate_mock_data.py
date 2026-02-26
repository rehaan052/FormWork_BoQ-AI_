import pandas as pd
import numpy as np
import os

np.random.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# 1. PROJECTS (100)
# -----------------------------
n_projects = 100
projects = pd.DataFrame({
    "project_id": [f"P{str(i).zfill(3)}" for i in range(1, n_projects + 1)],
    "project_type": np.random.choice(["Residential", "Commercial", "Industrial"], n_projects),
    "floors": np.random.randint(5, 35, n_projects),
    "location": np.random.choice(["Metro", "Tier-1", "Tier-2"], n_projects),
    "start_day": np.random.randint(1, 50, n_projects)
})
projects.to_csv(f"{DATA_DIR}/projects.csv", index=False)

# -----------------------------
# 2. INVENTORY (300)
# -----------------------------
inventory = pd.DataFrame({
    "formwork_type": np.repeat(["Steel", "Aluminum", "Timber"], 100),
    "unit_area_sqm": np.random.uniform(1.5, 3.5, 300),
    "total_units": np.random.randint(50, 500, 300),
    "reuse_limit": np.random.randint(30, 60, 300)
})
inventory.to_csv(f"{DATA_DIR}/inventory.csv", index=False)

# -----------------------------
# 3. SCHEDULE (10,000)
# -----------------------------
n_schedule = 10000

schedule = pd.DataFrame({
    "project_id": np.random.choice(projects["project_id"], n_schedule),
    "floor_no": np.random.randint(1, 35, n_schedule),
    "element_type": np.random.choice(["Column", "Beam", "Slab", "Wall"], n_schedule),
    "planned_start_day": np.random.randint(1, 365, n_schedule),
    "cycle_time_days": np.random.randint(3, 10, n_schedule)
})

schedule["actual_start_day"] = (
    schedule["planned_start_day"]
    + np.random.randint(-2, 6, n_schedule)
)

schedule.to_csv(f"{DATA_DIR}/schedule.csv", index=False)

# -----------------------------
# 4. TRADITIONAL BOQ (10,000)
# -----------------------------
boq_traditional = schedule.copy()

boq_traditional["formwork_type"] = np.random.choice(
    ["Steel", "Aluminum", "Timber"], n_schedule
)
boq_traditional["area_sqm"] = np.round(np.random.uniform(10, 100, n_schedule), 2)
boq_traditional["quantity"] = np.random.randint(5, 25, n_schedule)

cost_map = {
    "Steel": 850,
    "Aluminum": 1100,
    "Timber": 600
}

boq_traditional["cost_per_sqm"] = boq_traditional["formwork_type"].map(cost_map)
boq_traditional["total_cost"] = (
    boq_traditional["area_sqm"]
    * boq_traditional["quantity"]
    * boq_traditional["cost_per_sqm"]
)

boq_traditional.to_csv(f"{DATA_DIR}/boq_traditional.csv", index=False)

# -----------------------------
# 5. OPTIMIZED BOQ (10,000)
# -----------------------------
boq_optimized = boq_traditional.copy()

# Simulate reuse + kitting optimization
reuse_factor = np.random.uniform(0.6, 0.9, n_schedule)
boq_optimized["optimized_quantity"] = np.ceil(
    boq_optimized["quantity"] * reuse_factor
).astype(int)

boq_optimized["optimized_cost"] = (
    boq_optimized["optimized_quantity"]
    * boq_optimized["area_sqm"]
    * boq_optimized["cost_per_sqm"]
)

boq_optimized["cost_saving"] = (
    boq_optimized["total_cost"] - boq_optimized["optimized_cost"]
)

boq_optimized.to_csv(f"{DATA_DIR}/boq_optimized.csv", index=False)

# -----------------------------
print("✅ ALL MOCK DATASETS GENERATED SUCCESSFULLY")
print("📁 Files created:")
print("- projects.csv")
print("- inventory.csv")
print("- schedule.csv")
print("- boq_traditional.csv")
print("- boq_optimized.csv")