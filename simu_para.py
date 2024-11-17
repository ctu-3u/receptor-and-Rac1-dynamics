import numpy as np


# System configuration

time_interval = 0.01 # unit: s
space_interval = 0.25 # unit: um

cell_membrane = 20 # unit: um. the real length of the cell membrane

compart_num = 80 # number of compartments we devide for simulation
total_number_C = 200 # total number of active and inactive Rac

initial_stimulus = 0.5
initial_broad = 16

D_act = 0.1
D_inact = 1

# Signal gradient
class Gradient:
    def __init__(self):
        return

    # gradient parameters    
    c0 = 10
    p = 1
    phi = np.pi / 4
    # bind parameters
    K_d = 5


# Simulation running configuration

rounds = 50001
sampot = 100

# Theoretical running configuration

theo_rounds = 150
rho_receptor = 150


# File saving path

data_archives = "111724"
data_number = "7"
datelabel = data_archives + "/" + data_number
