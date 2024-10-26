import time

import h5py

import numpy as np
import matplotlib.pyplot as plt

from reaction import Reaction

import simu_para as spa

# receptor normally distribute along the membrane
compart_num = spa.compart_num
rho_receptor = 1
num_receptor = rho_receptor * compart_num

# record the receptors binding or unbinding states
binding_states = np.zeros(compart_num)

# Generate binding states randomly