'''
Hydrogen tank model
Refer to : Simulation of PVeWind-hybrid systems combined with
hydrogen storage for rural electrification
'''
p_0 =101325
class hydrogen_tank():
    R = 8.314 # J/(K.mol)
    def __init__(self, p_init = 0, Volume_tank = 6, T = 273.15, p_max = 200):

        self.p_init = p_init *p_0
        self.p = self.p_init
        self.p_max = p_max*p_0
        self.V = Volume_tank
        self.T = T
        self.M = (self.p_init * self.V)/(self.R * self.T)
        self.mass_max = (self.p_max * self.V)/(self.R * self.T)/500#kg

    def blow_up(self, q_h2=0.1, time = 3600):
        # q_h2 depends on the output pressure of compress and gas bottle pressure, gas pipe section area
        # pipe flow coefficient
        self.M = self. M +  q_h2 * time
        self.p = self.M *self.R * self.T / self.V
        if self.p <= 200*p_0:
            return self.p /p_0
        else:
            self.M = self.M - q_h2 * time
            self.p = self.M * self.R * self.T / self.V
            return False
        pass

    def deflate(self,q_h2=1, time = 3600):
        '''
        Hydrogen tank deflates
        :param q_h2: the mole flow rate of hydrogen, mol/s
        :param time: lasting time
        :return: How much hydrogen is consumed/mol
        '''
        self.M = max(0,self. M -  q_h2 * time)
        self.p = self.M *self.R * self.T / self.V
        return q_h2*time

    def mass(self):#kg
        return self.M/500

if __name__ =="__main__":
    a = hydrogen_tank(p_init=0, Volume_tank=60)
    print(a.M,a.mass())
    a.blow_up(time=200)
    print(a.p,a.mass())
    a.blow_up(time=200)
    print(a.p,a.mass())
    a.blow_up(time=200)
    print(a.p,a.mass())
    print(a.mass_max)
