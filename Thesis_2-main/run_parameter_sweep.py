import itertools
import os
from main_code import run_simulation

# Define parameter ranges
A2_VALUES = [1]
THETA_VALUES = [1.2]
SIGMA_VALUES = [0.5]
MU_VALUES = [0.004]

# Create base results directory
RESULT_DIR = "results/parameter_sweep"
os.makedirs(RESULT_DIR, exist_ok=True)

for a2, theta, sigma, mu in itertools.product(A2_VALUES, THETA_VALUES, SIGMA_VALUES, MU_VALUES):
    filename = f"results_a2_{a2}_theta_{theta}_sigma_{sigma}_mu_{mu}.csv"
    output_path = os.path.join(RESULT_DIR, filename)
    run_simulation(a2=a2, theta=theta, sigma=sigma, mu=mu, output_csv=output_path)
