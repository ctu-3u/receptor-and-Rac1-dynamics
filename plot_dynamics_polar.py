import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

dynamics = np.array([])

with h5py.File(".\\data\\"+spa.datelabel+"\\Act_Rac.h5",'r') as f:
    for i in range(0, spa.rounds, spa.sampot):    
        if i == 0:
            dynamics = np.array(f['act_dist_'+str(i)][()])
        act_rac_dist = np.array(f['act_dist_'+str(i)][()])
        dynamics = np.vstack((act_rac_dist, dynamics))


# Plot contour

x = np.linspace(0, spa.cell_membrane, spa.compart_num)
y = np.arange(0, spa.rounds, spa.sampot) * spa.time_interval
X, Y = np.meshgrid(x, y)

plt.contour(X, Y, dynamics[:-1])
plt.show()