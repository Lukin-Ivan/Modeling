import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import subprocess

dt = 0.01
dt_output = 0.1
x_0 = 1.0
v_0 = 1.0
omega = 1.0
t = 100000
solver_type = "heun"  # euler, heun, rk4
output_filename_coords = f"coords_{solver_type}_t_{t}_dt_{dt}_w_{omega}_x0_{x_0}_v0_{v_0}.csv"
output_filename_energy = f"enegry_{solver_type}_t_{t}_dt_{dt}_w_{omega}_x0_{x_0}_v0_{v_0}.csv"
params = {
    "output_filename_coords": output_filename_coords,
    "output_filename_energy": output_filename_energy,
    "solver_type": solver_type,
    "t": t,
    "dt": dt,
    "dt_output": dt_output,
    "x_0": x_0,
    "v_0": v_0,
    "omega": omega
}
config_path = "config.json"

with open(config_path, "w", encoding="utf-8") as file:
    json.dump(params, file, indent=4)

executable_path = "./solver.exe"

subprocess.run([executable_path, config_path], capture_output=True, text=True)

if solver_type == "euler":
    label_type = "Метод Эйлера"
elif solver_type == "heun":
    label_type = "Метод Хойна"
elif solver_type == "rk4":
    label_type = "Метод Рунге-Кутты"
else:
    label_type = solver_type

data_coords = pd.read_csv(output_filename_coords)
data_energy = pd.read_csv(output_filename_energy)

fig, ax = plt.subplots(1, 1, figsize=(10, 7))
ax.plot(data_coords['t'], data_coords['x'], color='C0', linestyle='-', lw=2, label=f"{label_type}, $\\Delta t = {dt}$ с")
ax.set_xlabel('t, c')
ax.set_ylabel('x, м')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))
ax.plot(data_coords['x'], data_coords['v'], color='C0', linestyle='-', lw=2, label=f"{label_type}, $\\Delta t = {dt}$ с")
ax.set_xlabel('x, м')
ax.set_ylabel('v, м/с')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))
ax.plot(data_energy['t'], data_energy['E'], color='C0', linestyle='-', lw=2, label=f"{label_type}, $\\Delta t = {dt}$ с")
ax.set_xlabel('t, c')
ax.set_ylabel('E/m, Дж/кг')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')
plt.show()

