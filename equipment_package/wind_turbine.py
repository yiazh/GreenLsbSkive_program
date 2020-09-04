"""
Wind turbine model
Refer to: Economic sizing of a hybrid(PV–WT–FC) renewable energy system (HRES)
for stand-alone usages by an optimization-simulation model: Case study of Iran
"""
import math
import numpy as np
class wind_turbine():
    rho = 1.08 # Air density, kg/m3
    def __init__(self,C_p = 0.42, r = 50, height = 55,capital_cost = 2000):
        self.C_p = C_p # Power coefficient
        self.r = r # radius
        self.height = height
        self.capital_cost = capital_cost # $/kW

    def wt_ac_output(self,v_wind,alpha = 0.16):
        "v_wind is the velocity of wind near the ground,alpha is the  surface roughness, depends on terrain condition,\
        which varies from 0.128 to 0.160."
        v_height = v_wind * math.pow(self.height / 10, alpha)
        A = 3.14*self.r**2 # m2
        return 0.5 * self.rho * self.C_p * A * v_height ** 3 / 1e6 #MW

    def get_v_wind(self, power):
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
    a = wind_turbine()
    print(a.wt_ac_output(10))
    c = [1.799562248,1.799562248,1.799562248,1.799562248,1.622018799,1.622018799,1.622018799,1.622018799,1.456554633,1.456554633,1.456554633,1.456554633,1.695634526,1.695634526,1.695634526,1.695634526,1.959541367,1.959541367,1.959541367,1.959541367,1.52511183,1.52511183,1.52511183,1.52511183,1.8351257,1.8351257,1.8351257,1.8351257,1.481241478,1.481241478,1.481241478,1.481241478,1.792505149,1.792505149,1.792505149,1.792505149,0.372650838,0.372650838,0.372650838,0.372650838,0.348460541,0.348460541,0.348460541,0.348460541,0.323086349,0.323086349,0.323086349,0.323086349,0.460375299,0.460375299,0.460375299,0.460375299,0.63543053,0.63543053,0.63543053,0.63543053,2.299060445,2.299060445,2.299060445,2.299060445,0.828786814,0.828786814,0.828786814,0.828786814,0.486482973,0.486482973,0.486482973,0.486482973,0.296844404,0.296844404,0.296844404,0.296844404,0.35321221,0.35321221,0.35321221,0.35321221,0.747328191,0.747328191,0.747328191,0.747328191,0.617942612,0.617942612,0.617942612,0.617942612,0.260207563,0.260207563,
         0.260207563,0.260207563,0.731705116,0.731705116,0.731705116,0.731705116,0.70111522,0.70111522,0.70111522,0.70111522]
    b = []
    i= 0
    for c_i in c:
        if i %4 == 0:
            b.append(a.get_v_wind(c_i))
        i+=1
    print(b)
    d = np.array(b)
    d = np.around(d,2)
    print(d)


