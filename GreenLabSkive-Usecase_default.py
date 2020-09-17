'''
Created on June 14, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147 Elevation:30m Slope:44 Azimuth:3

20200701:set this program as default case1. we will have four scenarios depending on the external price
or renewable energy generation.

Edited on July 27, 2020
'''
from equipment_package import wind_turbine, battery, hydrogen_tank
from equipment_package import pv, electrolyser, gls_network_function, economic
import os
import math
import scipy.signal as signal  # Used to get extremum
from scipy import optimize as op
import numpy as np
import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt
from prediction_wind_solar_price_load import wind_speed_prediction_MLP, solar_irradiance_prediction, \
    ele_price_prediction
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
scenario = 'High_re_high_price' # Normal, High_re, High_price,High_re_high_price

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

# fig_pre_solar, ax_pre_solar = plt.subplots()
# ax_pre_solar.plot(range(real_solar_irradiance.__len__()), real_solar_irradiance,
#                   color='orangered', label='real value')
# ax_pre_solar.plot(range(predicted_solar_irradiance.__len__()), predicted_solar_irradiance,
#                   color='navy', label='predicted value')
# ax_pre_solar.legend()
# ax_pre_solar.set_xlabel('Time(hour)')
# ax_pre_solar.set_ylabel('Solar irradiance(W/m2)')
# ax_pre_solar.grid()
# plt.savefig(figure_file /'Usecase1' / 'solar_pred.png', dpi=150)
#
# fig_pre_wind, ax_pre_wind = plt.subplots()
# ax_pre_wind.plot(range(real_observed_wind_speed.__len__()), real_observed_wind_speed,
#                  color='orangered', label='real data')
# ax_pre_wind.plot(range(predicted_wind_speed.__len__()), predicted_wind_speed,
#                  color='navy', label='predicted data')
# ax_pre_wind.legend()
# ax_pre_wind.set_xlabel('Time(hour)')
# ax_pre_wind.set_ylabel('Wind speed(m/s)')
# ax_pre_wind.set_ylim([3,12])
# ax_pre_wind.grid()
# plt.savefig(figure_file /'Usecase1' / 'wind_speed_pred.png', dpi=150)
# plt.show()

# Read data on 0411
directory_path = Path().absolute()
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
               'electrolyser': [0] * total_cycle
               # This is considered as a kind of energy storage in power flow calcultion, however,
               # to maintain the number of loads, it is set to zero.
               }

load_data_q_mvar = [0.2] * 8

h2_consumption = {'Quantfuel_h2': [],
                  # 10-12 hours per day, 2100kg CH3OH per hour, 21kg H2 per hour, this estimation refers to
                  # "Alternative Diesel from Waste Plastics"
                  'Methanol_systhesis_h2': [15] * total_cycle,
                  # the production of methanol is expected to be 30000L/day methanol,
                  # CO2+3H2 = CH3OH + H2O. 90000L H2/day. The pressure of h2 is 35bar, meaning the density is 0.089g/l *35
                  # 0.089 *35 *9e4 = 280350g/day about 11.6 kg/hour
                  'EverFuel_h2': []  # two trailers. 4 hours per trailer and 1000kg /trailer
                  }

# default schedule of quantfuel
for i in range(0, total_cycle):
    hour = i // 4
    if hour >= 0 and hour <= 24:
        load_data_p['Quantfuel'].append(0.98)
        h2_consumption['Quantfuel_h2'].append(5.25)
    else:
        load_data_p['Quantfuel'].append(0)
        h2_consumption['Quantfuel_h2'].append(0)
    if hour >= 8 and hour <= 16:
        load_data_p['EverFuel'].append(0.15)
        h2_consumption['EverFuel_h2'].append(62.5)
    else:
        load_data_p['EverFuel'].append(0)
        h2_consumption['EverFuel_h2'].append(0)

# total active power load
load_data_p_all = []
for i in range(total_cycle):
    sum = 0
    for value in load_data_p.values():
        sum += value[i]
    load_data_p_all.append(sum)

# Regarding hydrogen
h2_consumption_all = []
h2_production_all = [] # In this case, this variable is the same as h2_consumption_all
electrolyser_power = []
Mh2 = [0]*total_cycle
Mh2_ini = 3000
h2_tank_price = 25 / 24
for i in range(0, total_cycle):
    a = 0
    for j in h2_consumption.values():
        a += j[i]
    h2_consumption_all.append(a)
    electrolyser_power.append(min(12,a / 24 * 4+1.08))
    h2_production_all.append(electrolyser_power[i]*0.25*24)
    if i == 0:
        Mh2[i]=Mh2_ini-h2_consumption_all[i]+electrolyser_power[i]*0.25*24
    else:
        Mh2[i]=Mh2[i-1]-h2_consumption_all[i]+electrolyser_power[i]*0.25*24

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

