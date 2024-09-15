import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa


with h5py.File(".\\data\\"+spa.datelabel\\Act_Rac.h5",'r') as f:
    for i in range(0,spa.rounds,spa.sampot):
        act_rac_dist = f['act_dist_'+str(i)][()]
        plt.plot(range(80),act_rac_dist)
        plt.xlim(0,80)
        plt.xticks(np.arange(0,80,10))
        plt.xlabel("\u03BC m")
        plt.ylabel("Concentration of Active Rac")
        plt.savefig(".\\result\\"+spa.datelabel + "\\Act_rac_" + str(i) + ".jpg")
        plt.clf()
with h5py.File(".\\data\\"+spa.datelabel+"\\Inact_Rac.h5",'r') as f:
    for i in range(0,spa.rounds,spa.sampot):
        act_rac_dist = f['inact_dist_'+str(i)][()]
        plt.plot(range(80),act_rac_dist)
        plt.xlim(0,80)
        plt.xticks(np.arange(0,80,10))
        plt.xlabel("\u03BC m")
        plt.ylabel("Concentration of Inactive Rac")
        plt.savefig(".\\result\\"+spa.datelabel+"_testrun\\Inact_rac_" + str(i) + ".jpg")
        plt.clf()


