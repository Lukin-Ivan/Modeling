import numpy as np
import matplotlib.pyplot as plt

dt = np.dtype([
    ('time', np.float64),
    ('pot_energy', np.float64),
    ('kin_energy', np.float64),
    ('p_x', np.float64),
    ('p_y', np.float64),
    ('p_z', np.float64)
])

dt1 = np.dtype([
    ('v_x', np.float64),
    ('v_y', np.float64),
    ('v_z', np.float64)
])

data = np.fromfile('time_pot_energy_kin_energy_pulse.bin', dtype=dt)
data_v = np.fromfile('N_velocity.bin', dtype=dt1)

t = data['time']
U = data['pot_energy']
K = data['kin_energy']
E = U + K
p_x = data['p_x']
p_y = data['p_y']
p_z = data['p_z']
v_x = data_v['v_x']
v_y = data_v['v_y']
v_z = data_v['v_z']
v = np.sqrt(v_x ** 2 + v_y ** 2 + v_z ** 2)

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

ax.plot(t, U, color='C0', linestyle='-', lw=2, label='$W_{pot}(t)$')
ax.plot(t, K, color='C1', linestyle='-', lw=2, label='$E_{kin}(t)$')
ax.plot(t, E, color='C2', linestyle='-', lw=2, label='E(t)')

ax.set_xlabel('t, c')
ax.set_ylabel('Е, LJ units')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

ax.plot(t, p_x, color='C0', linestyle='-', lw=2, label=r'$\dfrac{p_{x}}{\sqrt{\langle p^2 \rangle}}$')
ax.plot(t, p_y, color='C1', linestyle='-', lw=2, label=r'$\dfrac{p_{y}}{\sqrt{\langle p^2 \rangle}}$')
ax.plot(t, p_z, color='C2', linestyle='-', lw=2, label=r'$\dfrac{p_{z}}{\sqrt{\langle p^2 \rangle}}$')

ax.set_xlabel('t, c')
ax.set_ylabel(r'$\dfrac{p}{\sqrt{\langle p^2 \rangle}}$')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

ax.hist(v_x, bins=30, density=True, alpha=0.5, color='C0', label=r'$v_x$')
ax.hist(v_y, bins=30, density=True, alpha=0.5, color='C1', label=r'$v_y$')
ax.hist(v_z, bins=30, density=True, alpha=0.5, color='C2', label=r'$v_z$')

ax.set_xlabel(r'$v, м/с$')
ax.set_ylabel(r'$p(v)$')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

ax.hist(v, bins=30, density=True, alpha=0.5, color='C0', label=r'$|v|$')

ax.set_xlabel(r'$v, м/с$')
ax.set_ylabel(r'$p(v)$')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()
