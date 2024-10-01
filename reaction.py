import numpy as np

class Reaction:
    def __init__(self):
        return

    def reaction(self,rho_act,rho_inact,t=0,x=0):
        num_exchg = self.exchange(func=self.positive_feedback_Hills,t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        num_stimu = self.stimulus(func=self.square_initial_pulse,t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        num_react = num_exchg + num_stimu
        return num_react

    def exchange(self,rho_act,rho_inact,t=0,x=0):
        num = self.positive_feedback_Hills(rho_act=rho_act,rho_inact=rho_inact,t=t,x=x)
        return num
    
    def stimulus(self,t,x,rho_act=0,rho_inact=0):
        num = self.zerotest(t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        return num


    # Exchange expression
    
    def positive_feedback_Hills(self,rho_act,rho_inact,t=0,x=0):
        # configure reaction coefficients
        k_0 = 0.067
        gamma = 1
        delta = 1
        cap_K = 1
        # exchange expression
        rate_exchange = k_0 + gamma*rho_act*rho_act/(cap_K*cap_K+rho_act*rho_act)
        num_exchange = rho_inact * rate_exchange - delta*rho_act
        return num_exchange

    def receptor_signal(self, x_i, num_compart, rho_inact):
        ## effect of receptor binding under signal gradient
        # configure reaction coefficients
        c0 = 0.01
        K_d = 1
        rho_rec = 1
        # concerntration
        c_xi = c0 / 2 * (1 - np.cos(2 * np.pi * x_i / num_compart))
        # receptor binding
        return c_xi / (c_xi + K_d) * rho_rec * rho_inact

    # Stimulus expression
    
    def square_initial_pulse(self,t,x,rho_act=0,rho_inact=0):
        # configure stimulus coefficients
        addition = 1.5
        t_end = 20
        x_end = 1
        # stimulus expression
        if t < t_end and x <= x_end:
            return addition
        return 0

    def transient_localized_simuli(self,t,x,rho_act=0,rho_inact=0):
        # configure stimulus coefficients
        t1 = 20
        t2 = 25
        capS = 0.5
        x_end = 1
        if x >= 0 and x <= 2 * x_end:
            if t <= t1:
                st = capS/2
            elif t <= t2:
                st = capS/4 * (1 + np.cos(np.pi*(t-t1)/(t2-t1)))
            else:
                return 0
            return st * (1 + np.cos(np.pi*x))
        return 0

    # Test for non-reaction expression
    def zerotest(self,t,x,rho_act=0,rho_inact=0):
        return 0