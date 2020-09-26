'''
Created on July 28, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147 Elevation:30m Slope:44 Azimuth:3
'''
import os
import math
import numpy as np
import pandas as pd
import pandapower as pp
import matplotlib.pyplot as plt
from scipy import optimize as op
from equipment_package import wind_turbine, battery, hydrogen_tank
from equipment_package import pv, electrolyser, gls_network_function, economic
from prediction_wind_solar_price_load import wind_speed_prediction_MLP, solar_irradiance_prediction, \
    ele_price_prediction
from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY
from pathlib import Path
from openpyxl import *

total_cycle = 96  # 96*15 minutes,24h
p0 = 101325  # Atmospheric pressure
np.random.seed(1)

# # 20160105 real data,
# previous_day_wind_speed = np.array([10.98,10.81,10.65,10.48,10.43,10.37,10.32,10.31,10.3,10.29,10.24,
#                                     10.2,10.15,9.89,9.64,9.38,9.49,9.61,9.72,9.65,9.58,9.5,9.27,9.04])
# # 20160106 for reference
# real_observed_wind_speed = np.array([8.81,8.71,8.61,8.51,8.81,9.11,9.41,9.37,9.34,9.31,9.14,8.97,8.8,
#                                      8.57,8.33,8.1,8.38,8.67,8.95,9.02,9.08,9.14,9.12,9.09])

# 20160410 real data
previous_day_wind_speed_data = np.array([4.23, 4.53, 4.83, 5.13, 5.31, 5.49, 5.67, 5.66, 5.64, 5.63, 5.54, 5.46,
                                         5.38, 5.6, 5.83, 6.06, 5.84, 5.63, 5.42, 5.13, 4.83, 4.54, 4.37, 4.2])
# 20160411 real data, for reference
real_observed_wind_speed = np.array([4.03, 4.02, 4.01, 4, 3.92, 3.84, 3.77, 3.91, 4.06, 4.21, 4.29, 4.36, 4.44,
                                     4.73, 5.02, 5.31, 5.22, 5.13, 5.03, 4.94, 4.84, 4.74, 4.58, 4.42])

real_solar_irradiance = np.array([0, 0, 0, 0, 0, 23.66, 164.81, 394.79, 624.5, 828.23, 949.64, 1009.38, 1001.66,
                                  923.55, 775.91, 559.14, 333.03, 108.54, 0, 0, 0, 0, 0, 0])

# meteorological data, some depend on forecast, others come from direct datasets.
scenario = 'High_re_high_price'  # Normal, High_re, High_price,High_re_high_price

if scenario == 'Normal':
    predicted_wind_speed = wind_speed_prediction_MLP.prediction_function_wind_mlp(previous_day_wind_speed_data)
    predicted_day_ahead_ele_price = ele_price_prediction.Ele_price_prediction(temporaty_time=264)
    predicted_solar_irradiance = solar_irradiance_prediction.prediction_fun_solar_irradiance()

elif scenario == 'High_re':
    predicted_wind_speed = np.array([10.98, 10.81, 10.65, 10.48, 10.43, 10.37, 10.32, 10.31, 10.3, 10.29, 10.24,
                                     10.2, 10.15, 9.89, 9.64, 9.38, 9.49, 9.61, 9.72, 9.65, 9.58, 9.5, 9.27, 9.04])
    predicted_day_ahead_ele_price = ele_price_prediction.Ele_price_prediction(temporaty_time=264)
    predicted_solar_irradiance = solar_irradiance_prediction.prediction_fun_solar_irradiance()

elif scenario == 'High_price':
    predicted_wind_speed = wind_speed_prediction_MLP.prediction_function_wind_mlp(previous_day_wind_speed_data)
    predicted_day_ahead_ele_price = ele_price_prediction.Ele_price_prediction(temporaty_time=96)
    predicted_solar_irradiance = solar_irradiance_prediction.prediction_fun_solar_irradiance()

elif scenario == 'High_re_high_price':
    predicted_wind_speed = np.array([10.98, 10.81, 10.65, 10.48, 10.43, 10.37, 10.32, 10.31, 10.3, 10.29, 10.24,
                                     10.2, 10.15, 9.89, 9.64, 9.38, 9.49, 9.61, 9.72, 9.65, 9.58, 9.5, 9.27, 9.04])
    predicted_day_ahead_ele_price = ele_price_prediction.Ele_price_prediction(temporaty_time=96)
    predicted_solar_irradiance = solar_irradiance_prediction.prediction_fun_solar_irradiance()
    pass

