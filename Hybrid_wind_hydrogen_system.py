'''
Created on: 20200915

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
from equipment_package import wind_turbine, electrolyser, hydrogen_tank
from prediction_wind_solar_price_load import ele_price_prediction
from mip import Model, xsum, minimize, BINARY, MAXIMIZE
from openpyxl import *
from pathlib import Path
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import GreenLabSkive_Usecase1_MILP_0802


# An interesting fact is if you name this file GreenLabSkive-Usecase1_MILP_0802, it can not be imported. Did you notice
# that a underscore is replaced by hyphen?

Absolute_path = Path().absolute()


# Weibull_min distritbution
def _weibull_min(x, c, loc, scale):
    return c / scale * ((x - loc) / scale) ** (c - 1) * np.exp(-((x - loc) / scale) ** c)


class HWHS():
    time_span = 0.25  # h

    def deterministic_wind_power(self):
        '''
        Give a deterministic wind power so that we can start preliminary optimization. It would be useless in the future.
        :return: MW
        '''
        # Real data for someday in 2016
        wind_speed = np.array([10.98, 10.81, 10.65, 10.48, 10.43, 10.37, 10.32, 10.31, 10.3, 10.29, 10.24,
                               10.2, 10.15, 9.89, 9.64, 9.38, 9.49, 9.61, 9.72, 9.65, 9.58, 9.5, 9.27, 9.04])
        WT_gls = wind_turbine.wind_turbine(r=50, height=55)
        # These are hourly data while our time span is 15 min. Thus we need to make it consistent with
        # other parameters by repeating each element four times
        return np.asarray([[13 * WT_gls.wt_ac_output(i)] * 4 for i in wind_speed]).flatten()

    def deteministic_price(self):
        # Euros/Mwh
        return np.asarray(
            [[i] * 4 for i in ele_price_prediction.Ele_price_prediction()]).flatten()

    def deteministic_power_load(self):
        # MW
        return np.asarray([i + 0.8 for i in GreenLabSkive_Usecase1_MILP_0802.load_data_p_ex])

    def deterministic_hydrogen_load(self):
        # kg/h
        return np.asarray([i * 4 for i in GreenLabSkive_Usecase1_MILP_0802.h2_consumption_all])

    def optimize_operation_HWHS(self, number=96, tank_size=3000, ele_capacity=14, save = True, *args, **kwargs):
        p_w_t = kwargs['wind_power']
        pi_t = kwargs['price']
        p_l_t = kwargs['power_load']
        m_l_h2_t = kwargs['hydrogen_load']

        # marginal cost
        C_m_ele = 20.5 / 2 * 18 * 0.063 * 0.13  # Euros/MWh 1MWh electricity->20.5kg H2 ->
        # 20.5/2 kmol H2 -> 20.5/2 kmol H2O -> 20.5/2*18 kg H2O -> 0.063DKK/kg H2O
        C_m_comp = 3600 / 3.221 * 0.004
        '''
        According to Hydrogen Station Compression, Storage, and Dispensing Technical Status and Costs: Systems Integration, 
        compressor that impoves hydrogen pressure to 350bar gives an additional cost to hydrogen as $0.14/kg, provided the
        electricity cost is 1.6kWh/kg and power price is $0.085/kWh. Thus it can be infered that the addtional cost without
        electricity payment is 0.14-0.085*1.6 = 0.004$/kg

        '''

        # define MILP model
        GLS_milp_model = Model('GLS', sense=MAXIMIZE)

        # add the variables
        power_utility = [GLS_milp_model.add_var(lb=-100, ub=100, var_type='C') for i in range(number)]
        hydrogen_level = [GLS_milp_model.add_var(lb=0, ub=tank_size, var_type='C') for i in range(number)]
        power_ele = [GLS_milp_model.add_var(lb=0, ub=ele_capacity, var_type='C') for i in
                     range(number)]
        power_comp = [GLS_milp_model.add_var(lb=0, ub=100, var_type='C') for i in range(number)]

        # add objective function
        Mh2_ini = 1000  # initial amount of hydrogen stored in the tank
        GLS_milp_model.objective = xsum((power_utility[i] * pi_t[i]
                                         - power_ele[i] * C_m_ele - power_comp[i] * C_m_comp) * self.time_span
                                        for i in range(number)) + (hydrogen_level[-1] - Mh2_ini) * 0

        # --------------------------------------add constrains-------------------------------------
        # energy conservation
        for t in range(number):
            GLS_milp_model += p_w_t[t] - power_utility[t] - p_l_t[t] - power_comp[t] - power_ele[t] == 0
            pass

        # electrolyser ramping rate limit
        RLU = 10
        RLD = 10
        for t in range(number):
            if t == 0:
                GLS_milp_model += power_ele[t] - 0 <= RLU
                GLS_milp_model += power_ele[t] - 0 >= -RLD
            else:
                GLS_milp_model += power_ele[t] - power_ele[t - 1] <= RLU
                GLS_milp_model += power_ele[t] - power_ele[t - 1] >= -RLD

        # relation between compressor power and electrolyser power
        for t in range(number):
            power_comp[t] = power_ele[t] * 20.5 / 3600 * 1e3 * 3221 / 1e6  # MW, unit conversion

        # regrading hydrogen tank

        for t in range(number):
            if t == 0:
                GLS_milp_model += hydrogen_level[t] - Mh2_ini == (power_ele[t] * 20.5 - m_l_h2_t[t]) * self.time_span

            else:
                GLS_milp_model += hydrogen_level[t] - hydrogen_level[t - 1] == (
                            power_ele[t] * 20.5 - m_l_h2_t[t]) * self.time_span

        GLS_milp_model += hydrogen_level[-1] == Mh2_ini

        # optimize
        GLS_milp_model.optimize()
        print(GLS_milp_model.status.name)
        print(GLS_milp_model.objective.x)
        if  save == True:
            res_dict = {'Time': [i * 0.25 for i in range(number)],
                        'Price': pi_t,
                        'Power from utility grid': [round(power_utility[i].x, 2) for i in range(number)],
                        'Electrolyser power': [round(power_ele[i].x, 2) for i in range(number)],
                        'Compressor power': [round(power_comp[i].x, 2) for i in range(number)],
                        'Wind power': p_w_t.round(2),
                        'Hydrogen level': [round(hydrogen_level[i].x) for i in range(number)]
                        }
            print()
            Saving_path = Path(Path().absolute() / 'Figure' / 'HWHS' / ('Temporary_1.xlsx'))

            pd_results = pd.DataFrame(res_dict)

            try:
                pd_results.to_excel(Saving_path, float_format='%.3f', index=False)
            except PermissionError:
                print('File already exists')
        return GLS_milp_model.status.name, GLS_milp_model.objective.x

    def optimize_sizing_HWHS(self):
        nodes = 20
        capacity_ele = [i for i in np.linspace(2, 20, nodes)]
        tank_size = [i for i in np.linspace(1000, 6000, nodes)]
        inner_result = np.zeros((nodes, nodes))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i, ele in enumerate(capacity_ele):
            for j, tank in enumerate(tank_size):
                status,optimized_result = self.optimize_operation_HWHS(tank_size=tank, ele_capacity=ele,
                                                   wind_power=self.deterministic_wind_power(),
                                                   price=self.deteministic_price(),
                                                   power_load=self.deteministic_power_load(),
                                                   hydrogen_load=self.deterministic_hydrogen_load(),
                                                   save=False
                                                   )
                if status!= 'INFEASIBLE':
                    inner_result[(i, j)] = optimized_result
                    ax.scatter(ele, tank, inner_result[(i, j)], c = 'darkorange', marker = '>')
                else:
                    inner_result[(i, j)] = 0
                print(f'Cycle: ele_capacity ={ele}, tank_size = {tank}')
        ax.set_xlabel('Capacity of electrolyser(MW)')
        ax.set_ylabel('Tank size(kg)')
        ax.set_zlabel('Optimal operational profit(€)')
        plt.show()
        return inner_result


class Uncertainity_variable():
    # wind speed
    Saving_path = Absolute_path / "Figure/HWHS" / 'UV.xlsx'

    def wind_speed(self):
        # The meterologicl data is saved in this file. Caution: when I am using Path().absolute() to get the path, the
        # return value differs according to where I provoke this funtion
        data_path = Absolute_path / 'prediction_wind_solar_price_load/Historical_Data/pv_wind_data_2016.csv'
        WS_10_m = pd.read_csv(data_path)['WS10m']

        # Fitting the speed data with weibull distribution
        # For some reason, the argument 'loc' has to be set to a value. If not, the fitting would be very poor.
        # For details, check https://github.com/scipy/scipy/issues/11806
        shape, loc, scale = stats.weibull_min.fit(WS_10_m, loc=7)
        print(shape, loc, scale)

        # -------------------------------------plot statistical results----------------------------
        # Interval number
        num_bins = 100

        # Dipict frequency distribution histgram
        fig, ax = plt.subplots()
        # N is the count in each bin, bins is the lower-limit of the bin
        N, bins, patches = ax.hist(WS_10_m, num_bins)

        # ------------------------------------Fitting curve-----------------------------------------
        fig1, ax1 = plt.subplots()
        x = np.linspace(WS_10_m.min(), WS_10_m.max(), num_bins)
        y1 = [stats.weibull_min.pdf(i, shape, loc, scale) for i in x]
        ax1.plot(x, y1)
        # Self-defined function
        y2 = [_weibull_min(i, shape, loc, scale) for i in x]
        ax1.plot(x, y2, color='red')

        # ------------------------------------Fitting curve and statistical data--------------------
        fig2, ax2 = plt.subplots()
        ax2.hist(WS_10_m, num_bins, density=True, color='tab:blue', alpha=0.5)
        ax2.plot(x, y1, label='Fitted weibull dist')
        ax2.set(xlabel='Wind speed(m/s)', ylabel='Frequency', title='Weibull distribution fitting')
        ax2.legend()
        plt.show()

        # Save data
        wind_speed_data = pd.DataFrame()
        bins = bins.tolist()
        bins.pop(-1)
        wind_speed_data['Speed'] = bins
        wind_speed_data['Frequency'] = [i / WS_10_m.size for i in N]
        wind_speed_data['Speed_2'] = x
        wind_speed_data['Weibull_pdf'] = y1
        try:
            wind_speed_data.to_excel(Uncertainity_variable.Saving_path, sheet_name='ws', float_format='%.3f',
                                     index=False)
        except PermissionError:
            print('File is open')

    def electricity_price(self):
        data_path = Absolute_path / 'prediction_wind_solar_price_load/Historical_Data/elspot-prices_2020_hourly_eur1.csv'
        ele_price = pd.read_csv(data_path)['DK2']
        # -------------------------------------print statistical results----------------------------
        # Interval number
        num_bins = 150

        # Dipict frequency distribution histgram
        fig, ax = plt.subplots()
        # N is the count in each bin, bins is the lower-limit of the bin
        N, bins, patches = ax.hist(ele_price, num_bins)
        a = np.asarray(ele_price)
        for index, value in enumerate(a):
            if np.isfinite(value) == False:
                print(index)

        # -------------------------------------Fitting -----------------------------------------------
        loc, scale = stats.norm.fit(ele_price, loc=10)
        print(f'Parameters of normal distribution is mu = {round(loc, 2)},sigma = {round(scale, 2)}')
        fig1, ax1 = plt.subplots()
        x = np.linspace(ele_price.min(), ele_price.max(), num_bins)
        '''
        Specifically, norm.pdf(x, loc, scale) is identically equivalent to 
        norm.pdf(y) / scale with y = (x - loc) / scale
        '''
        y1 = [stats.norm.pdf(i, loc, scale) for i in x]
        ax1.plot(x, y1, label='Fitted normal dist')
        ax1.hist(ele_price, num_bins, color='tab:orange', alpha=0.5, density=True)
        ax1.set(xlabel='Price/€', ylabel='Frequency')
        ax1.legend()
        fig1.tight_layout()
        plt.show()

    def hydrogen_demand(self):
        pass


if __name__ == '__main__':
    a = HWHS()
    c = a.optimize_operation_HWHS(wind_power=a.deterministic_wind_power(), price=a.deteministic_price(),
                                  power_load=a.deteministic_power_load(), hydrogen_load=a.deterministic_hydrogen_load())
    d = a.optimize_sizing_HWHS()
    print(d)
