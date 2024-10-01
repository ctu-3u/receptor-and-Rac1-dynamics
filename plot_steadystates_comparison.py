import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

label = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]
max_record = len(label)

max_round = 0
for i in np.arange(spa.rounds, 0, step = -1):
    if i % spa.sampot == 0:
        max_round = i
        break


for i in range(1, max_record + 1):
    racs = []
    with h5py.File(".\\data\\" + spa.data_archives + "\\" + str(i) + "\\Act_Rac.h5", 'r') as f:
        racs = f['act_dist_'+str(max_round)][()]
    plt.plot(range(80), racs, label = "c0=" + str(label[i-1]), linewidth = 0.75)

plt.xlim(0,80)
plt.xticks(np.arange(0,80,10))
plt.xlabel("\u03BC m")
plt.ylabel("Concentration of Active Rac")
plt.legend()
plt.savefig(".\\data\\" + spa.data_archives + "\\steady_states.pdf")
plt.show()