from src.optimization.scenario_simulator import ScenarioSimulator

base_payload = {
    "project_type": "Residential",
    "floors": 8,
    "area": 12000,
    "duration_days": 180
}

simulator = ScenarioSimulator(base_payload)

simulator.run_scenario("Baseline", {})
simulator.run_scenario("Higher Reuse", {"reuse_limit": 30})
simulator.run_scenario("Faster Cycle", {"cycle_time_days": 5})

df = simulator.get_comparison_table()
print(df)