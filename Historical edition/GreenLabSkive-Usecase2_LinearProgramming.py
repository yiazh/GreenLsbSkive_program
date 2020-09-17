'''
Created on June 14, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147 Elevation:30m Slope:44 Azimuth:3
Linear programming method is based on the package "scipy", where problem is formulated through matrix.
Be careful with the variable definition.
'''
from equipment_package import wind_turbine, battery, hydrogen_tank
from equipment_package import pv, electrolyser, gls_network_function, economic
from prediction_wind_solar_price_load import wind_speed_prediction_MLP, solar_irradiance_prediction, \
    ele_price_prediction
from scipy import optimize as op
from pathlib import Path
import os
import math
import scipy.signal as signal  # Used to get extremum
import numpy as np
import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt


total_cycle = 96  # 96*15 minutes,24h
p0 = 101325  # Atmospheric pressure
np.random.seed(1)

# # 20160105 real data,
# previous_day_wind_speed = np.array([10.98,10.81,10.65,10.48,10.43,10.37,10.32,10.31,10.3,10.29,10.24,
#                                     10.2,10.15,9.89,9.64,9.38,9.49,9.61,9.72,9.65,9.58,9.5,9.27,9.04])
# # 20160106 for reference
# real_observed_wind_speed = np.array([8.81,8.71,8.61,8.51,8.81,9.11,9.41,9.37,9.34,9.31,9.14,8.97,8.8,
#                                      8.57,8.33,8.1,8.38,8.67,8.95,9.02,9.08,9.14,9.12,9.09])

# meteorological data, some depend on forecast, others come from direct datasets.
scenario = 'demand_response'

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

elif scenario == 'demand_response':
    predicted_wind_speed = np.array([7.64, 7.38, 7.12, 7.49, 7.86, 7.23, 7.69, 7.16, 7.63, 4.52, 4.42, 4.31, 4.85, 5.4,
                                     8.29, 5.9, 4.94, 4.19, 4.44, 5.7, 5.35, 4.01, 5.66, 5.58])
    predicted_day_ahead_ele_price = ele_price_prediction.Ele_price_prediction(temporaty_time=264)
    predicted_solar_irradiance = np.array(
        [0, 0, 0, 0, 0, 0, 50, 118, 126, 126, 162, 298, 294, 272, 228, 164, 98, 32, 0, 0, 0, 0, 0, 0])

    pass

Saving_path = Path(Path().absolute() / 'Figure' / 'Usecase2' / ('usecase2_' + scenario + '.csv'))

# Read data on 0411
directory_path = Path(Path().absolute().parent)
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
               'Protein': [0.8] * total_cycle,
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

# default schedule of quantfuel
for i in range(0, total_cycle):
    hour = i // 4
    if hour >= 8 and hour <= 18:
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

# Main loop
cycle = 0

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

# optimizing
objective_dict = {'external_grid': [0] * total_cycle,
                  'battery': [0] * total_cycle,
                  'electrolyser': [1] * total_cycle,
                  'protein_deviation': [0] * total_cycle,
                  'soc': [0] * total_cycle,
                  'Mh2': [0] * (total_cycle - 1) + [-1],
                  'quantafuel_h2': [0] * total_cycle,
                  'methanol_h2': [0] * total_cycle,
                  'everfuel_h2': [0] * total_cycle
                  }

c = []
for value in objective_dict.values():
    c += value
c = np.array(c)

# equality constraint
A_eq_gls = np.zeros((3 * total_cycle + 4, objective_dict.__len__() * total_cycle))
B_eq_gls = np.zeros(3 * total_cycle + 4)

# energy conservation, defined from row 0 to row number 'total cycle'
for t in range(0, total_cycle):
    A_eq_gls[t][t] = 1
    A_eq_gls[t][t + total_cycle] = -1  # battery
    A_eq_gls[t][t + 2 * total_cycle] = -1  # electrolyser
    A_eq_gls[t][t + 3 * total_cycle] = -1  # protein_deviation
    B_eq_gls[t] = -power_pv_t[t] - power_wind_t[t]
    for value in load_data_p.values():
        B_eq_gls[t] += value[t]
    pass

# soc change
soc_int = Battery_gls.soc
Q = Battery_gls.capacity * Battery_gls.E_bat / 1e6
for t in range(total_cycle, total_cycle * 2):
    A_eq_gls[t][t] = 24 / Q / total_cycle
    if t == total_cycle:
        A_eq_gls[t][t + 3 * total_cycle] = -1
        B_eq_gls[t] = -soc_int
    else:
        A_eq_gls[t][t - 1 + 3 * total_cycle] = 1
        A_eq_gls[t][t + 3 * total_cycle] = -1
    pass

# Mh2: mass of h2, initial hydrogen is 3000kg
Mh2_ini = 3000
for t in range(total_cycle * 2, total_cycle * 3):
    A_eq_gls[t][
        t] = 24 / total_cycle * 24  # assuming the efficiency is constant (24kg/Mwh)so that we can use linear programming
    if t == 2 * total_cycle:
        A_eq_gls[t][t + 3 * total_cycle] = -1
        A_eq_gls[t][t + 4 * total_cycle] = -1
        A_eq_gls[t][t + 5 * total_cycle] = -1
        A_eq_gls[t][t + 6 * total_cycle] = -1
        B_eq_gls[t] = -Mh2_ini + h2_consumption_all[t - 2 * total_cycle]
    else:
        A_eq_gls[t][t - 1 + 3 * total_cycle] = 1
        A_eq_gls[t][t + 3 * total_cycle] = -1
        A_eq_gls[t][t + 4 * total_cycle] = -1
        A_eq_gls[t][t + 5 * total_cycle] = -1
        A_eq_gls[t][t + 6 * total_cycle] = -1
        B_eq_gls[t] = h2_consumption_all[t - 2 * total_cycle]
    pass

