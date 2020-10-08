"""
Wind turbine model
Refer to: Economic sizing of a hybrid(PV–WT–FC) renewable energy system (HRES)
for stand-alone usages by an optimization-simulation model: Case study of Iran
"""
import math
import numpy as np
import matplotlib.pyplot as plt

class wind_turbine():
    rho = 1.08 # Air density, kg/m3
    def __init__(self,C_p = 0.42, r = 40, height = 40,capital_cost = 1547, OM_cost = 0.03, V_ci = 4, V_co = 25, V_r = 14):
        """
        Construction of wind turbine
        :param C_p: Power coefficient
        :param r: radius
        :param height:
        :param capital_cost: Euros/kW
        :param OM_cost: Operation and maintanence cost as a percentage of capital cost
        :param V_ci: cut-in speed
        :param V_co: cut-out speed
        :param V_r: rated speed
        """
        self.C_p = C_p # Power coefficient
        self.r = r # radius
        self.height = height
        self.capital_cost = capital_cost # Euros/kW
        self.V_ci = V_ci
        self.V_co = V_co
        self.V_r = V_r
        self.OM_cost = OM_cost*capital_cost

    def wt_ac_output(self,v_wind,alpha = 0.16):
        "v_wind is the velocity of wind near the ground,alpha is the  surface roughness, depends on terrain condition,\
        which varies from 0.128 to 0.160."
        v_height = v_wind * math.pow(self.height / 10, alpha)
        A = 3.14*self.r**2 # m2
        P = 0 # power output
        if v_height <= self.V_ci:
            P =0
        elif v_height >self.V_ci and v_height <= self.V_r:
            P = 0.5 * self.rho * self.C_p * A * v_height ** 3 / 1e6 #MW
        elif v_height >self.V_r and v_height<= self.V_co:
            P = 0.5 * self.rho * self.C_p * A * self.V_r ** 3 / 1e6 #MW
        else:
            P = 0
        return P

    def rated_power(self):
        return self.wt_ac_output(v_wind=self.V_r)

    def get_v_wind(self, power):
        '''
        An auxilary function for potential use
        :param power:
        :return:
        '''
        v1 = 1
        v2 = 16
        v = (v1+v2)/2
        while math.fabs(self.wt_ac_output(v)-power)>1e-4:
            if self.wt_ac_output(v)<power:
                v1 = v
                v = (v1 + v2) / 2
            if self.wt_ac_output(v)>power:
                v2 = v
                v = (v1+v2)/2
        return v

if __name__ == '__main__':
    a = wind_turbine(V_ci=4, r=45,height=55)
    print(a.rated_power())
    print(a.wt_ac_output(v_wind=6))
    ws = [i / 40 for i in range(0, 600)]
    b = []
    for c_i in ws:
        b.append(a.wt_ac_output(v_wind=c_i))
    fig , ax = plt.subplots()
    ax.plot(ws, b)
    ax.set(xlabel = 'wind speed/ ms-1', ylabel = 'power output/Mw')
    ax.grid()
    plt.show()



