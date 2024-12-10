import time

import h5py

import numpy as np
import matplotlib.pyplot as plt

from reaction import Reaction

import simu_para as spa


#######
# simulation parameters

time_interval = spa.time_interval # unit: s
space_interval = spa.space_interval # unit: um

# system parameters

compart_num = spa.compart_num # number of compartments we devide for simulation
total_number_C = spa.total_number_C # total number of active and inactive Rac

initial_stimulus = spa.initial_stimulus
initial_broad = spa.initial_broad
initial_inact = (total_number_C - initial_broad*initial_stimulus) / compart_num

radius = compart_num * space_interval / 2 / np.pi # radius of the cell, assuming the cell has a round shape

Rac_dist = np.append(np.linspace(initial_stimulus,initial_stimulus,initial_broad),np.linspace(0,0,compart_num-initial_broad))
# Rac_dist = np.append(np.linspace(15,15,200),np.linspace(Rac_initial_unitnum,Rac_initial_unitnum,compart_num-200))
Rac_inact_dist = np.linspace(initial_inact,initial_inact,compart_num)

Rac_total_num = np.sum(Rac_dist) + np.sum(Rac_inact_dist) # total number of Rac molecules

D_act = spa.D_act
D_inact = spa.D_inact

#######
# Modules
# FTCS scheme solution
def pde2nd_Forward_time_centered_space(Rac_dist, Rac_inact_dist, D_act, D_inact, reactObject, compart_num, time_interval, space_interval):
    new_Rac_dist = np.zeros(compart_num)
    new_Rac_inact_dist = np.zeros(compart_num)
    for i in range(compart_num):
        backstep = i - 1
        forstep = i + 1
        # ensure boundary condition
        if i == 0:
            backstep = compart_num - 1
        elif i == compart_num - 1:
            forstep = 0

        # 测试用
        # space_diff = 0

        spacepoint = (i+1)*space_interval
        timepoint = (i+1)*time_interval

        ### configure your reactions and exchanges and stimulus
        reaction_number = reactObject.exchange(Rac_dist[i],Rac_inact_dist[i]) + reactObject.receptor_random(i,compart_num,Rac_dist[i])
        stimulus_number = reactObject.stimulus(t=timepoint,x=spacepoint)

        space_diff = D_act * (Rac_dist[forstep] + Rac_dist[backstep] - Rac_dist[i] * 2) / space_interval / space_interval
        new_Rac_dist[i] = (space_diff + reaction_number + stimulus_number) * time_interval + Rac_dist[i]
        if new_Rac_dist[i] < 0:
            new_Rac_dist[i] = 0

        space_diff = D_inact * (Rac_inact_dist[forstep] + Rac_inact_dist[backstep] - Rac_inact_dist[i] * 2) / space_interval / space_interval
        new_Rac_inact_dist[i] = (space_diff - reaction_number - stimulus_number) * time_interval + Rac_inact_dist[i]
        if new_Rac_inact_dist[i] < 0:
            new_Rac_inact_dist[i] = 0
    return new_Rac_dist, new_Rac_inact_dist

# Check conservation
def check_totalnumber_conservation(Rac_total_num, Rac_dist, Rac_inact_dist):
    num = np.sum(Rac_dist) + np.sum(Rac_inact_dist)
    return num - Rac_total_num

#######
# define reaction
positive_feedback = Reaction()

# Start running simulation
time_start = time.time()


for i in range(spa.rounds):
    new_Rac_dist, new_Rac_inact_dist = pde2nd_Forward_time_centered_space(Rac_dist=Rac_dist, Rac_inact_dist=Rac_inact_dist, D_act=D_act, D_inact=D_inact, \
        compart_num=compart_num,time_interval=time_interval,space_interval=space_interval,\
            reactObject=positive_feedback)
    Rac_dist = new_Rac_dist
    Rac_inact_dist = new_Rac_inact_dist
    # record results in hdf5 file
    if i % spa.sampot == 0:
        with h5py.File(".\\data\\" + spa.data_archives + "\\Act_Rac_" + spa.data_number + ".h5",'a') as f:
            dset = f.create_dataset('act_dist_'+str(i),data=Rac_dist)
        with h5py.File(".\\data\\" + spa.data_archives + "\\Inact_Rac_" + spa.data_number + ".h5",'a') as f:
            dset = f.create_dataset('inact_dist_'+str(i),data=Rac_inact_dist)


time_end = time.time()
time_spent = time_end - time_start

# Result arrangements

print(check_totalnumber_conservation(Rac_total_num, Rac_dist, Rac_inact_dist))

print("time: " + str(time_spent))

plt.plot(range(compart_num),Rac_dist)
plt.xlim(0,compart_num-1)
# plt.show()
