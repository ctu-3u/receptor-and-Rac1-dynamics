
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


# Simulation running configuration

rounds = 600001
sampot = 1000

data_archives = "101624_inits"
data_number = "4"
datelabel = "101624_inits" + "/" + data_number