# Read data on 0411
directory_path = os.path.dirname(__file__)
input_data_path = r'{}/prediction_wind_solar_price_load/Historical_Data'.format(directory_path)

File_data = input_data_path + '/pv_wind_data_0411.csv'

Ambient_Data = pd.read_csv(File_data)
# ---------------------------------------Data preprocessing-----------------------------------------
# Build the wind turbines
WT_gls = [wind_turbine.wind_turbine(r=50, height=55)] * 13

# Build the photovoltaics
PV_gls = [pv.pv()] * 6

# Build the battery
Battery_gls = battery.battery_bank(soc_min=0.1)

# Build the electrolyser
Electrolyser_gls = electrolyser.electrolyser_group()

# Build the hydrogen tank
Hydrogen_tank_gls = hydrogen_tank.hydrogen_tank(Volume_tank=100)  # Given the fact that trailers carry 1000kg H2

# Build the load
# default schedule of all loads
load_data_p = {'Quantfuel': [],  # working time:10 hours per day,
               'Biogas': [2.5] * total_cycle,
               'Protein': [0] * total_cycle,
               'EverFuel': [],  # 8 hours per day, 0.15kW
               'Recycle': [3.25] * total_cycle,
               'Methanol': [0.7] * total_cycle,
               'college': [2] * total_cycle,
               'electrolyser': [0] * total_cycle}

h2_consumption = {'Quantfuel': [],
                  # 10-12 hours per day, 2100kg CH3OH per hour, 21kg H2 per hour, this estimation refers to
                  # "Alternative Diesel from Waste Plastics"
                  'Methanol_systhesis': [15] * total_cycle,
                  # the production of methanol is expected to be 30000L/day methanol,
                  # CO2+3H2 = CH3OH + H2O. 90000L H2/day. The pressure of h2 is 35bar, meaning the density is 0.089g/l *35
                  # 0.089 *35 *9e4 = 280350g/day about 11.6 kg/hour
                  'EverFuel': []  # two trailers. 4 hours per trailer and 1000kg /trailer
                  }

# default schedule of quantfuel and everfuel
for i in range(0, total_cycle):
    hour = i // 4
    if hour >= 0 and hour <= 24:
        load_data_p['Quantfuel'].append(0.98)
        h2_consumption['Quantfuel'].append(5.25)
    else:
        load_data_p['Quantfuel'].append(0)
        h2_consumption['Quantfuel'].append(0)
    if hour >= 8 and hour <= 16:
        load_data_p['EverFuel'].append(0.15)
        h2_consumption['EverFuel'].append(62.5)
    else:
        load_data_p['EverFuel'].append(0)
        h2_consumption['EverFuel'].append(0)

h2_consumption_all = []
for i in range(0, total_cycle):
    a = 0
    for j in h2_consumption.values():
        a += j[i]
    h2_consumption_all.append(a)
h2_cost = 0
green_hydrogen = 0
h2_production_all = []
h2_tank_price = 25 / 24

# total active power load with exception of protein plant
load_data_p_ex = []
for i in range(total_cycle):
    sum = 0
    for value in load_data_p.values():
        sum += value[i]
    load_data_p_ex.append(sum)

load_data_q_mvar = [0.2] * 8

supply_RES = []  # Total energy supplied by RES
power_wind_t = []
power_pv_t = []

external_grid_power = []
C_grid_t = []

# only consider the operation and maintenance cost
wind_price = 11.57  # 2e6*0.02/(8640*0.4)
pv_price = 17.36  # 3e6 * 0.02/(8640*0.4)
expenditure = []
accumulated_expenditure = []

