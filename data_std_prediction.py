import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

#===============================================================#
## simulation numbers =
simulateds = spa.dataset_number_int
simurounds = spa.theo_rounds

## receptor normally distribute along the membrane
compart_num = spa.compart_num
rho_receptor = spa.rho_receptor
num_receptor = rho_receptor * compart_num

## Signal gradient parameters
gradi = spa.Gradient()

#===============================================================#

def predicts(simulated_nume, simurounds):
    c0s = spa.variable_list

    param_mu = [num_receptor * c0 * gradi.K_d / 4 / np.power(c0 + gradi.K_d, 2) for c0 in c0s]
    p_std_t = np.array([np.sqrt(2 / mu) for mu in param_mu]) # theoretic std of p
    phi_std_t = np.array([np.sqrt(2 / mu / gradi.p / gradi.p) for mu in param_mu]) # theoretic std of phi

    p_diffs = np.zeros(len(c0s)) # difference between estimated p and real p
    p_std_e = np.zeros(len(c0s)) # estimated std of p
    phi_diffs = np.zeros(len(c0s)) # difference between estimated phi and real phi
    phi_std_e = np.zeros(len(c0s)) # estimated std of phi


    ## reading
    for i in range(simulated_nume):
        nume_c0 = 0

        while True:
            try:
                with h5py.File(".\\data\\" + spa.data_archives + "_" + str(i + 1) +"\\Estimation_" + str(nume_c0 + 1) + ".h5", 'r') as f:
                    p_s = f['p_est'][()]
                    phi_s = f['phi_est'][()]

                    diff_p = np.abs(np.average(p_s) - gradi.p)
                    p_diffs[nume_c0] += diff_p
                    std_p = np.std(p_s)
                    p_std_e[nume_c0] += std_p

                    diff_phi = np.abs(np.average(phi_s) - gradi.phi)
                    phi_diffs[nume_c0] += diff_phi
                    std_phi = np.std(phi_s)
                    phi_std_e[nume_c0] += std_phi
                
                nume_c0 += 1


            except FileNotFoundError:
                print("Num of samples: " + str(nume_c0))
                break
    
    p_diffs /= simulated_nume
    p_std_e /= simulated_nume
    phi_diffs /= simulated_nume
    phi_std_e /= simulated_nume

    ### record results
    with h5py.File(".\\data\\" + spa.data_archives + "_0\\Ther_vs_Esti_" + str(simulated_nume * simurounds) + ".h5", 'w') as f:
        dset1 = f.create_dataset('p_diff', data = p_diffs)
        dset2 = f.create_dataset('p_std', data = p_std_e)
        dset3 = f.create_dataset('phi_diff', data = phi_diffs)
        dset4 = f.create_dataset('phi_std', data = phi_std_e)
        dset5 = f.create_dataset('theoretical_std_p', data = p_std_t)
        dset6 = f.create_dataset('theoretical_std_phi', data = phi_std_t)

    return p_diffs, p_std_t, p_std_e, phi_diffs, phi_std_t, phi_std_e


def visualization(simulated_nume, p_diffs, p_std_t, p_std_e, phi_diffs, phi_std_t, phi_std_e):
    c0s = spa.variable_list

    ### Visualize deviations
    plt.plot(c0s, [i / gradi.p for i in p_diffs], '.-', label = "p dev")
    plt.plot(c0s, [i / gradi.phi for i in phi_diffs], '.-', label = 'phi dev')
    plt.plot(c0s, [np.abs(p_std_e[i] - p_std_t[i]) / p_std_t[i] for i in range(len(p_std_t))], '.-', label = "p std dev")
    plt.plot(c0s, [np.abs(phi_std_e[i] - phi_std_t[i]) / phi_std_t[i] for i in range(len(phi_std_t))], '.-', label = "phi std dev")
    plt.legend()
    plt.xscale('log')
    plt.title("Deviation of Numerical Estimated from Theoretical " + str(simulated_nume * simurounds))
    plt.savefig(".\\data\\" + spa.data_archives + "_0\\Deviat_Theo_Esti_" + str(simulated_nume * simurounds) + ".png")
    plt.show()
    plt.clf()

    ### Visualize prediction quality
    plt.plot(c0s, [p_diffs[i] / p_std_t[i] for i in range(len(p_std_t))], '.-', label = "p")
    plt.plot(c0s, [phi_diffs[i] / phi_std_t[i] for i in range(len(phi_std_t))], '.-', label = "phi")
    plt.legend()
    plt.xscale('log')
    plt.title("Estimation Accuracy " + str(simulated_nume * simurounds))
    plt.savefig(".\\data\\" + spa.data_archives + "_0\\Esti_Accu_" + str(simulated_nume * simurounds) + ".png")
    plt.show()
    plt.clf()

    ####
    plt.plot(c0s, phi_std_e, label = 'esti')
    plt.plot(c0s, phi_std_t, label = 'theo')
    plt.xscale('log')
    plt.legend()
    plt.title("Estimation Quality " + str(simulated_nume * simurounds))
    plt.savefig(".\\data\\" + spa.data_archives + "_0\\Esti_Qual_" + str(simulated_nume * simurounds) + ".png")
    plt.show()
    plt.clf()

#=====================MAIN==============================#
for simutimes in range(1, simulateds + 1):
    p_diffs, p_std_t, p_std_e, phi_diffs, phi_std_t, phi_std_e = predicts(simutimes, simurounds)

    visualization(simutimes, p_diffs, p_std_t, p_std_e, phi_diffs, phi_std_t, phi_std_e)



