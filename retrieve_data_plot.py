import h5py

import numpy as np
import matplotlib.pyplot as plt

with h5py.File(".\\data\\082824_testrun\\Act_Rac.h5",'r') as f:
    for i in range(0,5001,50):
        act_rac_dist = f['act_dist_'+str(i)][()]
        plt.plot(range(6283),act_rac_dist)
        plt.xlim(0,6283)
        plt.savefig(".\\result\\082824_testrun\\Act_rac_" + str(i) + ".jpg")
with h5py.File(".\\data\\082524_testrun\\Inact_Rac.h5",'r') as f:
    for i in range(0,5001,50):
        act_rac_dist = f['inact_dist_'+str(i)][()]
        plt.plot(range(6283),act_rac_dist)
        plt.xlim(0,6283)
        plt.savefig(".\\result\\082824_testrun\\Inact_rac_" + str(i) + ".jpg")


