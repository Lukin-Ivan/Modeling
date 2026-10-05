import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data_eyler = pd.read_csv('eyler_10000_0.001000.csv')
data_heun = pd.read_csv('heun_100000_0.010000.csv')
data_RK = pd.read_csv('RK_1000000_0.100000.csv')

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

# ax.plot(data_eyler['t'], data_eyler['x'], color='C0', linestyle='-', lw=2, label='$Метод~Эйлера, ~\Delta t = 0.001~с$')
# ax.plot(data_heun['t'], data_heun['x'], color='C1', linestyle='-', lw=2, label='$Метод~Хойна,~\Delta t = 0.01~с$')
# ax.plot(data_RK['t'], data_RK['x'], color='C2', linestyle='-', lw=2, label='$Метод~Рунге-Кутты,~\Delta t = 0.1~с$')

ax.set_xlabel('t, c')
ax.set_ylabel('x, м')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()

data_eyler_energy = pd.read_csv('eyler_energy_10000_0.001000.csv')
data_heun_energy = pd.read_csv('heun_energy_100000_0.010000.csv')
data_RK_energy = pd.read_csv('RK_energy_1000000_0.100000.csv')
data_RK_energy_2 = pd.read_csv('RK_energy_1000000_0.010000.csv')
data_RK_energy_3 = pd.read_csv('RK_energy_10000000_0.100000.csv')

fig1, ax = plt.subplots(1, 1, figsize=(10, 7))

# ax.plot(data_eyler_energy['t'], data_eyler_energy['E'], color='C0', linestyle='-', lw=2, label='$Метод~Эйлера, ~\Delta t = 0.001~с$')
# ax.plot(data_heun_energy['t'], data_heun_energy['E'], color='C1', linestyle='-', lw=2, label='$Метод~Хойна,~\Delta t = 0.01~с$')
# ax.plot(data_RK_energy['t'], data_RK_energy['E'], color='C2', linestyle='-', lw=2, label='$Метод~Рунге-Кутты,~\Delta t = 0.1~с$')
ax.plot(data_RK_energy_2['t'], data_RK_energy_2['E'], color='C3', linestyle='-', lw=2, label='$Метод~Рунге-Кутты,~\Delta t = 0.01~с$')
# ax.plot(data_RK_energy_3['t'], data_RK_energy_3['E'], color='C3', linestyle='-', lw=2, label='$Метод~Рунге-Кутты,~\Delta t = 0.1~с$')

ax.set_xlabel('t, c')
ax.set_ylabel('E/m, Дж/кг')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()
