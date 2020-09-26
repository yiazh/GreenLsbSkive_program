'''
electrolyser model
Refer to : Low-temperature electrolysis system modelling: A review

'''
import math
import matplotlib.pyplot as plt
from scipy.optimize import minimize

F = 96485  # C/mol
R = 8.314  # J/(mol K)
p_0 = 101325  # pa


def Butler_Bolmer(E_act_k, I, I0=3000, alpha=0.5, z=2, T=300):
    # Equation depicting the current density and activation overpotential
    # \left.I=I_{0, k}\left[\exp \left(\frac{\alpha_{k} \cdot z . F \cdot E_{a c t, k}}{R \cdot T}\right)-\exp
    # \left(-\frac{\left(1-\alpha_{k}\right) \cdot z \cdot F \cdot E_{a c t, k}}{R \cdot T}\right)\right]\right]
    A = alpha * z * F / R / T
    B = -(1 - alpha) * z * F / R / T
    return I - I0 * (math.exp(A * E_act_k) - math.exp(B * E_act_k))


def derivative_Butler_bolmer(E_act_k, I, I0=3000, alpha=0.5, z=2, T=300):
    # \frac{dI}{dE_{act}}
    A = alpha * z * F / R / T
    B = -(1 - alpha) * z * F / R / T
    return -I0 * (A * math.exp(A * E_act_k) - B * math.exp(B * E_act_k))


