import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

with h5py.File(".\\data\\"+spa.datelabel+"\\Act_Rac.h5",'r') as f:
    for i in range(0,spa.rounds,spa.sampot):
        act_rac_dist = f['act_dist_'+str(i)][()]