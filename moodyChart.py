import numpy as np
import matplotlib.pyplot as plt

# Colebrook equation definition
def colebrook(f, Re, e_D):
    return 1.0 / np.sqrt(f) + 2.0 * np.log10(e_D / 3.7 + 2.51 / (Re * np.sqrt(f)))

# Derivative of Colebrook equation
def d_colebrook(f, Re, e_D):
    return -0.5 * f**(-1.5) - (2.51 / (np.log(10) * Re)) * (1 / (f**1.5 * (e_D / 3.7 + 2.51 / (Re * np.sqrt(f)))))

# Newton-Raphson method to solve for f
def newton_raphson(f_init, Re, e_D, tol=1e-6, max_iter=100):
    f = f_init
    for _ in range(max_iter):
        f_new = f - colebrook(f, Re, e_D) / d_colebrook(f, Re, e_D)
        if abs(f_new - f) < tol:
            return f_new
        f = f_new
    return f  # Return the last computed value if not converged

# Generate Moody chart data
Re_values = np.logspace(3, 8, 50)  # Reynolds number range
roughness_values = np.array([0, 0.00001, 0.0001, 0.001, 0.01, 0.05])  # Relative roughness (e/D)

# Compute friction factor for each Re and roughness value
friction_factors = np.zeros((len(roughness_values), len(Re_values)))

for i, e_D in enumerate(roughness_values):
    for j, Re in enumerate(Re_values):
        friction_factors[i, j] = newton_raphson(0.02, Re, e_D)

# Plot Moody chart
plt.figure(figsize=(8, 6))
for i, e_D in enumerate(roughness_values):
    plt.loglog(Re_values, friction_factors[i, :], label=f'e/D = {e_D}')

plt.xlabel('Reynolds Number (Re)')
plt.ylabel('Darcy-Weisbach Friction Factor (f)')
plt.title("Moody's Chart")
plt.legend()
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.show()