import h5py

import numpy as np
import matplotlib.pyplot as plt

import simu_para as spa


parameter_list = spa.variable_list

dynamics = np.array([])

for rnd in range(len(parameter_list)):

    with h5py.File(".\\data\\" + spa.data_archives + "_1" + "\\Act_Rac_" + str(rnd + 1) + ".h5",'r') as f:
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

    plt.savefig(".\\data\\" + spa.data_archives + "_1" + "\\Act_Rac_" + str(rnd + 1) + ".png")

    # plt.show()

    plt.clf()