class electrolyser():
    def __init__(self, T=300, p=p_0, A=0.05, I=5000, I0_an=1e-1, I0_ca=1e-1, thickness=3e-2, alpha_an=0.5,
                 alpha_ca=0.5):
        self.T = T  # K
        self.p = p  # Pa
        self.A = A  # m2
        self.I = I  # A/m2, current density not current!
        self.I0_an = I0_an  # A/m2, exchange current density of anode, highly depends on electrode reaction
        self.I0_ca = I0_ca  # A/m2, cathode
        self.thickness = thickness  # m
        self.alpha_an = alpha_an  # charge transfer coefficient, anode
        self.alpha_ca = alpha_ca  # charge transfer coefficient,cathode

    def H2_production(self, f1=250, f2=0.96):
        # Faraday law
        # kg/s, considering the leak current, eta_faraday is slightly less than one
        # faraday efficiency is also called current efficiency, deviation of which to one is produced by parastic current
        # refer to: Modeling of advanced alkaline electrolyzers: a system computation approach, 2003
        eta_faraday = (self.I / 10) ** 2 / (f1 + (self.I / 10) ** 2) * f2
        n_H2 = eta_faraday * self.I * self.A / (2 * F)
        m_H2 = n_H2 * 2 / 1000
        return m_H2  # kg/s

    def efficiency(self):
        """
        \eta = \frac{H_{2,p}H_{H\!H\!V,H_2}}{E_{cell}I}
        :return:
        """
        return self.H2_production() * 142000 / self.power_input() * 1000  #
        """
        The high heat value of hydrogen is 286kJ/mol, responding to around 142kJ/g, 142000kJ/kg
        Another choice is :
        return 1.473/self.E_cell()# 1.473 is the thermal neural voltage, with which the cell is thermal balanced.
        """

    def E_rev_0(self):
        '''
        Standard reversible potential
        Refer to : Low-temperature electrolysis system modelling: A review
        '''
        E_0_T = 1.5184 - 1.5421e-3 * self.T + 9.523e-5 * self.T * math.log(self.T) + 9.84e-8 * self.T ** 2
        return E_0_T

    def E_rev(self, p_H2O=0.5 * p_0):
        '''
        Reversible potential
        '''
        E_rev = self.E_rev_0() + R * self.T / (2 * F) * math.log((self.p - p_H2O) ** 1.5 / (p_H2O))
        return E_rev

    def E_act_an(self):
        act_op = 0.5  # activation over potential
        # Solved by Newton Method
        while math.fabs(Butler_Bolmer(act_op, self.I, I0=self.I0_an, alpha=self.alpha_an, T=self.T)) >= 1e-5:
            slope = derivative_Butler_bolmer(act_op, self.I, I0=self.I0_an, alpha=self.alpha_an, T=self.T)
            act_op = act_op - Butler_Bolmer(act_op, self.I, I0=self.I0_an, alpha=self.alpha_an, T=self.T) \
                     / derivative_Butler_bolmer(act_op, self.I, I0=self.I0_an, alpha=self.alpha_an, T=self.T)
        return act_op

    def E_act_ca(self):
        act_op = 0.5  # activation over potential
        # Solved by Newton Method
        while math.fabs(Butler_Bolmer(act_op, self.I, I0=self.I0_ca, alpha=self.alpha_ca, T=self.T)) >= 1e-5:
            slope = derivative_Butler_bolmer(act_op, self.I, I0=self.I0_ca, alpha=self.alpha_ca, T=self.T)
            act_op = act_op - Butler_Bolmer(act_op, self.I, I0=self.I0_ca, alpha=self.alpha_ca, T=self.T) \
                     / derivative_Butler_bolmer(act_op, self.I, I0=self.I0_ca, alpha=self.alpha_ca, T=self.T)
        return act_op

    # Some approximate approaches to estimate activation overpotential
    # def E_act(self, T_ref=400, mode='Tafel',
    #           p_H2=101325, p_O2=101325, I_0ref=3454, alpha_k=0.25
    #           ):
    #     '''
    #     Activation over-voltage
    #     :param T:Temperature
    #     :param I:Current density
    #     :return: E_act
    #     '''
    #     E = 1.1e5  # activation energy
    #     # I_0k = I_0ref*math.exp(-E/R*(1/self.T-1/T_ref))*(p_H2/p_0)*(p_O2/p_0)**0.5
    #     I_0k = I_0ref
    #     if self.I <= 1.5 * I_0k:
    #         mode = 'symmetry'
    #     else:
    #         mode = 'Tafel'
    #     if mode == 'Tafel':
    #         # The validity domain of this equation is limited to high current density
    #         E_act = R * self.T / (2 * alpha_k * F) * math.log(self.I / I_0k)
    #         return E_act
    #     elif mode == 'symmetry':
    #         E_act = R * self.T / F * math.asin(self.I / (2 * I_0k))
    #         return E_act
    #         pass
    #     else:
    #         pass

    def E_ohm(self, w=0.4):
        # sigma = 0.005139*lamda - 0.0326*(1268*(1/303-1/self.T)) # conductivity of proton exchange membrane S/cm
        # sigma = 2.96396 -0.02371*self.T-0.12269*w+(5.7e-5)*self.T**2 \
        # 		+0.00173*w**2+(4.7e-4)*w-(3.6e-8)*self.T**3 + (2.7e-6)*w**3 -(8.9e-6)*self.T*w**2+(2.4e-7)*self.T**2*w
        # refer to New multi-physics approach for modelling and design of alkaline electrolyzers, eq 31,
        # but the result is negative, weird

        sigma = 0.279844 * (100 * w) - 0.009241 * self.T - 0.000149 * self.T ** 2 - 0.000905 * (100 * w) * self.T \
                + 0.000114 * self.T ** 2 * math.pow((100 * w), 0.1765) + 0.069664 * self.T / (100 * w) - 28.9815 * (
                        100 * w) / self.T
        # refer to: Temperature and Concentration Dependence of the Specific Conductivity of Concentrated Solutions of Potassium Hydroxide
        # S/cm

        E_ohm = self.I / (sigma * 100) * self.thickness
        return E_ohm

    def E_diff(self, I_lim=12000, beta=0.1):
        '''
        Diffusion overvoltage
        :param I_lim: Limiting current density
        :param beta: empiric coefficient
        :return: Diffusion overvoltage
        '''
        E_diff = R * self.T / (2 * beta * F) * math.log(1 + self.I / I_lim)
        return E_diff

    def E_cell(self):
        E_cell = self.E_rev() + self.E_act_an() + self.E_act_ca() + self.E_ohm() + self.E_diff()
        return E_cell

    def power_input(self):
        '''
        :return: W
        '''
        self.power = self.E_cell() * self.I * self.A  # W
        return self.power

    def set_current_density(self, set_I=5000):
        self.I = set_I

    def temperature(self,
                    H_air=100,  # W/(m2 K)
                    H_water=7000,  # W/(m2 K)
                    time_interval=1  # s
                    ):
        Heat_Capacity = 174  # kJ/celcius
        Area = 0.05
        T_air = 20 + 273.15
        T_water = 50 + 273.15
        heat_generation = (self.E_cell() - 1.473) *self.I*self.A
        Delta_T = (heat_generation + H_air * Area * (T_air - self.T) + H_water * Area * (
                    T_water - self.T)) * time_interval / 1000 / Heat_Capacity
        self.T = self.T + Delta_T


