import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import subprocess
import scipy.signal
from matplotlib.animation import FuncAnimation

t_0 = 1000
dt = 0.001
dt_output = 0.01

phi_1_0 = 1.0
phi_2_0 = 1.0
phi_2_1 = 1.01
dot_phi_1_0 = 1.0
dot_phi_2_0 = 1.0
m_1 = 1.0
m_2 = 1.0
L_1 = 1.0
L_2 = 1.0
g = 9.81

solver_type = "rk4"  # euler, heun, rk4
file_type = ".bin"  # .bin, .csv

output_filename = f"data/{solver_type}_t0_{t_0}_dt_{dt}_m1_{m_1}_m2_{m_2}_L1_{L_1}_L2_{L_2}_phi10_{phi_1_0}_phi20_{phi_2_0}_dotphi10_{dot_phi_1_0}_dotphi20_{dot_phi_2_0}{file_type}"
params = {
    "output_filename": output_filename,
    "solver_type": solver_type,
    "t_0": t_0,
    "dt": dt,
    "dt_output": dt_output,
    "phi_1_0": phi_1_0,
    "phi_2_0": phi_2_0,
    "dot_phi_1_0": dot_phi_1_0,
    "dot_phi_2_0": dot_phi_2_0,
    "m_1": m_1,
    "m_2": m_2,
    "L_1": L_1,
    "L_2": L_2,
    "g": g
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

data0 = None
if file_type == ".csv":
    data0 = pd.read_csv(output_filename)
if file_type == ".bin":
    dtype = np.dtype([
        ('t', np.float64),
        ('phi_1', np.float64),
        ('dot_phi_1', np.float64),
        ('phi_2', np.float64),
        ('dot_phi_2', np.float64),
        ('E', np.float64),
    ])
    data0 = np.fromfile(output_filename, dtype=dtype)

t = data0['t']
phi_1 = data0['phi_1']
dot_phi_1 = data0['dot_phi_1']
phi_2 = data0['phi_2']
dot_phi_2 = data0['dot_phi_2']
E = data0['E']

x_10 = L_1 * np.sin(phi_1)
y_10 = - L_1 * np.cos(phi_1)
x_20 = x_10 + L_2 * np.sin(phi_2)
y_20 = y_10 - L_2 * np.cos(phi_2)

output_filename = f"data/{solver_type}_t0_{t_0}_dt_{dt}_m1_{m_1}_m2_{m_2}_L1_{L_1}_L2_{L_2}_phi10_{phi_1_0}_phi20_{phi_2_1}_dotphi10_{dot_phi_1_0}_dotphi20_{dot_phi_2_0}{file_type}"
params = {
    "output_filename": output_filename,
    "solver_type": solver_type,
    "t_0": t_0,
    "dt": dt,
    "dt_output": dt_output,
    "phi_1_0": phi_1_0,
    "phi_2_0": phi_2_1,
    "dot_phi_1_0": dot_phi_1_0,
    "dot_phi_2_0": dot_phi_2_0,
    "m_1": m_1,
    "m_2": m_2,
    "L_1": L_1,
    "L_2": L_2,
    "g": g
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

data1 = None
if file_type == ".csv":
    data1 = pd.read_csv(output_filename)
if file_type == ".bin":
    dtype = np.dtype([
        ('t', np.float64),
        ('phi_1', np.float64),
        ('dot_phi_1', np.float64),
        ('phi_2', np.float64),
        ('dot_phi_2', np.float64),
        ('E', np.float64),
    ])
    data1 = np.fromfile(output_filename, dtype=dtype)

t = data1['t']
phi_1 = data1['phi_1']
dot_phi_1 = data1['dot_phi_1']
phi_2 = data1['phi_2']
dot_phi_2 = data1['dot_phi_2']
E = data1['E']

x_11 = L_1 * np.sin(phi_1)
y_11 = - L_1 * np.cos(phi_1)
x_21 = x_11 + L_2 * np.sin(phi_2)
y_21 = y_11 - L_2 * np.cos(phi_2)

fig_anim, ax = plt.subplots(figsize=(7, 7))

ax.set_xlim(-(L_1 + L_2) * 1.1, (L_1 + L_2) * 1.1)
ax.set_ylim(-(L_1 + L_2) * 1.1, (L_1 + L_2) * 1.1)
ax.set_aspect('equal')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.tick_params(which='both', direction='in')

line_1, = ax.plot([], [], color='C0', marker='o', lw=2, markersize=8)
line_2, = ax.plot([], [], color='C1', marker='o', lw=2, markersize=8)
time_text = ax.text(0.03, 0.95, '', transform=ax.transAxes)


def update(i):
    line_1.set_data([0, x_10[i], x_20[i]], [0, y_10[i], y_20[i]])
    line_2.set_data([0, x_11[i], x_21[i]], [0, y_11[i], y_21[i]])
    time_text.set_text(f't = {t[i]:.2f} с')
    return line_1, line_2, time_text


anim = FuncAnimation(fig_anim, update, frames=range(0, len(t), 10), interval=10, blit=True)
plt.show()