# Overall consumption of protein should be constant
for t in range(3 * total_cycle, 4 * total_cycle):
    A_eq_gls[3 * total_cycle][t] = 1

# Overall consumption of hydrogen constant
for t in range(6 * total_cycle, 7 * total_cycle):
    A_eq_gls[3 * total_cycle + 1][t] = 1

for t in range(7 * total_cycle, 8 * total_cycle):
    A_eq_gls[3 * total_cycle + 2][t] = 1

for t in range(8 * total_cycle, 9 * total_cycle):
    A_eq_gls[3 * total_cycle + 3][t] = 1

# inequality constraints, all the h2 consumption is positive
A_ineq_gls = np.zeros((5 * total_cycle, objective_dict.__len__() * total_cycle))
B_ineq_gls = np.zeros(5 * total_cycle)
for t in range(0, 1 * total_cycle):
    A_ineq_gls[t][t + 6 * total_cycle] = -1
    B_ineq_gls[t] = h2_consumption['Quantfuel'][t]

for t in range(1 * total_cycle, 2 * total_cycle):
    A_ineq_gls[t][t + 6 * total_cycle] = -1
    B_ineq_gls[t] = h2_consumption['Methanol_systhesis'][t - total_cycle]

for t in range(2 * total_cycle, 3 * total_cycle):
    A_ineq_gls[t][t + 6 * total_cycle] = -1
    B_ineq_gls[t] = h2_consumption['EverFuel'][t - 2 * total_cycle]

for t in range(3 * total_cycle, 4 * total_cycle):
    A_ineq_gls[t][t + 5 * total_cycle] = 1
    B_ineq_gls[t] = 62.5 - h2_consumption['EverFuel'][t - 3 * total_cycle]

# hydrogen is only generated by renewable energy
for t in range(4 * total_cycle, 5 * total_cycle):
    A_ineq_gls[t][t - 3 * total_cycle] = 1  # battery
    A_ineq_gls[t][t - 2 * total_cycle] = 1  # electrolyser
    B_ineq_tem = power_pv_t[t - 4 * total_cycle] + power_wind_t[t - 4 * total_cycle]
    for value in load_data_p.values():
        B_ineq_tem -= value[t - 4 * total_cycle]
    pass
    B_ineq_gls[t] = max(0, B_ineq_tem)  # re power - load

bound_dict = {'external_grid': [(None, None)] * total_cycle,
              'battery': [(-1.36, 1.36)] * total_cycle,
              'electrolyser': [(-1e-4, Electrolyser_gls.max_power)] * total_cycle,
              'protein_deviation': [(-0.2, 0.2)] * total_cycle,
              'soc': [(Battery_gls.soc_min, Battery_gls.soc_max)] * total_cycle,
              'Mh2': [(1000, 5000)] * total_cycle,
              'quantafuel_h2': [(-5, 5)] * total_cycle,
              'methanol_h2': [(-5, 5)] * total_cycle,
              'everfuel_h2': [(-62.5, 60)] * total_cycle
              }
bound = []
for value in bound_dict.values():
    bound += value
bound_gls = tuple(bound)

# solve
res = op.linprog(c, A_ub=A_ineq_gls, b_ub=B_ineq_gls, A_eq=A_eq_gls, b_eq=B_eq_gls, bounds=bound_gls)
print(res)
print(res.success)
print("Successfuly solved?",res.success)

res_dict_opt = {'external_grid': res.x[0:total_cycle],
                'battery': res.x[total_cycle:2 * total_cycle],
                'electrolyser': res.x[2 * total_cycle:3 * total_cycle],
                'protein': np.sum([res.x[3 * total_cycle:4 * total_cycle], load_data_p['Protein']], axis=0),
                'soc': res.x[4 * total_cycle:5 * total_cycle],
                'Mh2': res.x[5 * total_cycle:6 * total_cycle],
                'quantafuel_h2': np.sum([res.x[6 * total_cycle:7 * total_cycle], h2_consumption['Quantfuel']], axis=0),
                'methanol_h2': np.sum([res.x[7 * total_cycle:8 * total_cycle], h2_consumption['Methanol_systhesis']],
                                      axis=0),
                'everfuel_h2': np.sum([res.x[8 * total_cycle:9 * total_cycle], h2_consumption['EverFuel']], axis=0)
                }

load_data_p['Protein'] = res_dict_opt['protein'].tolist()
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

    expenditure.append((external_grid_power[cycle_power_flow] * C_grid_t[cycle_power_flow] +
                        power_wind_t[cycle_power_flow] * wind_price + power_pv_t[cycle_power_flow] * pv_price +
                        0) * 24 / total_cycle)
    accumulated_expenditure.append(np.array(expenditure).sum())

    print(cycle_power_flow)

    cycle_power_flow += 1

res_dict = {'P_grid': np.array(external_grid_power),
            'P_wind': np.array(power_wind_t),
            'P_pv': np.array(power_pv_t),
            'P_b': res_dict_opt['battery'],
            'P_ele': res_dict_opt['electrolyser'],
            'P_pro': res_dict_opt['protein'],
            'soc': res_dict_opt['soc'],
            'Mh2': res_dict_opt['Mh2'],
            'price_grid': np.array(C_grid_t),
            'expenditure': np.array(expenditure),
            'accumulated_ex': np.array(accumulated_expenditure),
            'quantafuel_h2': res_dict_opt['quantafuel_h2'],
            'methanol_h2': res_dict_opt['methanol_h2'],
            'everfuel_h2': res_dict_opt['everfuel_h2']
            }

pd_results = pd.DataFrame(res_dict)

try:
    pd_results.to_csv(Saving_path)
except PermissionError:
    print('File already exists')
