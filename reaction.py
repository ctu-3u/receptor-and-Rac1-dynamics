class Reaction:
    def __init__(self):
        return

    def reaction(self,rho_act,rho_inact,t=0,x=0):
        num_exchg = self.exchange(func=self.positive_feedback_Hills,t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        num_stimu = self.stimulus(func=self.square_initial_pulse,t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        num_react = num_exchg + num_stimu
        return num_react

    # Exchange expression
    def exchange(self,rho_act,rho_inact,t=0,x=0):
        num = self.positive_feedback_Hills(t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        return num
    
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

    # stimulus expression
    def stimulus(self,t,x,rho_act=0,rho_inact=0):
        num = self.square_initial_pulse(t=t,x=x,rho_act=rho_act,rho_inact=rho_inact)
        return num

    def square_initial_pulse(self,t,x,rho_act=0,rho_inact=0):
        # configure stimulus coefficients
        addition = 10
        t_end = 1
        x_end = 100
        # stimulus expression
        if t < t_end and x < x_end:
            return addition
        return 0

    def zerotest(self,t,x,rho_act=0,rho_inact=0):
        return 0