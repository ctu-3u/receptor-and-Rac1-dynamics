import time

import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

t0 = time.time()

#===============================================================#
## receptor normally distribute along the membrane
compart_num = spa.compart_num
rho_receptor = spa.rho_receptor
num_receptor = rho_receptor * compart_num

## record the receptors binding or unbinding states
binding_states = np.zeros(num_receptor)

## Signal gradient parameters
gradi = spa.Gradient()

## Runing rounds
rounds = spa.theo_rounds

#===============================================================#

##  Generate binding states randomly

def generate_binding(num_receptor, gradi):
    binding_probs = np.zeros(num_receptor)
    binding_states = np.zeros(num_receptor)

    for i in range(num_receptor):
        # calculate binding probability
        conc_x = gradi.c0 * np.exp(gradi.p / 2 * np.cos(2 * np.pi * i / num_receptor - gradi.phi))
        prob = conc_x / (conc_x + gradi.K_d)
        binding_probs[i] = prob
        # bind randomly
        np.random.seed()
        t = np.random.rand()
        if t <= prob:
            binding_states[i] = 1
    
    return binding_states


## MLA estimation
def MLA_estimation(num_receptor, gradi, binding_states):
    # estimator
    z1, z2 = [0, 0]
    cos_s = [np.cos(2 * np.pi * i / num_receptor) for i in range(num_receptor)]
    sin_s = [np.sin(2 * np.pi * i / num_receptor) for i in range(num_receptor)]

    z1 = np.sum(cos_s * binding_states)
    z2 = np.sum(sin_s * binding_states)

    # estimation
    param_mu = num_receptor * gradi.c0 * gradi.K_d / 4 / np.power(gradi.c0 + gradi.K_d, 2)

    est_p = np.sqrt(z1 * z1 + z2 * z2) / param_mu

    if z1 == 0 and z2 == 0:
        est_phi = 0
    elif z1 == 0 and z2 > 0:
        est_phi = np.pi / 2
    elif z1 == 0 and z2 < 0:
        est_phi = -np.pi / 2
    elif z1 > 0:
        est_phi = np.arctan(z2 / z1)
    elif z1 < 0:
        est_phi = np.pi + np.arctan(z2 / z1)
    
    est_p_std = np.sqrt(2 / param_mu)
    if gradi.p == 0:
        est_phi_std = 0
    else:
        est_phi_std = np.sqrt( 2 / param_mu / gradi.p / gradi.p)

    return est_p, est_phi, est_p_std, est_phi_std


### MAIN ###
p_s = np.zeros(rounds)
phi_s = np.zeros(rounds)
pstd_s = np.zeros(rounds)
phistd_s = np.zeros(rounds)

for i in range(rounds):
    binding_states = generate_binding(num_receptor, gradi)

    p_s[i], phi_s[i], pstd_s[i], phistd_s[i] = MLA_estimation(num_receptor, gradi, binding_states[:])

with h5py.File(".\\data\\" + spa.data_archives + "_" + str(spa.dataset_number) + "\\Estimation_" + spa.data_number + ".h5",'a') as f:
    dset1 = f.create_dataset('p_est', data=p_s)
    dset2 = f.create_dataset('phi_est', data=phi_s)
    dset3 = f.create_dataset('pstd_est', data=pstd_s)
    dset4 = f.create_dataset('phistd_est', data=phistd_s)
    dset5 = f.create_dataset('p_ave', data=np.average(p_s))
    dset5 = f.create_dataset('phi_ave', data=np.average(phi_s))


plt.errorbar(np.arange(rounds), p_s, yerr=pstd_s, fmt='-', ecolor='red', capsize=5, label='p estimated')
plt.savefig(".\\data\\" + spa.data_archives + "_" + str(spa.dataset_number) + "\\p_estimation_" + spa.data_number + ".png")
plt.clf()
plt.errorbar(np.arange(rounds), phi_s, yerr=phistd_s, fmt='-', ecolor='blue', capsize=5, label='\u03C6 estimated')
plt.savefig(".\\data\\" + spa.data_archives + "_" + str(spa.dataset_number) + "\\phi_estimation_" + spa.data_number + ".png")



print(f"Est p: {np.average(p_s)}, Est phi: {np.average(phi_s)}")

print(time.time() - t0)