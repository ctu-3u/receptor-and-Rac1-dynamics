import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

#===========================================================#

phi = np.pi / 4

#===========================================================#

### Read data

## record notebooks
p_s = []
phi_s = []

ci_s = []

## reading
num_samples = 0

while True:
    num_samples += 1
    try:
        with h5py.File(".\\data\\" + spa.data_archives + "\\Estimation_" + str(num_samples) + ".h5", 'r') as f:
            p_s = f['p_est'][()]
            phi_s = f['phi_est'][()]
    except FileNotFoundError:
        num_samples -= 1
        print("Num of samples: " + str(num_samples))
        break

    # plot p histogram
    plt.hist(p_s, density=1, bins=20)
    plt.xlabel("Estimated p")
    plt.savefig(".\\data\\" + spa.data_archives + "\\P_hist_" + str(num_samples) + ".png")
    # plt.show()
    plt.clf()

    # calculate CI
    ci = np.average(np.cos(phi_s - [phi for i in range(len(phi_s))]))
    ci_s.append(ci)

# plot CI
plt.plot(spa.variable_list, ci_s, 'b.-')
plt.xscale('log')
plt.xlabel("c0")
plt.ylabel("CI")
plt.xticks(spa.variable_list, fontsize=6)
plt.savefig(".\\data\\" + spa.data_archives + "\\CI" + ".png")
plt.show()
