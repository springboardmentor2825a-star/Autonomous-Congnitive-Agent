import pandas as pd
import numpy as np

def execute(plan_steps):
    """
    Execute each step with simulated data analysis.
    """
    results = []

    # Simulated sales data
    data = pd.DataFrame({
        "Product": ["A", "B", "C", "D"],
        "Sales": [100, 150, 80, 200]
    })

    for step in plan_steps:
        if "Analyze" in step:
            # Use numpy to compute mean sales
            mean_sales = np.mean(data["Sales"])
            result = f"{step} -> Mean Sales: {mean_sales}"
        elif "Collect" in step:
            result = f"{step} -> Collected data: {data.shape[0]} rows"
        else:
            result = f"Executed step: {step}"
        results.append(result)

    return results
