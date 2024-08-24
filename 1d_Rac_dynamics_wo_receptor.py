import numpy as py
import matplotlib.pyplot as plt

time_interval = 1

radius = 1 # radius of the cell, assuming the cell has a round shape
compart_num = 6283 # number of compartments we devide for simulation
Rac_initial_unitnum = 10 # initial number of Rac molecules in each compartment
Rac_total_num = Rac_initial_unitnum * compart_num # total number of Rac molecules

space_interval = radius * py.pi * 2 / compart_num

Rac_dist = [50 for i in range(2000)] + [Rac_initial_unitnum for i in range(compart_num-2000)]
Rac_inact_dist = [Rac_initial_unitnum for i in range(compart_num)]

D_act = 1
D_inact = 10

def pde2nd_Forward_time_centered_space(Rac_dist, Rac_inact_dist, D_act, D_inact, reaction, compart_num, time_interval, space_interval):
    new_Rac_dist = [0 for i in range(compart_num)]
    new_Rac_inact_dist = [0 for i in range(compart_num)]
    for i in range(compart_num):
        backstep = i - 1
        if i == 0:
            backstep = compart_num - 1
        forstep = i + 1
        if i == compart_num - 1:
            forstep = 0
        space_diff = D_act * (Rac_dist[forstep] + Rac_dist[backstep] - Rac_dist[i] * 2) / space_interval / space_interval
        new_Rac_dist[i] = (Rac_dist[i] + space_diff + reaction) * time_interval
        space_diff = D_inact * (Rac_inact_dist[forstep] + Rac_inact_dist[backstep] - Rac_inact_dist[i] * 2) / space_interval / space_interval
        new_Rac_inact_dist[i] = (Rac_inact_dist[i] + space_diff + reaction) * time_interval
    return new_Rac_dist, new_Rac_inact_dist

for i in range(500):
    new_Rac_dist, new_Rac_inact_dist = pde2nd_Forward_time_centered_space(Rac_dist=Rac_dist, Rac_inact_dist=Rac_inact_dist, D_act=D_act, D_inact=D_inact, \
        compart_num=compart_num,time_interval=time_interval,space_interval=space_interval,reaction=0)
    Rac_dist = new_Rac_dist
    Rac_inact_dist = new_Rac_inact_dist

plt.plot(range(compart_num),Rac_dist)
plt.show()
