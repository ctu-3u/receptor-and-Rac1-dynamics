import numpy as np

# File saving path

data_archives = "112524"
data_number_int = 1
data_number = str(data_number_int)
datelabel = data_archives + "/" + data_number

# Theoretical running configuration

rho_receptor = 300
theo_rounds = 10

variable_list = [0.01, 0.1, 0.5, 1, 50, 500, 1000, 5000, 10000]

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
    c0 = variable_list[data_number_int - 1]
    p = 0.2
    phi = np.pi / 3
    # bind parameters
    K_d = 5


# Simulation running configuration

rounds = 50001
sampot = 100


