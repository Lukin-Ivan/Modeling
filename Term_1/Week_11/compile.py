import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import subprocess
import scipy.signal
from matplotlib.animation import FuncAnimation


def find_amplitude(x, n=20):
    maxima, _ = scipy.signal.find_peaks(x)
    minima, _ = scipy.signal.find_peaks(-x)
    return (np.mean(x[maxima[-n:]]) - np.mean(x[minima[-n:]])) / 2


t_0 = 100
dt = 0.001
dt_output = 0.01

phi_1_0 = 1.0
phi_2_0 = 1.01
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

data = None
if file_type == ".csv":
    data = pd.read_csv(output_filename)
if file_type == ".bin":
    dtype = np.dtype([
        ('t', np.float64),
        ('phi_1', np.float64),
        ('dot_phi_1', np.float64),
        ('phi_2', np.float64),
        ('dot_phi_2', np.float64),
        ('E', np.float64),
    ])
    data = np.fromfile(output_filename, dtype=dtype)

t = data['t']
phi_1 = data['phi_1']
dot_phi_1 = data['dot_phi_1']
phi_2 = data['phi_2']
dot_phi_2 = data['dot_phi_2']
E = data['E']

x_1 = L_1 * np.sin(phi_1)
y_1 = - L_1 * np.cos(phi_1)
x_2 = x_1 + L_2 * np.sin(phi_2)
y_2 = y_1 - L_2 * np.cos(phi_2)

fig = plt.figure(figsize=(10, 7))
fig.suptitle(f"{label_type}, $\\Delta t = {dt}$ с", fontsize=14)
gs = plt.GridSpec(3, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[2, :])

ax1.plot(t, phi_1, color='C9', linestyle='-', lw=2, label=r'Зависимость $\varphi_1(t)$')
ax1.set_xlabel('t, c')
ax1.set_ylabel(r'$\varphi_1$, рад')

ax2.plot(phi_1, dot_phi_1, color='C4', linestyle='-', lw=2, label='Фазовый портрет')
ax2.set_xlabel(r'$\varphi_1$, рад')
ax2.set_ylabel(r'$\dot \varphi_1$, рад/с')

ax3.plot(t, phi_2, color='C9', linestyle='-', lw=2, label=r'Зависимость $\varphi_2(t)$')
ax3.set_xlabel('t, c')
ax3.set_ylabel(r'$\varphi_2$, рад')

ax4.plot(phi_2, dot_phi_2, color='C4', linestyle='-', lw=2, label='Фазовый портрет')
ax4.set_xlabel(r'$\varphi_2$, рад')
ax4.set_ylabel(r'$\dot \varphi_2$, рад/с')

ax5.plot(t, E, color='C1', linestyle='-', lw=2, label='Закон сохранения энергии')
ax5.set_xlabel('t, c')
ax5.set_ylabel('E, Дж')

fig.legend()

for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
    ax.minorticks_on()
    ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
    ax.tick_params(which='both', direction='in')

plt.show()

fig_anim, ax = plt.subplots(figsize=(7, 7))

ax.set_xlim(-(L_1 + L_2) * 1.1, (L_1 + L_2) * 1.1)
ax.set_ylim(-(L_1 + L_2) * 1.1, (L_1 + L_2) * 1.1)
ax.set_aspect('equal')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.tick_params(which='both', direction='in')

line, = ax.plot([], [], marker='o', lw=2, markersize=8)
time_text = ax.text(0.03, 0.95, '', transform=ax.transAxes)


def update(i):
    line.set_data([0, x_1[i], x_2[i]], [0, y_1[i], y_2[i]])
    time_text.set_text(f't = {t[i]:.2f} с')
    return line, time_text


anim = FuncAnimation(fig_anim, update, frames=range(0, len(t), 2), interval=20, blit=True)
plt.show()