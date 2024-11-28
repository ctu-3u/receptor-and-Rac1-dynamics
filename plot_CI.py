import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

#===========================================================#

phi = np.pi / 3

#===========================================================#

### Read data
p_s = np.zeros(spa.theo_rounds) # each reading of p
phi_s = np.zeros(spa.theo_rounds) # each reading of phi

p_s_datasetstack = np.zeros(spa.theo_rounds) # p readings stacked by datasets
phi_s_datasetstack = np.zeros(spa.theo_rounds) # phi readings stacked by datasets

ci_s = []


## record notebooks
for i in range(spa.dataset_number_int):
    ## reading
    num_samples = 0

    while True:
        num_samples += 1
        try:
            with h5py.File(".\\data\\" + spa.data_archives + "_" + str(i + 1) + "\\Estimation_" + str(num_samples) + ".h5", 'r') as f:
                p_s = f['p_est'][()]
                phi_s = f['phi_est'][()]
        except FileNotFoundError:
            num_samples -= 1
            print("Num of samples: " + str(num_samples))
            break

        # calculate CI
        ci = np.average(np.cos(phi_s_ave - [phi for i in range(len(phi_s_ave))]))
        ci_s.append(ci)

    p_s_ave /= (i + 1)
    phi_s_ave /= (i + 1)

    # plot p histogram
    plt.hist(p_s_ave, density=1, bins=20)
    plt.xlabel("Estimated p")
    plt.savefig(".\\data\\" + spa.data_archives + "_0\\P_hist_" + str(num_samples) + "_"+ str((i + 1) * spa.theo_rounds) + ".png")
    # plt.show()
    plt.clf()

    # plot CI
    plt.plot(spa.variable_list, ci_s, 'b.-')
    plt.xscale('log')
    plt.xlabel("c0")
    plt.ylabel("CI")
    plt.xticks(spa.variable_list, fontsize=6)
    plt.savefig(".\\data\\" + spa.data_archives + "_0\\CI" + "_"+ str((i + 1) * spa.theo_rounds) + ".png")
    plt.show()

    ci_s = []