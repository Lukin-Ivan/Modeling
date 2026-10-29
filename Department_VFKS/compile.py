import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import json
import subprocess

n_per_side = 6
total_time = 10
start_record_time = 2
delta_t = 0.00001
delta_t_output = 0.001
density = 10
m = 1.0
N = n_per_side ** 3

output_file_name_parametrs = f"data/parametrs_N_{N}_density_{density}_t_{total_time}_start_record_{start_record_time}_dt_{delta_t}.csv"
output_file_name_velocities = f"data/velocities_N_{N}_density_{density}_t_{total_time}_start_record_{start_record_time}_dt_{delta_t}.csv"
output_file_name_coordinates = f"data/coordinates_N_{N}_density_{density}_t_{total_time}_start_record_{start_record_time}_dt_{delta_t}.xyz"

params = {
    "output_file_name_parametrs": output_file_name_parametrs,
    "output_file_name_velocities": output_file_name_velocities,
    "output_file_name_coordinates": output_file_name_coordinates,
    "n_per_side": n_per_side,
    "total_time": total_time,
    "start_record_time": start_record_time,
    "delta_t": delta_t,
    "delta_t_output": delta_t_output,
    "density": density,
    "m": m
}
config_path = "config.json"

with open(config_path, "w", encoding="utf-8") as file:
    json.dump(params, file, indent=4)

executable_path = "./Modeling.exe"
result = subprocess.run([executable_path, config_path], capture_output=True, text=True)


data_parametrs = pd.read_csv(output_file_name_parametrs)
data_velocities = pd.read_csv(output_file_name_velocities)

t = data_parametrs['t'] - start_record_time
U = data_parametrs['U']
K = data_parametrs['K']
E = U + K
p_x = data_parametrs['p_x']
p_y = data_parametrs['p_y']
p_z = data_parametrs['p_z']
r2 = data_parametrs['r_rms']
vacf = data_parametrs['vacf']
v_pr = data_velocities['v_pr']

fig = plt.figure(figsize=(11, 12))
fig.suptitle(f"N = {N}, t = {total_time} с, $\\Delta t = {delta_t}$ с", fontsize=14)
gs = plt.GridSpec(3, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[0, 1])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[2, 0])
ax6 = fig.add_subplot(gs[2, 1])

ax1.plot(t, U, color='C0', linestyle='-', lw=2, label='$W_{pot}(t)$')
ax1.plot(t, K, color='C1', linestyle='-', lw=2, label='$E_{kin}(t)$')
ax1.plot(t, E, color='C2', linestyle='-', lw=2, label='E(t)')
ax1.set_xlabel('t, c')
ax1.set_ylabel('Е, LJ units')

ax2.plot(t, p_x, color='C0', linestyle='-', lw=2, label=r'$\dfrac{p_{x}}{\sqrt{\langle p^2 \rangle}}$')
ax2.plot(t, p_y, color='C1', linestyle='-', lw=2, label=r'$\dfrac{p_{y}}{\sqrt{\langle p^2 \rangle}}$')
ax2.plot(t, p_z, color='C2', linestyle='-', lw=2, label=r'$\dfrac{p_{z}}{\sqrt{\langle p^2 \rangle}}$')
ax2.set_xlabel('t, c')
ax2.set_ylabel(r'$\dfrac{p}{\sqrt{\langle p^2 \rangle}}$')

_, bins, _ = ax3.hist(v_pr, bins=30, density=True, alpha=0.5, color='C0', label=r'Результаты моделирования')
T = 2 * np.mean(K) / (3 * N)
v_teor = np.linspace(bins[0], bins[-1], 300)
f_v_teor = (1.0 / np.sqrt(2.0 * np.pi * T)) * np.exp(- (v_teor ** 2) / (2.0 * T))
ax3.plot(v_teor, f_v_teor, color='C1', linestyle='-', lw=2, label=r'Теоретическая зависимость')
ax3.set_xlabel(r'$v_i, ~м/с$')
ax3.set_ylabel(r'$p(v_i)$')

counts, bins = np.histogram(v_pr, bins=30, density=True)
v_centers = (bins[:-1] + bins[1:]) / 2
X = v_centers ** 2
Y = np.log(counts)
X_teor = np.linspace(0, max(X), 100)
Y_teor = np.log(1.0 / np.sqrt(2.0 * np.pi * T)) - (1.0 / (2.0 * T)) * X_teor
ax4.scatter(X, Y, color='C0', marker='^', label=r'Результаты моделирования')
ax4.plot(X_teor, Y_teor, color='C1', linestyle='-', lw=2, label=r'Теоретическая зависимость')
ax4.set_xlabel(r'$v_i^2, м^2/с^2$')
ax4.set_ylabel(r'$\ln{p(v_i)}$')

ax5.plot(t, r2, color='C0', linestyle='-', lw=2, label=r'Результаты моделирования')
res = scipy.stats.linregress(t, r2)
ax5.plot(t, res.slope * t + res.intercept, color='C1', linestyle='-', lw=2, label=r'Линейная аппроксимация')
ax5.set_xlabel(r'$t,~с$')
ax5.set_ylabel(r'$r^2, ~м^2$')