load_data_p_copy = load_data_p
load_data_p_copy['electrolyser']=electrolyser_power

default_schedule = pd.DataFrame(Merge(load_data_p_copy, h2_consumption))
figure_file = Path(Path().absolute() / 'Figure')
try:
    default_schedule.to_excel(figure_file / 'Usecase_default' / 'default_schedule.xlsx', float_format='%.2f')
except PermissionError:
    print('File already exists')

supply_RES = []  # Total energy supplied by RES
power_wind_t = []
power_pv_t = []
external_grid_power = []
C_grid_t = []
h2_cost = 0
green_hydrogen = 0

# only consider the operation and maintenance cost
wind_price = 11.57  # 2e6*0.02/(8640*0.4)
pv_price = 17.36  # 3e6 * 0.02/(8640*0.4)
expenditure = []
accumulated_expenditure = []

# hourly generation of renewable energy
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

    # Here we calculate the total cost of produced hydrogen.
    surplus_power = power_wind_t[cycle] + power_pv_t[cycle] - load_data_p_all[cycle]
    if surplus_power >= 0:
        green_hydrogen += min(surplus_power, electrolyser_power[cycle]) * 0.25 * 24
        h2_cost += min(surplus_power, electrolyser_power[cycle]) * 0.25 * (wind_price + pv_price) / 2 + \
                   max(0, electrolyser_power[cycle] - surplus_power) * 0.25 * C_grid_t[cycle]
    else:
        green_hydrogen += 0
        h2_cost += electrolyser_power[cycle] * 0.25 * C_grid_t[cycle]
    cycle += 1
    pass

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

    gls_network.storage.loc[:, 'p_mw'] = electrolyser_power[cycle_power_flow]

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
                        0) * 24 / total_cycle + (Mh2
                       [cycle_power_flow - 1] - Mh2[cycle_power_flow] ) * h2_tank_price)
    else:
        expenditure.append((external_grid_power[cycle_power_flow] * C_grid_t[cycle_power_flow] +
                        power_wind_t[cycle_power_flow] * wind_price + power_pv_t[cycle_power_flow] * pv_price +
                        0) * 24 / total_cycle + (Mh2_ini - Mh2[cycle_power_flow]) * h2_tank_price)

    accumulated_expenditure.append(np.array(expenditure).sum())

    print(cycle_power_flow)

    cycle_power_flow += 1

res_dict = {'P_grid/MW': np.array(external_grid_power),
            'P_wind/MW': np.array(power_wind_t),
            'P_pv/MW': np.array(power_pv_t),
            'P_b/MW': [0] * total_cycle,
            'P_ele/MW': electrolyser_power,
            'P_pro/MW': load_data_p['Protein'],
            'P_recycle/MW': load_data_p['Recycle'],
            'P_biogas/MW': load_data_p['Biogas'],
            'soc': [0.6] * total_cycle,
            'Mh2': Mh2,
            'price_grid/(euros/MWh)': np.array(C_grid_t),
            'expenditure/(euros/15min)': np.array(expenditure),
            'accumulated_ex/euros': np.array(accumulated_expenditure),
            'h2_consumption_all/(kg/15min)': np.array(h2_consumption_all),
            }

pd_results = pd.DataFrame(res_dict)

Saving_path = Path(Path().absolute() / 'Figure' / 'Usecase_default' / ('usecase_de_' + scenario + '.xlsx'))

try:
    pd_results.to_excel(Saving_path,float_format='%.3f')
except PermissionError:
    print('File already exists')

# Print total cost of H2, amount of green H2 and total consumption of H2, as well as the proportion of green hydrogen
print(f'Total cost of hydrogen:{h2_cost}\n', f'Green hydrogen production:{green_hydrogen}\n',
      f'Total hydrogen production:{np.array(h2_consumption_all).sum()}\n',
      f'Proportion of green hydrogen:{green_hydrogen / np.array(h2_consumption_all).sum()}')

# Write aforementioned information to existing excel
wb = load_workbook(Saving_path)
wb.active['P1'].value = 'Total cost of hydrogen'
wb.active['Q1'].value = h2_cost
wb.active['P2'].value = 'Green hydrogen production'
wb.active['Q2'].value = green_hydrogen
wb.active['P3'].value = 'Total hydrogen production'
wb.active['Q3'].value = np.array(h2_production_all).sum()
wb.active['P4'].value = 'Proportion of green hydrogen'
wb.active['Q4'].value = green_hydrogen / np.array(h2_production_all).sum()
wb.active['P5'].value = 'Total expenditure of the system'
wb.active['Q5'].value = accumulated_expenditure[-1]

wb.save(Saving_path)