class electrolyser_group():
    def __init__(self, series=100, parallel=200, T=300, p=101325, I_max=10000, I_min=100):
        self.series = series
        self.parallel = parallel
        self.T = T
        self.p = p
        self.single = electrolyser(T=self.T, p=self.p, I=5000)
        self.single.set_current_density(I_max)
        self.max_power = self.series * self.parallel * self.single.power_input() / 1e6
        self.single.set_current_density(I_min)
        self.min_power = self.series * self.parallel * self.single.power_input() / 1e6

    def power(self):
        # MW
        return self.series * self.parallel * self.single.power_input() / 1e6

    def n_H2(self):
        # mol/s
        # currently(0610), there is no startup function. This one can be regarded as a start
        return self.single.H2_production() * self.parallel * self.series

    def voltage(self):
        # V
        return self.single.E_cell() * self.series

    def current(self):
        # A
        return self.parallel * self.single.I * self.single.A


def set_power(ele=electrolyser(), power=1000):
    '''
    Given a power output, calculating the corresponding current density.
    If the power demand is out of range, return False
    :param ele:
    :param power:
    :return:
    '''
    ia = 100
    ib = 10000
    if power < electrolyser(I=ia).power_input() or power > electrolyser(I=ib).power_input():
        print('Out of range of work')
        return False
    ic = (ia + ib) / 2
    for i in range(0, 1000):
        if math.fabs(electrolyser(I=ic).power_input() - power) <= 1e-4:
            ele.set_current_density(ic)
            return ic
            break
        else:
            if electrolyser(I=ic).power_input() < power:
                ia = ic
                ic = (ia + ib) / 2
            else:
                ib = ic
                ic = (ia + ib) / 2
    pass


def set_power_group(ele=electrolyser_group(), power=14.5):
    power_0 = min(max(power, ele.min_power), ele.max_power)
    power_1 = power_0 * 1e6 / (ele.series * ele.parallel)
    set_power(ele.single, power_1)


# An emperical model for alkaline electrolyser.
# class alkaline_ele(electrolyser):
#     def __init__(self, T=300, p=p_0, A=100e-4, I=5000):
#         super().__init__(T, p, A, I)
#
#     def E_cell_empirical(self,
#                          r1=8.05e-5,  # ohm m2
#                          r2=-2.5e-7,  # ohm m2/celcius
#                          s=0.185,  # V
#                          t1=-1.002,  # A-1 m2
#                          t2=8.424,  # A-1 m2 celcius
#                          t3=247.3,  # A-1 m2 celcius **2
#                          ):
#         assert (t1 + t2 / (self.T - 273.15) + t3 / (self.T - 273.15) ** 2) * self.I + 1 > 0
#         U = self.E_rev() + (r1 + r2 * (self.T - 273.15)) * self.I + s * math.log(
#             (t1 + t2 / (self.T - 273.15) + t3 / (self.T - 273.15) ** 2) * self.I + 1)
#         return U
#
#     def eta(self):
#         # Energy efficiency.
#         # Provided that auxiliary heat is supplied, this could be higher than one
#         E_tn = 1.473  # thermal neural voltage
#         return self.E_cell_empirical() / E_tn

if __name__ == '__main__':
    test = 0
    if test == 0:
        fig, ax = plt.subplots()
        for temperature in range(273, 353, 20):
            a = electrolyser(T=temperature, I0_an=1e0, I0_ca=1e0, thickness=10e-4)
            current_density = [i * 50 for i in range(10, 200)]
            voltage = []
            m_h2 = []
            power = []
            eff = []
            for c in current_density:
                a.set_current_density(c)
                voltage.append(a.E_cell())
                m_h2.append(a.H2_production() * 3600)
                power.append(a.power_input())
                eff.append(a.efficiency())
            x = current_density
            y = voltage
            ax.plot(power, m_h2, label=f'T={temperature}')
            print([round(m_h2[i]/power[i]*1e6,2) for i in range(1,20)])
            current_str = 'Current density/(A/m2)'
            ax.set(xlabel='Power/W', ylabel='M_h2/(kg/h)')
            # ax.set_xlim([0,1e4])
            # ax.set_ylim([0,5])
        # ax.set(xlabel = 'Current density', ylabel = 'Voltage')
        ax.legend()
        plt.show()
    elif test == 1:
        a = electrolyser_group()
        print(a.max_power, a.min_power)
        set_power_group(a, 14.5)
        print(a.single.I)
        pass
    elif test == 2:
        a = electrolyser()
        tem = []
        hour = 10
        for t in range(hour * 3600):
            a.temperature(time_interval=1, H_air=50, H_water=1000)
            tem.append(a.T - 273.15)
        fig, ax = plt.subplots()
        time_span = [i / 3600 for i in range(hour * 3600)]
        ax.plot(time_span, tem, color='blue')
        ax.set(xlabel='Time/h', ylabel='Temperature/℃')
        ax.grid() # Make the figure look better
        plt.show()
