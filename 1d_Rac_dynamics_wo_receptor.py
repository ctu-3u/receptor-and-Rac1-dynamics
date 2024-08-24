import time

import numpy as py
import matplotlib.pyplot as plt

# simulation parameters

time_interval = 0.1
space_interval = 1

# system parameters

compart_num = 6283 # number of compartments we devide for simulation

radius = compart_num * space_interval / 2 / py.pi # radius of the cell, assuming the cell has a round shape

Rac_initial_unitnum = 5 # initial number of Rac molecules in each compartment

Rac_dist = [15 for i in range(200)] + [Rac_initial_unitnum for i in range(compart_num-200)]
Rac_inact_dist = [Rac_initial_unitnum for i in range(compart_num)]

Rac_total_num = Rac_initial_unitnum * compart_num +  Rac_initial_unitnum * compart_num + 10*200 # total number of Rac molecules

D_act = 1
D_inact = 5


# Modules
# FTCS scheme solution
def pde2nd_Forward_time_centered_space(Rac_dist, Rac_inact_dist, D_act, D_inact, reaction, compart_num, time_interval, space_interval):
    new_Rac_dist = [0 for i in range(compart_num)]
    new_Rac_inact_dist = [0 for i in range(compart_num)]
    for i in range(compart_num):
        backstep = i - 1
        forstep = i + 1
        # ensure boundary condition
        if i == 0:
            backstep = compart_num - 1
        elif i == compart_num - 1:
            forstep = 0

        space_diff = D_act * (Rac_dist[forstep] + Rac_dist[backstep] - Rac_dist[i] * 2) / space_interval / space_interval
        new_Rac_dist[i] = (space_diff + reaction(Rac_dist[i],Rac_inact_dist[i])) * time_interval + Rac_dist[i]
        if new_Rac_dist[i] < 0:
            new_Rac_dist[i] = 0

        space_diff = D_inact * (Rac_inact_dist[forstep] + Rac_inact_dist[backstep] - Rac_inact_dist[i] * 2) / space_interval / space_interval
        new_Rac_inact_dist[i] = (space_diff - reaction(Rac_dist[i],Rac_inact_dist[i])) * time_interval + Rac_inact_dist[i]
        if new_Rac_inact_dist[i] < 0:
            new_Rac_inact_dist[i] = 0
    return new_Rac_dist, new_Rac_inact_dist


# Reaction term, including exchange term and stimuli term
def reaction(exchange, stimuli, rho_Rac_act, rho_Rac_inact):
    return exchange(rho_Rac_act,rho_Rac_inact) + stimuli(rho_Rac_act,rho_Rac_inact)

# Exchange reaction term
def exchange(rho_Rac_act, rho_Rac_inact):
    # define reaction coefficients
    k_0 = 0.067
    gamma = 1
    delta = 1
    cap_K = 1
    # exchange expression
    return rho_Rac_inact * (k_0 + gamma*rho_Rac_act*rho_Rac_act/(cap_K*cap_K+rho_Rac_act*rho_Rac_act)) - delta*rho_Rac_act


# Check conservation
def check_totalnumber_conservation(Rac_total_num, Rac_dist, Rac_inact_dist):
    num = 0
    for i in range(len(Rac_dist)):
        num += Rac_dist[i] + Rac_inact_dist[i]
    return num - Rac_total_num


# Start running simulation
time_start = time.time()


for i in range(2000):
    new_Rac_dist, new_Rac_inact_dist = pde2nd_Forward_time_centered_space(Rac_dist=Rac_dist, Rac_inact_dist=Rac_inact_dist, D_act=D_act, D_inact=D_inact, \
        compart_num=compart_num,time_interval=time_interval,space_interval=space_interval,reaction=exchange)
    Rac_dist = new_Rac_dist
    Rac_inact_dist = new_Rac_inact_dist


time_end = time.time()
time_spent = time_end - time_start


# Result arrangements

print(check_totalnumber_conservation(Rac_total_num, Rac_dist, Rac_inact_dist))

plt.plot(range(compart_num),Rac_dist)
plt.xlim(0,compart_num-1)
plt.show()
