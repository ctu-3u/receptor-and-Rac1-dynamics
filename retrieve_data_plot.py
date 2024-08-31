import h5py

import numpy as np
import matplotlib.pyplot as plt


with h5py.File(".\\data\\083024_testrun\\Act_Rac.h5",'r') as f:
    for i in range(0,6001,50):
        act_rac_dist = f['act_dist_'+str(i)][()]
        plt.plot(range(100),act_rac_dist)
        plt.xlim(0,100)
        plt.ylim(1,15)
        plt.savefig(".\\result\\083024_testrun\\Act_rac_" + str(i) + ".jpg")
        plt.clf()
with h5py.File(".\\data\\083024_testrun\\Inact_Rac.h5",'r') as f:
    for i in range(0,6001,50):
        act_rac_dist = f['inact_dist_'+str(i)][()]
        plt.plot(range(100),act_rac_dist)
        plt.xlim(0,100)
        plt.ylim(1,15)
        plt.savefig(".\\result\\083024_testrun\\Inact_rac_" + str(i) + ".jpg")
        plt.clf()


