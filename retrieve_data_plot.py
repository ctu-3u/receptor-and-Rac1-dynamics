import h5py

import numpy as np
import matplotlib.pyplot as plt

for i in range(0,5000,50):
    with h5py.File(".\\data\\082524_testrun\\Act_Rac_" + str(i) + ".h5",'r') as f:
        a_group_key = list(f.keys())[0]
        act_rac_dist = list(f[a_group_key])
        plt.plot(range(6283),act_rac_dist)
        plt.xlim(0,6283)
        plt.savefig(".\\result\\082624_testrun\\Act_rac_" + str(i) + ".jpg")
    with h5py.File(".\\data\\082524_testrun\\Inact_Rac_" + str(i) + ".h5",'r') as f:
        a_group_key = list(f.keys())[0]
        inact_rac_dist = list(f[a_group_key])
        plt.plot(range(6283),inact_rac_dist)
        plt.xlim(0,6283)
        plt.savefig(".\\result\\082624_testrun\\Inact_rac_" + str(i) + ".jpg")
