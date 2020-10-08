'''
Created on: 20200923

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
import math
R = 8.314
class compressor():
    def __init__(self,eta_c = 0.75):
        self.eta_c = 0.75

    def power(self,P_in = 30, P_out = 200, gamma = 1.4, T_in = 50, mass_flow_rate = 0.01):
        '''
        power consumed by compressor
        :param P_in: inlet pressure
        :param P_out: outlet pressure
        :param gamma: adiabatic efficient
        :param T_in: inlet temperature
        :param mass_flow_rate: g/s
        :return: power, w
        '''
        p = (R*(T_in+273.15))/(2*(gamma-1)*self.eta_c)*(math.pow((P_out/P_in),(gamma-1)/gamma)-1)*mass_flow_rate
        return p

if __name__ == '__main__':
    a = compressor()
    print(a.power(mass_flow_rate=1))