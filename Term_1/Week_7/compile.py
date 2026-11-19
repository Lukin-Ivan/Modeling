import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import subprocess

dt = 0.001
dt_output = 0.01
x_0 = 2
v_0 = 0
omega = 1.0
t = 100
solver_type = "heun"  # euler, heun, rk4
file_type = ".bin"  # .bin, .csv
output_filename = f"data/{solver_type}_t_{t}_dt_{dt}_w_{omega}_x0_{x_0}_v0_{v_0}{file_type}"
params = {
    "output_filename": output_filename,
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

data = None
if file_type == ".csv":
    data = pd.read_csv(output_filename)
if file_type == ".bin":
    dtype = np.dtype([
        ('t', np.float64),
        ('x', np.float64),
        ('v', np.float64),
        ('E', np.float64)
    ])
    data = np.fromfile(output_filename, dtype=dtype)

fig = plt.figure(figsize=(10, 7))
fig.suptitle(f"{label_type}, $\\Delta t = {dt}$ с", fontsize=14)
gs = plt.GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

ax1.plot(data['t'], data['x'], color='C9', linestyle='-', lw=2, label='Зависимость x(t)')
ax1.set_xlabel('t, c')
ax1.set_ylabel('x, рад')

ax2.plot(data['x'], data['v'], color='C4', linestyle='-', lw=2, label='Фазовый портрет')
ax2.set_xlabel('x, рад')
ax2.set_ylabel('v, рад/с')

ax3.plot(data['t'], data['E'], color='C1', linestyle='-', lw=2, label='Закон сохранения энергии')
ax3.set_xlabel('t, c')
ax3.set_ylabel('E/m, Дж/кг')

fig.legend()

for ax in [ax1, ax2, ax3]:
    ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
    ax.minorticks_on()
    ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
    ax.tick_params(which='both', direction='in')

plt.show()