if __name__ == '__main__':
    # Main loop
    cycle = 0
    # power of wind turbine and pv
    while cycle < total_cycle:
        # Corresponding time, hour
        hour = cycle // 4
        # ----------------------------Parameters-------------------------------------------------------
        # Wind speed at 10m
        v_wind = predicted_wind_speed[hour]

        # Solar irradiance and surrounding temperature
        irradiance = predicted_solar_irradiance[hour]
        T_sur = Ambient_Data['T2m'][hour]

        wind_generation = []
        pv_generation = []

        for i in WT_gls:
            wind_generation.append(i.wt_ac_output(v_wind))
        for i in PV_gls:
            pv_generation.append(i.pv_ac_output(irradiance, T_sur))

        supply_RES.append(wind_generation + pv_generation)

        power_wind_t.append(np.array(wind_generation).sum())
        power_pv_t.append(np.array(pv_generation).sum())

        C_grid_t.append(predicted_day_ahead_ele_price[hour])
        cycle += 1
        pass

    opt_time1 = 0
    opt_time2 = 4
    opt_objective = 1000

    Mh2_ini = 3000 # Initial amount of hydrogen stored in the tank
    Trailer_per_15min = 62.5

    for time_trailer1 in range(17):
        # This variable represents the time when trailer1 starts to charge.
        # The charging process will last four hours continuously.
        for time_trailer2 in range(time_trailer1 + 4, 21):
            # Time for trailer 2
            # define MILP model
            GLS_milp_model = Model('GLS', sense=minimize)

            # add the variables
            power_ex_grid = [GLS_milp_model.add_var(lb=-100, ub=100, var_type='C') for i in range(total_cycle)]
            power_battery = [GLS_milp_model.add_var(lb=-1.36, ub=1.36, var_type='C') for i in range(total_cycle)]
            power_ele = [GLS_milp_model.add_var(lb=0, ub=12.0, var_type='C') for i in range(total_cycle)]
            power_protein = [GLS_milp_model.add_var(lb=0.6, ub=1.0, var_type='C') for i in range(total_cycle)]
            soc = [GLS_milp_model.add_var(lb=Battery_gls.soc_min, ub=Battery_gls.soc_max, var_type='C') for i in
                   range(total_cycle)]
            Mh2 = [GLS_milp_model.add_var(lb=0, var_type='C') for i in range(total_cycle)]
            quantfuel_h2 = [GLS_milp_model.add_var(lb=0, var_type='C') for i in range(total_cycle)]
            methanol_h2 = [GLS_milp_model.add_var(lb=0, var_type='C') for i in range(total_cycle)]

            # # Integer variable
            # everfuel_h2_trailer1 = [GLS_milp_model.add_var(var_type='B') for i in range(total_cycle)]
            # everfuel_h2_trailer2 = [GLS_milp_model.add_var(var_type='B') for i in range(total_cycle)]

            # Add objective function
            GLS_milp_model.objective = xsum(power_ex_grid[i] * 0.25 * C_grid_t[i] for i in range(total_cycle)) \
                                       + (Mh2_ini - Mh2[-1]) * h2_tank_price

            # Equality constrain: conservation of energy
            for t in range(total_cycle):
                Total_load_t = 0
                for value in load_data_p.values():
                    Total_load_t += value[t]
                GLS_milp_model += power_pv_t[t] + power_wind_t[t] + power_ex_grid[t] - \
                                  power_ele[t] - power_battery[t] - power_protein[t] - \
                                  Total_load_t == 0

            # Constrain regarding battery soc
            soc_int = 0.6
            Q = Battery_gls.capacity * Battery_gls.E_bat / 1e6
            for t in range(total_cycle):
                if t == 0:
                    GLS_milp_model += soc[t] - soc_int - power_battery[t] * 15 / 60 / Q == 0
                else:
                    GLS_milp_model += soc[t] - soc[t - 1] - power_battery[t] * 15 / 60 / Q == 0

            # The total consumption after re-schedule should be the same
            # Protein plant
            GLS_milp_model += xsum(power_protein[i] for i in range(total_cycle)) - \
                              0.8 * total_cycle == 0
            # Quantfuel plant
            GLS_milp_model += xsum(quantfuel_h2[i] for i in range(total_cycle)) - \
                              xsum(h2_consumption['Quantfuel'][i] for i in range(total_cycle)) == 0
            # Methanol synthesis
            GLS_milp_model += xsum(methanol_h2[i] for i in range(total_cycle)) - \
                              xsum(h2_consumption['Methanol_systhesis'][i] for i in range(total_cycle)) == 0
            # # Trailers
            # GLS_milp_model += xsum(everfuel_h2_trailer1[i] * 62.5 for i in range(total_cycle)) - \
            #                   xsum(h2_consumption['EverFuel'][i] for i in range(total_cycle))/2 == 0
            # GLS_milp_model += xsum(everfuel_h2_trailer2[i] * 62.5 for i in range(total_cycle)) - \
            #                   xsum(h2_consumption['EverFuel'][i] for i in range(total_cycle))/2 == 0

            # Consumption should be in a reasonable range
            for t in range(total_cycle):
                GLS_milp_model += quantfuel_h2[t] >= h2_consumption['Quantfuel'][t] * 0.8
                GLS_milp_model += quantfuel_h2[t] <= h2_consumption['Quantfuel'][t] * 1.2

                GLS_milp_model += methanol_h2[t] >= h2_consumption['Methanol_systhesis'][t] * 0.8
                GLS_milp_model += methanol_h2[t] <= h2_consumption['Methanol_systhesis'][t] * 1.2

            # Transient change of electrolyser is subject to limited range
            for t in range(total_cycle):
                if t == 0:
                    GLS_milp_model += power_ele[t]-0 <= 3
                else:
                    GLS_milp_model += power_ele[t] - power_ele[t-1] <= 3

            # Constrain regarding hydrogen tank
            for t in range(total_cycle):
                if t >= time_trailer1 * 4 and t < (time_trailer1 + 4) * 4:
                    if t == 0:
                        GLS_milp_model += Mh2[t] - Mh2_ini + quantfuel_h2[t] + Trailer_per_15min \
                                          + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
                    else:
                        GLS_milp_model += Mh2[t] - Mh2[t - 1] + quantfuel_h2[t] + Trailer_per_15min \
                                          + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
                elif t >= time_trailer2 * 4 and t < (time_trailer2 + 4) * 4:
                    if t == 0:
                        GLS_milp_model += Mh2[t] - Mh2_ini + quantfuel_h2[t] + Trailer_per_15min \
                                          + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
                    else:
                        GLS_milp_model += Mh2[t] - Mh2[t - 1] + quantfuel_h2[t] + Trailer_per_15min \
                                          + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
                else:
                    if t == 0:
                        GLS_milp_model += Mh2[t] - Mh2_ini + quantfuel_h2[t] \
                                          + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
                    else:
                        GLS_milp_model += Mh2[t] - Mh2[t - 1] + quantfuel_h2[t] \
                                          + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
            # Optimize
            GLS_milp_model.optimize()
            print(GLS_milp_model.status.name)
            print(GLS_milp_model.objective.x)
            if time_trailer1 == 0 and time_trailer2 == 4:
                opt_objective = GLS_milp_model.objective.x
            if GLS_milp_model.objective.x < opt_objective:
                opt_time1 = time_trailer1
                opt_time2 = time_trailer2
                opt_objective = GLS_milp_model.objective.x
            print(time_trailer1, time_trailer2)

    print(opt_time1, opt_time2, opt_objective)

    GLS_milp_model = Model('GLS', sense=minimize)

    # add the variables
    power_ex_grid = [GLS_milp_model.add_var(lb=-100, ub=100, var_type='C') for i in range(total_cycle)]
    power_battery = [GLS_milp_model.add_var(lb=-1.36, ub=1.36, var_type='C') for i in range(total_cycle)]
    power_ele = [GLS_milp_model.add_var(lb=0, ub=12.0, var_type='C') for i in range(total_cycle)]
    power_protein = [GLS_milp_model.add_var(lb=0.6, ub=1.0, var_type='C') for i in range(total_cycle)]
    soc = [GLS_milp_model.add_var(lb=Battery_gls.soc_min, ub=Battery_gls.soc_max, var_type='C') for i in
           range(total_cycle)]
    Mh2 = [GLS_milp_model.add_var(lb=0, var_type='C') for i in range(total_cycle)]
    quantfuel_h2 = [GLS_milp_model.add_var(lb=0, var_type='C') for i in range(total_cycle)]
    methanol_h2 = [GLS_milp_model.add_var(lb=0, var_type='C') for i in range(total_cycle)]

    # # Integer variable
    # everfuel_h2_trailer1 = [GLS_milp_model.add_var(var_type='B') for i in range(total_cycle)]
    # everfuel_h2_trailer2 = [GLS_milp_model.add_var(var_type='B') for i in range(total_cycle)]

    # Add objective function
    GLS_milp_model.objective = xsum(power_ex_grid[i] * 0.25 * C_grid_t[i] for i in range(total_cycle)) \
                               + (Mh2[0] - Mh2[-1]) * h2_tank_price

    # Equality constrain: conservation of energy
    for t in range(total_cycle):
        Total_load_t = 0
        for value in load_data_p.values():
            Total_load_t += value[t]
        GLS_milp_model += power_pv_t[t] + power_wind_t[t] + power_ex_grid[t] - \
                          power_ele[t] - power_battery[t] - power_protein[t] - \
                          Total_load_t == 0

    # Constrain regarding battery soc
    soc_int = 0.6
    # Q = Battery_gls.capacity * Battery_gls.E_bat / 1e6
    Q = 1.6
    for t in range(total_cycle):
        if t == 0:
            GLS_milp_model += soc[t] - soc_int - power_battery[t] * 15 / 60 / Q == 0
        else:
            GLS_milp_model += soc[t] - soc[t - 1] - power_battery[t] * 15 / 60 / Q == 0

    # The total consumption after re-schedule should be the same
    # Protein plant
    GLS_milp_model += xsum(power_protein[i] for i in range(total_cycle)) - \
                      0.8 * total_cycle == 0
    # Quantfuel plant
    GLS_milp_model += xsum(quantfuel_h2[i] for i in range(total_cycle)) - \
                      xsum(h2_consumption['Quantfuel'][i] for i in range(total_cycle)) == 0
    # Methanol synthesis
    GLS_milp_model += xsum(methanol_h2[i] for i in range(total_cycle)) - \
                      xsum(h2_consumption['Methanol_systhesis'][i] for i in range(total_cycle)) == 0
    # # Trailers
    # GLS_milp_model += xsum(everfuel_h2_trailer1[i] * 62.5 for i in range(total_cycle)) - \
    #                   xsum(h2_consumption['EverFuel'][i] for i in range(total_cycle))/2 == 0
    # GLS_milp_model += xsum(everfuel_h2_trailer2[i] * 62.5 for i in range(total_cycle)) - \
    #                   xsum(h2_consumption['EverFuel'][i] for i in range(total_cycle))/2 == 0

    # Consumption should be in a reasonable range
    for t in range(total_cycle):
        GLS_milp_model += quantfuel_h2[t] >= h2_consumption['Quantfuel'][t] * 0.8
        GLS_milp_model += quantfuel_h2[t] <= h2_consumption['Quantfuel'][t] * 1.2

        GLS_milp_model += methanol_h2[t] >= h2_consumption['Methanol_systhesis'][t] * 0.8
        GLS_milp_model += methanol_h2[t] <= h2_consumption['Methanol_systhesis'][t] * 1.2

    # Transient change of electrolyser is subject to limited range
    for t in range(total_cycle):
        if t == 0:
            GLS_milp_model += power_ele[t] - 0 <= 3
        else:
            GLS_milp_model += power_ele[t] - power_ele[t - 1] <= 3

    # Constrain regarding hydrogen tank
    Mh2_ini = 3000
    Trailer_per_15min = 62.5

    for t in range(total_cycle):
        if t >= opt_time1 * 4 and t < (opt_time1 + 4) * 4:
            if t == 0:
                GLS_milp_model += Mh2[t] - Mh2_ini + quantfuel_h2[t] + Trailer_per_15min \
                                  + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
            else:
                GLS_milp_model += Mh2[t] - Mh2[t - 1] + quantfuel_h2[t] + Trailer_per_15min \
                                  + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
        elif t >= opt_time2 * 4 and t < (opt_time2 + 4) * 4:
            if t == 0:
                GLS_milp_model += Mh2[t] - Mh2_ini + quantfuel_h2[t] + Trailer_per_15min \
                                  + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
            else:
                GLS_milp_model += Mh2[t] - Mh2[t - 1] + quantfuel_h2[t] + Trailer_per_15min \
                                  + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
        else:
            if t == 0:
                GLS_milp_model += Mh2[t] - Mh2_ini + quantfuel_h2[t] \
                                  + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
            else:
                GLS_milp_model += Mh2[t] - Mh2[t - 1] + quantfuel_h2[t] \
                                  + methanol_h2[t] - power_ele[t] * 0.25 * 24 == 0
    # Optimize
    GLS_milp_model.optimize()
    print(GLS_milp_model.status.name)
    print(GLS_milp_model.objective.x)

    everfuel_h2 = []
    for t in range(total_cycle):
        if (t >= opt_time1 * 4 and t < (opt_time1 + 4) * 4) or (t >= opt_time2 * 4 and t < (opt_time2 + 4) * 4):
            everfuel_h2.append(62.5)
        else:
            everfuel_h2.append(0)

    res_dict_opt = {'external_grid': [power_ex_grid[i].x for i in range(total_cycle)],
                    'battery': [power_battery[i].x for i in range(total_cycle)],
                    'electrolyser': [power_ele[i].x for i in range(total_cycle)],
                    'protein': [power_protein[i].x for i in range(total_cycle)],
                    'soc': [soc[i].x for i in range(total_cycle)],
                    'Mh2': [Mh2[i].x for i in range(total_cycle)],
                    'quantafuel_h2': [quantfuel_h2[i].x for i in range(total_cycle)],
                    'methanol_h2': [methanol_h2[i].x for i in range(total_cycle)],
                    'everfuel_h2': everfuel_h2
                    }


    load_data_p['Protein'] = res_dict_opt['protein']

    # Calculate the hydrogen data under optimized schedule
    # total active power load
    load_data_p_all = []
    for i in range(total_cycle):
        sum = 0
        for value in load_data_p.values():
            sum += value[i]
        load_data_p_all.append(sum)

    #--------------------------------------HYDROGEN ECONOMIES------------------------------------
    cycle_h2 = 0
    while cycle_h2 < total_cycle:

        # H2 production is proportional to power of electrolyser
        h2_production_all.append(res_dict_opt['electrolyser'][cycle_h2] * 0.25 * 24)
        surplus_power = power_wind_t[cycle_h2] + power_pv_t[cycle_h2] - load_data_p_all[cycle_h2]

        # If there is surplus renewable energy, green hydrogen can be generated.
        # Provided that the surplus energy is not enough for electrolyser schedule, external power will be used.
        if surplus_power >= 0:
            green_hydrogen += min(surplus_power, res_dict_opt['electrolyser'][cycle_h2]) * 0.25 * 24
            h2_cost += min(surplus_power, res_dict_opt['electrolyser'][cycle_h2]) * 0.25 * (wind_price + pv_price) / 2 + \
                       max(0, res_dict_opt['electrolyser'][cycle_h2] - surplus_power) * 0.25 * C_grid_t[cycle_h2]
        else:
            # No surplus leads to no green hydrogen
            green_hydrogen += 0
            h2_cost += res_dict_opt['electrolyser'][cycle_h2] * 0.25 * C_grid_t[cycle_h2]
        cycle_h2 += 1

    #--------------------------------------------POWER FLOW CALCULATION------------------------
    cycle_power_flow = 0

    while cycle_power_flow < total_cycle:
        hour = cycle_power_flow // 4

        # %% Run network builder function

        gls_network, gls_network_results_original = gls_network_function.gls_network_builder()

        # %% Change power consumption from loads
        gls_network.load.loc[:, 'name']  # order in which to supply load data

        # electrolyser as a load
        load = []
        for i in load_data_p.values():
            load.append(i[cycle_power_flow])

        gls_network.load.loc[:, 'p_mw'] = load
        gls_network.load.loc[:, 'q_mvar'] = load_data_q_mvar

        # %% Change storage
        gls_network.storage

        gls_network.storage.loc[:, 'p_mw'] = res_dict_opt['battery'][cycle_power_flow] \
                                             + res_dict_opt['electrolyser'][cycle_power_flow]

        # %% Change power of generators
        gls_network.sgen.loc[:, 'name']  # order in which to supply generator data

        generator_data_q_mvar = [0] * 19

        gls_network.sgen.loc[:, 'p_mw'] = supply_RES[cycle_power_flow]
        gls_network.sgen.loc[:, 'q_mvar'] = generator_data_q_mvar

        # %% Run pandapower power flow with new set of data
        pp.runpp(gls_network, trafo_loading='power', algorithm='nr', calculate_voltage_angles='auto')

        # %% Write results in the dictionary
        # Add names of the rows
        gls_network.res_bus.insert(0, 'name', pd.Series(gls_network.bus.loc[:, 'name']), allow_duplicates=False)
        gls_network.res_trafo.insert(0, 'name', pd.Series(gls_network.trafo.loc[:, 'name']), allow_duplicates=False)
        gls_network.res_line.insert(0, 'name', pd.Series(gls_network.line.loc[:, 'name']), allow_duplicates=False)
        gls_network.res_load.insert(0, 'name', pd.Series(gls_network.load.loc[:, 'name']), allow_duplicates=False)
        gls_network.res_storage.insert(0, 'name', pd.Series(gls_network.storage.loc[:, 'name']), allow_duplicates=False)
        gls_network.res_sgen.insert(0, 'name', pd.Series(gls_network.sgen.loc[:, 'name']), allow_duplicates=False)

        # Write all results in the dictionary
        gls_network_results = {}
        gls_network_results['Bus'] = gls_network.res_bus
        gls_network_results['External_grid'] = gls_network.res_ext_grid
        gls_network_results['Transformer'] = gls_network.res_trafo
        gls_network_results['Cable'] = gls_network.res_line
        gls_network_results['Load'] = gls_network.res_load
        gls_network_results['Storage'] = gls_network.res_storage
        gls_network_results['Generator'] = gls_network.res_sgen

        external_grid_power.append(gls_network_results['External_grid']['p_mw'][0])

        if cycle_power_flow !=0:
            expenditure.append((external_grid_power[cycle_power_flow] * C_grid_t[cycle_power_flow] +
                            power_wind_t[cycle_power_flow] * wind_price + power_pv_t[cycle_power_flow] * pv_price +
                            0) * 24 / total_cycle + (res_dict_opt['Mh2']
                           [cycle_power_flow - 1] - res_dict_opt['Mh2'][cycle_power_flow] ) * h2_tank_price)
        else:
            expenditure.append((external_grid_power[cycle_power_flow] * C_grid_t[cycle_power_flow] +
                            power_wind_t[cycle_power_flow] * wind_price + power_pv_t[cycle_power_flow] * pv_price +
                            0) * 24 / total_cycle + (Mh2_ini - res_dict_opt['Mh2'][cycle_power_flow]) * h2_tank_price)
        accumulated_expenditure.append(np.array(expenditure).sum())
        print(cycle_power_flow)
        cycle_power_flow += 1

    res_dict = {'P_grid/MW': np.array(external_grid_power),
                'P_wind/MW': np.array(power_wind_t),
                'P_pv/MW': np.array(power_pv_t),
                'P_b/MW': res_dict_opt['battery'],
                'P_ele/MW': res_dict_opt['electrolyser'],
                'P_pro/MW': res_dict_opt['protein'],
                'P_recycle/MW': load_data_p['Recycle'],
                'P_biogas/MW': load_data_p['Biogas'],
                'soc': res_dict_opt['soc'],
                'Mh2/kg': res_dict_opt['Mh2'],
                'price_grid/(euros/MWh)': np.array(C_grid_t),
                'expenditure/euros': np.array(expenditure),
                'accumulated_ex/euros': np.array(accumulated_expenditure),
                'quantafuel_h2/(kg/15min)': res_dict_opt['quantafuel_h2'],
                'methanol_h2/(kg/15min)': res_dict_opt['methanol_h2'],
                'everfuel_h2/(kg/15min)': res_dict_opt['everfuel_h2']
                }

    Saving_path = Path(Path().absolute() / 'Figure' / 'Usecase_MILP' / ('Usecase1_MILP_' + scenario + '.xlsx'))

    pd_results = pd.DataFrame(res_dict)

    try:
        pd_results.to_excel(Saving_path, float_format='%.3f')
    except PermissionError:
        print('File already exists')

    wb = load_workbook(Saving_path)
    wb.active['R1'].value = 'Total cost of hydrogen(euros)'
    wb.active['S1'].value = h2_cost
    wb.active['R2'].value = 'Green hydrogen production(kg)'
    wb.active['S2'].value = green_hydrogen
    wb.active['R3'].value = 'Total hydrogen production(kg)'
    wb.active['S3'].value = np.array(h2_production_all).sum()
    wb.active['R4'].value = 'Proportion of green hydrogen'
    wb.active['S4'].value = green_hydrogen / np.array(h2_production_all).sum()
    wb.active['R5'].value = 'Total expenditure of the system(euros)'
    wb.active['S5'].value = accumulated_expenditure[-1]
    wb.active['R6'].value = 'Average cost of hydrogen(euros/kg)'
    wb.active['S6'].value = h2_cost / np.array(h2_production_all).sum()

    wb.save(Saving_path)
