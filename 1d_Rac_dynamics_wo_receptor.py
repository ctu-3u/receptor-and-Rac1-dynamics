import time

import h5py

import numpy as np
import matplotlib.pyplot as plt

from reaction import Reaction


#######
# simulation parameters

time_interval = 0.1
space_interval = 1

# system parameters

compart_num = 6283 # number of compartments we devide for simulation

radius = compart_num * space_interval / 2 / np.pi # radius of the cell, assuming the cell has a round shape

Rac_initial_unitnum = 5 # initial number of Rac molecules in each compartment

Rac_dist = np.linspace(Rac_initial_unitnum,Rac_initial_unitnum,compart_num)
# Rac_dist = np.append(np.linspace(15,15,200),np.linspace(Rac_initial_unitnum,Rac_initial_unitnum,compart_num-200))
Rac_inact_dist = np.linspace(int(Rac_initial_unitnum/2),int(Rac_initial_unitnum/2),compart_num)

Rac_total_num = np.sum(Rac_dist) + np.sum(Rac_inact_dist) # total number of Rac molecules

D_act = 0.1
D_inact = 1

#######
# Modules
# FTCS scheme solution
def pde2nd_Forward_time_centered_space(Rac_dist, Rac_inact_dist, D_act, D_inact, reactObject, compart_num, time_interval, space_interval,timepoint):
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

        reaction_number = reactObject.exchange(Rac_dist[i],Rac_inact_dist[i])
        stimulus_number = reactObject.stimulus(t=timepoint,x=i)
        space_diff = D_act * (Rac_dist[forstep] + Rac_dist[backstep] - Rac_dist[i] * 2) / space_interval / space_interval
        new_Rac_dist[i] = (space_diff + reaction_number + stimulus_number) * time_interval + Rac_dist[i]
        if new_Rac_dist[i] < 0:
            new_Rac_dist[i] = 0

        space_diff = D_inact * (Rac_inact_dist[forstep] + Rac_inact_dist[backstep] - Rac_inact_dist[i] * 2) / space_interval / space_interval
        new_Rac_inact_dist[i] = (space_diff - reaction_number) * time_interval + Rac_inact_dist[i]
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


for i in range(5001):
    new_Rac_dist, new_Rac_inact_dist = pde2nd_Forward_time_centered_space(Rac_dist=Rac_dist, Rac_inact_dist=Rac_inact_dist, D_act=D_act, D_inact=D_inact, \
        compart_num=compart_num,time_interval=time_interval,space_interval=space_interval,\
            reactObject=positive_feedback, timepoint=(i+1)*time_interval)
    Rac_dist = new_Rac_dist
    Rac_inact_dist = new_Rac_inact_dist
    # record results in hdf5 file
    if i % 50 == 0:
        with h5py.File(".\\data\\082824_testrun\\Act_Rac.h5",'w') as f:
            dset = f.create_dataset('act_dist_'+str(i),data=Rac_dist)
        with h5py.File(".\\data\\082824_testrun\\Inact_Rac.h5",'w') as f:
            dset = f.create_dataset('inact_dist_'+str(i),data=Rac_inact_dist)


time_end = time.time()
time_spent = time_end - time_start

# Result arrangements

print(check_totalnumber_conservation(Rac_total_num, Rac_dist, Rac_inact_dist))

print("time: " + str(time_spent))

plt.plot(range(compart_num),Rac_dist)
plt.xlim(0,compart_num-1)
plt.show()
