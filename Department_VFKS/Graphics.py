import numpy as np
import matplotlib.pyplot as plt
import scipy

dt = np.dtype([
    ('time', np.float64),
    ('pot_energy', np.float64),
    ('kin_energy', np.float64),
    ('p_x', np.float64),
    ('p_y', np.float64),
    ('p_z', np.float64),
    ('r_rms', np.float64)
])

dt1 = np.dtype([('v_pr', np.float64)])

data = np.fromfile('time_pot_energy_kin_energy_pulse.bin', dtype=dt)
data_v = np.fromfile('N_velocity.bin', dtype=dt1)

t = data['time']
U = data['pot_energy']
K = data['kin_energy']
E = U + K
p_x = data['p_x']
p_y = data['p_y']
p_z = data['p_z']
r2 = data['r_rms']
# v_x = data_v['v_x']
# v_y = data_v['v_y']
# v_z = data_v['v_z']
v_pr = data_v['v_pr']
# v = np.sqrt(v_x ** 2 + v_y ** 2 + v_z ** 2)

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

# ax.hist(v_x, bins=30, density=True, alpha=0.5, color='C0', label=r'$v_x$')
# ax.hist(v_y, bins=30, density=True, alpha=0.5, color='C1', label=r'$v_y$')
# ax.hist(v_z, bins=30, density=True, alpha=0.5, color='C2', label=r'$v_z$')

_, bins, _ = ax.hist(v_pr, bins=30, density=True, alpha=0.5, color='C0', label=r'Результаты моделирования')

N = 10 ** 3
T = 2 * np.mean(K) / (3 * N)
v_teor = np.linspace(bins[0], bins[-1], 300)
f_v_teor = (1.0 / np.sqrt(2.0 * np.pi * T)) * np.exp(- (v_teor ** 2) / (2.0 * T))

ax.plot(v_teor, f_v_teor, color='C1', linestyle='-', lw=2, label=r'Теоретическая зависимость')

ax.set_xlabel(r'$v_i, ~м/с$')
ax.set_ylabel(r'$p(v_i)$')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()

counts, bins = np.histogram(v_pr, bins=30, density=True)
v_centers = (bins[:-1] + bins[1:]) / 2

X = v_centers ** 2
Y = np.log(counts)
X_teor = np.linspace(0, max(X), 100)
Y_teor = np.log(1.0 / np.sqrt(2.0 * np.pi * T)) - (1.0 / (2.0 * T)) * X_teor

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

ax.scatter(X, Y, color='C0', marker='^', label=r'Результаты моделирования')
ax.plot(X_teor, Y_teor, color='C1', linestyle='-', lw=2, label=r'Теоретическая зависимость')

ax.set_xlabel(r'$v_i^2, м^2/с^2$')
ax.set_ylabel(r'$\ln{p(v_i)}$')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')

plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

ax.plot(t, r2, color='C0', linestyle='-', lw=2, label=r'Результаты моделирования')
res = scipy.stats.linregress(t, r2)
ax.plot(t, res.slope * t + res.intercept, color='C1', linestyle='-', lw=2, label=r'Линейная аппроксимация')

ax.set_xlabel(r'$t,~с$')
ax.set_ylabel(r'$r^2, ~м^2$')
ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
ax.minorticks_on()
ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
ax.legend()
ax.tick_params(which='both', direction='in')
plt.show()

D = res.slope / 6

print("D =", D, 'м^2/с')
print("R^2 =", res.rvalue ** 2)

v_mean = (8 * T / np.pi) ** 0.5
Lambda = 3 * D / v_mean
sigma = v_mean / (3 * 2 ** 0.5 * D)

print(T)

print('Lambda =', Lambda)
print('sigma =', sigma)

d = (4.0 / T)**(1/12)
sigma = np.pi * d ** 2
Lambda = 1 / (2 ** 0.5 * sigma)
print('Lambda =', Lambda)
print('sigma =', sigma)
Lambda = 0.05 * v_mean
sigma = 1 / (2 ** 0.5 * Lambda)
print('Lambda =', Lambda)
print('sigma =', sigma)

# fig, ax = plt.subplots(1, 1, figsize=(10, 7))
# ax.hist(v, bins=30, density=True, alpha=0.5, color='C0', label=r'$|v|$')
#
# ax.set_xlabel(r'$v, м/с$')
# ax.set_ylabel(r'$p(v)$')
# ax.grid(True, which='major', color='black', linestyle=':', linewidth=1, alpha=0.7)
# ax.minorticks_on()
# ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
# ax.legend()
# ax.tick_params(which='both', direction='in')
#
# plt.show()
