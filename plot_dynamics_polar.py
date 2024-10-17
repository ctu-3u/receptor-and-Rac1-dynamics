import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa

dynamics = np.array([])

with h5py.File(".\\data\\" + spa.data_archives + "\\Act_Rac_" + spa.data_number + ".h5",'r') as f:
    for i in range(0, spa.rounds, spa.sampot):    
        if i == 0:
            dynamics = np.array(f['act_dist_'+str(i)][()])
        else:
            dynamics = np.vstack((dynamics, np.array(f['act_dist_'+str(i)][()])))


# Plot contour

x = np.linspace(0, spa.cell_membrane, spa.compart_num)
y = np.arange(0, spa.rounds, spa.sampot) * spa.time_interval
X, Y = np.meshgrid(x, y)

fig = plt.figure()

dyn_c = plt.contourf(X, Y, dynamics, levels = 15, cmap = 'viridis')
plt.xlabel("location on membrane (\u03BCm)")
plt.ylabel("time (s)")
plt.title("dynamics: Rac concentration on membrane")
# plt.clabel(dyn_c, inline = True)

cbar = fig.colorbar(dyn_c)
cbar.ax.set_ylabel('Rac concentration')

plt.savefig(".\\result\\" + spa.data_archives + "\\" + spa.data_number + ".pdf")
plt.savefig(".\\result\\" + spa.data_archives + "\\" + spa.data_number + ".png")

plt.show()

plt.clf()