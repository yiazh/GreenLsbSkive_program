'''
pv model
Refer to: Economic sizing of a hybrid(PV–WT–FC) renewable energy system (HRES)
for stand-alone usages by an optimization-simulation model: Case study of Iran
'''
import matplotlib.pyplot as plt


class pv():
    def __init__(self, A=60000, eta_r=0.15, beta=0.0045, NOCT=55, T_r=25, I_NOCT=800, eta_pc=0.7):
        self.A = A  # Area m2
        self.eta_r = eta_r  # Rated module efficiency
        self.beta = beta  # Temperature coefficient of efficiency
        self.NOCT = NOCT  # Normal operation cell temperature,celcius
        self.T_r = T_r  # Temperature in rated efficiency
        self.I_NOCT = I_NOCT  # Solar radiation in NOCT,W/m2
        self.eta_pc = eta_pc  # Efficiency of the auxiliary equipment

    def pv_dc_output(self, I_T, T_a):
        T_c = T_a + (self.NOCT - T_a) / self.I_NOCT * I_T
        eta_ec = self.eta_r * (1 - self.beta * (T_c - self.T_r))
        eta = eta_ec * self.eta_pc
        output_pv = I_T * eta * self.A / 1000 / 1000  # MW
        return output_pv

    def pv_ac_output(self, I_T, T_a):
        c = Inverter(p_nom=4.6)
        return c.p_ac(self.pv_dc_output(I_T, T_a))


'''
A simple mathematical model for estimating efficiency of inverters
Reference: Mathematical models for efficiency of inverters used in grid connected
photovoltaic systems(Eq 7)
'''


class Inverter(object):

    def __init__(self, p_nom):
        self.p_nom = p_nom

    def eta_con(self, p_ac, k_0=0.0185, k_1=0.0393, k_2=0.0562):
        eta = (p_ac / self.p_nom) / \
              ((p_ac / self.p_nom) + (k_0 + k_1 * (p_ac / self.p_nom) + k_2 * (p_ac / self.p_nom) ** 2))

        return eta

    def p_ac(self, p_dc, k_0=0.0185, k_1=0.0393, k_2=0.0562):
        import scipy.optimize
        def solve_p_ac(pac):
            return pac - p_dc * self.eta_con(pac, k_0, k_1, k_2)

        return scipy.optimize.fsolve(solve_p_ac, p_dc)[0]



if __name__ == '__main__':
    a = pv()
    fig, ax = plt.subplots()
    Irradiation = [i * 100 for i in range(10)]
    for t in range(10, 40, 10):
        PV_ac = [a.pv_ac_output(I_T=i, T_a=t) for i in Irradiation]
        ax.plot(Irradiation, PV_ac)
    b = Inverter(100)
# This model is mediocre
