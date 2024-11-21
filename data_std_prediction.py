import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

#===============================================================#
## receptor normally distribute along the membrane
compart_num = spa.compart_num
rho_receptor = spa.rho_receptor
num_receptor = rho_receptor * compart_num

## Signal gradient parameters
gradi = spa.Gradient()

#===============================================================#

c0s = spa.variable_list

param_mu = [num_receptor * c0 * gradi.K_d / 4 / np.power(c0 + gradi.K_d, 2) for c0 in c0s]

p_diffs = [] # difference between estimated p and real p
p_std_t = [np.sqrt(2 / mu) for mu in param_mu] # theoretic std of p
p_std_e = [] # estimated std of p
phi_diffs = [] # difference between estimated phi and real phi
phi_std_t = [np.sqrt(2 / mu / gradi.p / gradi.p) for mu in param_mu] # theoretic std of phi
phi_std_e = [] # estimated std of phi


## reading
num_samples = 0

while True:
    num_samples += 1
    try:
        with h5py.File(".\\data\\" + spa.data_archives + "\\Estimation_" + str(num_samples) + ".h5", 'r') as f:
            p_s = f['p_est'][()]
            phi_s = f['phi_est'][()]

            diff_p = np.abs(np.average(p_s) - gradi.p)
            p_diffs.append(diff_p)
            std_p = np.std(p_s)
            p_std_e.append(std_p)

            diff_phi = np.abs(np.average(phi_s) - gradi.phi)
            phi_diffs.append(diff_phi)
            std_phi = np.std(phi_s)
            phi_std_e.append(std_phi)


    except FileNotFoundError:
        num_samples -= 1
        print("Num of samples: " + str(num_samples))
        break


### record results
with h5py.File(".\\data\\" + spa.data_archives + "\\Ther_vs_Esti" + str(num_samples) + ".h5", 'w') as f:
    dset1 = f.create_dataset('p_diff', data = p_diffs)
    dset2 = f.create_dataset('p_std', data = p_std_e)
    dset3 = f.create_dataset('phi_diff', data = phi_diffs)
    dset4 = f.create_dataset('phi_std', data = phi_std_e)
    dset5 = f.create_dataset('theoretical_std_p', data = p_std_t)
    dset6 = f.create_dataset('theoretical_std_phi', data = phi_std_t)

#=====================Visualization=========================#

### Visualize deviations
plt.plot(c0s, [i / gradi.p for i in p_diffs], '.-', label = "p dev")
plt.plot(c0s, [i / gradi.phi for i in phi_diffs], '.-', label = 'phi dev')
plt.plot(c0s, [np.abs(p_std_e[i] - p_std_t[i]) / p_std_t[i] for i in range(len(p_std_t))], '.-', label = "p std dev")
plt.plot(c0s, [np.abs(phi_std_e[i] - phi_std_t[i]) / phi_std_t[i] for i in range(len(phi_std_t))], '.-', label = "phi std dev")
plt.legend()
plt.xscale('log')
plt.title("Deviation of Numerical Estimated from Theoretical")
plt.savefig(".\\data\\" + spa.data_archives + "\\Deviat_Theo_Esti" + ".png")
plt.show()

### Visualize prediction quality
plt.plot(c0s, [p_diffs[i] / p_std_t[i] for i in range(len(p_std_t))], '.-', label = "p")
plt.plot(c0s, [phi_diffs[i] / phi_std_t[i] for i in range(len(phi_std_t))], '.-', label = "phi")
plt.legend()
plt.xscale('log')
plt.title("Estimation Quality")
plt.savefig(".\\data\\" + spa.data_archives + "\\Esti_Qual" + ".png")
plt.show()

####
plt.plot(c0s, phi_std_e, label = 'esti')
plt.plot(c0s, phi_std_t, label = 'theo')
plt.xscale('log')
plt.legend()
plt.show()