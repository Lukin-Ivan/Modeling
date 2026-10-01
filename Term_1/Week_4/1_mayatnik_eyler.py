import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data_1 = pd.read_csv('eyler_100_0.001000.csv')
data_2 = pd.read_csv('eyler_100_0.000100.csv')
data_3 = pd.read_csv('eyler_100_0.000010.csv')
data_4 = pd.read_csv('eyler_100_0.000001.csv')
data_5 = pd.read_csv('eyler_100_0.000000.csv')

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

# ax.plot(data_1['t'], data_1['x'], color='C0', linestyle='-', lw=2, label='$\Delta t = 0.001~с$')
# ax.plot(data_2['t'], data_2['x'], color='C1', linestyle='-', lw=2, label='$\Delta t = 0.0001~с$')
# ax.plot(data_3['t'], data_3['x'], color='C2', linestyle='-', lw=2, label='$\Delta t = 0.00001~с$')
# ax.plot(data_4['t'], data_4['x'], color='C3', linestyle='-', lw=2, label='$\Delta t = 0.000001~с$')
# ax.plot(data_5['t'], data_4['x'], color='C4', linestyle='-', lw=2, label='$\Delta t = 0.0000001~с$')

real_val = 2 ** 0.5 * math.cos(data_1['t'].iloc[-1] - 1 / 2 ** 0.5)
print(real_val)
print(data_5['x'].iloc[-1])

ax.set_xlabel('t, c')
ax.set_ylabel('x, м')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()