ax6.plot(t, vacf, color='C0', linestyle='-', lw=2, label='АКФС')
ax6.set_xlabel('t, c')
ax6.set_ylabel('VACF')

for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
    ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
    ax.minorticks_on()
    ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
    ax.tick_params(which='both', direction='in')
    ax.legend()

plt.show()

print(result.stdout)

D = res.slope / 6

print("D (r^2(t)) =", D)
print("R^2 =", res.rvalue ** 2)

v_mean = (8 * T / np.pi) ** 0.5
Lambda = 3 * D / v_mean
sigma = v_mean / (3 * 2 ** 0.5 * D)


print('Lambda =', Lambda)
print('sigma =', sigma)

d = (4.0 / T) ** (1 / 12)
sigma = np.pi * d ** 2
Lambda = 1 / (2 ** 0.5 * sigma)
print('Lambda =', Lambda)
print('sigma =', sigma)
Lambda = 0.05 * v_mean
sigma = 1 / (2 ** 0.5 * Lambda)
print('Lambda =', Lambda)
print('sigma =', sigma)


# fig, ax = plt.subplots(1, 1, figsize=(10, 7))
#
# ax.plot(t, U, color='C0', linestyle='-', lw=2, label='$W_{pot}(t)$')
# ax.plot(t, K, color='C1', linestyle='-', lw=2, label='$E_{kin}(t)$')
# ax.plot(t, E, color='C2', linestyle='-', lw=2, label='E(t)')
#
# ax.set_xlabel('t, c')
# ax.set_ylabel('Е, LJ units')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
#
# plt.show()
#
# fig, ax = plt.subplots(1, 1, figsize=(10, 7))
#
# ax.plot(t, p_x, color='C0', linestyle='-', lw=2, label=r'$\dfrac{p_{x}}{\sqrt{\langle p^2 \rangle}}$')
# ax.plot(t, p_y, color='C1', linestyle='-', lw=2, label=r'$\dfrac{p_{y}}{\sqrt{\langle p^2 \rangle}}$')
# ax.plot(t, p_z, color='C2', linestyle='-', lw=2, label=r'$\dfrac{p_{z}}{\sqrt{\langle p^2 \rangle}}$')
#
# ax.set_xlabel('t, c')
# ax.set_ylabel(r'$\dfrac{p}{\sqrt{\langle p^2 \rangle}}$')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
#
# plt.show()
#
# fig, ax = plt.subplots(1, 1, figsize=(10, 7))
#
# # ax.hist(v_x, bins=30, density=True, alpha=0.5, color='C0', label=r'$v_x$')
# # ax.hist(v_y, bins=30, density=True, alpha=0.5, color='C1', label=r'$v_y$')
# # ax.hist(v_z, bins=30, density=True, alpha=0.5, color='C2', label=r'$v_z$')
#
# _, bins, _ = ax.hist(v_pr, bins=30, density=True, alpha=0.5, color='C0', label=r'Результаты моделирования')
#
# T = 2 * np.mean(K) / (3 * N)
# v_teor = np.linspace(bins[0], bins[-1], 300)
# f_v_teor = (1.0 / np.sqrt(2.0 * np.pi * T)) * np.exp(- (v_teor ** 2) / (2.0 * T))
#
# ax.plot(v_teor, f_v_teor, color='C1', linestyle='-', lw=2, label=r'Теоретическая зависимость')
#
# ax.set_xlabel(r'$v_i, ~м/с$')
# ax.set_ylabel(r'$p(v_i)$')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
#
# plt.show()
#
# counts, bins = np.histogram(v_pr, bins=30, density=True)
# v_centers = (bins[:-1] + bins[1:]) / 2
#
# X = v_centers ** 2
# Y = np.log(counts)
# X_teor = np.linspace(0, max(X), 100)
# Y_teor = np.log(1.0 / np.sqrt(2.0 * np.pi * T)) - (1.0 / (2.0 * T)) * X_teor
#
# ax.scatter(X, Y, color='C0', marker='^', label=r'Результаты моделирования')
# ax.plot(X_teor, Y_teor, color='C1', linestyle='-', lw=2, label=r'Теоретическая зависимость')
#
# ax.set_xlabel(r'$v_i^2, м^2/с^2$')
# ax.set_ylabel(r'$\ln{p(v_i)}$')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
#
# plt.show()
#
# fig, ax = plt.subplots(1, 1, figsize=(10, 7))
#
# ax.plot(t, r2, color='C0', linestyle='-', lw=2, label=r'Результаты моделирования')
# res = scipy.stats.linregress(t, r2)
# ax.plot(t, res.slope * t + res.intercept, color='C1', linestyle='-', lw=2, label=r'Линейная аппроксимация')
#
# ax.set_xlabel(r'$t,~с$')
# ax.set_ylabel(r'$r^2, ~м^2$')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
# plt.show()
#
# fig, ax = plt.subplots(1, 1, figsize=(10, 7))
# ax.plot(t, vacf, color='C0', linestyle='-', lw=2, label='АКФС')
# ax.set_xlabel('t, c')
# ax.set_ylabel('VACF')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
# plt.show()
#
