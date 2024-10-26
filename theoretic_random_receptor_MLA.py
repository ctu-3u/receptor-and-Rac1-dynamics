import time

import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

#===============================================================#
## receptor normally distribute along the membrane
compart_num = spa.compart_num
rho_receptor = 10
num_receptor = rho_receptor * compart_num

## record the receptors binding or unbinding states
binding_states = np.zeros(num_receptor)

## Signal gradient parameters
class Gradient:
    def __init__(self):
        return

    # gradient parameters    
    c0 = 0.04
    p = 1
    phi = np.pi / 2
    # bind parameters
    K_d = 5

gradi = Gradient()

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
    if z1 != 0:
        est_phi = np.arctan(z2 / z1)
    elif z2 >= 0:
        est_phi = np.pi / 2
    else:
        est_phi = - np.pi / 2
    

    est_p_std = np.sqrt(2 / param_mu)
    est_phi_std = np.sqrt( 2 / param_mu / est_p / est_p)

    return est_p, est_phi, est_p_std, est_phi_std


### MAIN ###
p_s = np.zeros(rounds)
phi_s = np.zeros(rounds)
pstd_s = np.zeros(rounds)
phistd_s = np.zeros(rounds)

for i in range(rounds):
    binding_states = generate_binding(num_receptor, gradi)

    p_s[i], phi_s[i], pstd_s[i], phistd_s[i] = MLA_estimation(num_receptor, gradi, binding_states[:])

# plt.errorbar(np.arange(rounds), p_s, yerr=pstd_s, fmt='-o', ecolor='red', capsize=5, label='p estimated')
plt.errorbar(np.arange(rounds), phi_s, yerr=phistd_s, fmt='-o', ecolor='blue', capsize=5, label='\u03C6 estimated')
plt.show()