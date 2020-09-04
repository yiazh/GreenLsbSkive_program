'''
Created on June 14, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147 Elevation:30m Slope:44 Azimuth:3
'''
from equipment_package import wind_turbine, battery, hydrogen
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
# predicted data
predicted_wind_speed = wind_speed_prediction_MLP.prediction_function_wind_mlp(previous_day_wind_speed_data)
predicted_day_ahead_ele_price = ele_price_prediction.Ele_price_prediction(temporaty_time=432)
predicted_solar_irradiance = solar_irradiance_prediction.prediction_fun_solar_irradiance()

figure_file = Path(Path().absolute() / 'Figure')

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
Hydrogen_tank_gls = hydrogen.hydrogen_tank(Volume_tank=100)  # Given the fact that trailers carry 1000kg H2

# Build the load
load_data_p_mw = [0.98,  # Quantfuel, 2020), start up tests currently. It also consumes H2,CH4 and plastic waster
                  2.5,  # Biogas
                  0,  # Danish Marine Protein, used as demand response
                  0.15,  # Ever Fuel, fillinig typical four hours. 200bar to 400bar, 900+kg Hydrogen
                  3.25,  # Recycle facility
                  0.7,  # Methanol facility
                  2,  # GreenSkive college
                  0,  # Electrolyser
                  ]  # The first one stands for protein plant, which should be used as DR
load_data_q_mvar = [0.2] * 8

supply_RES = []  # Total energy supplied by RES
power_wind_t = []
power_pv_t = []

external_grid_power = []


C_grid_t = []
# only consider the operation and maintenance cost
wind_price = 2e6*0.02/(8640*0.4)
pv_price = 3e6 * 0.02/(8640*0.4)
expenditure = []
accumulated_expenditure = []

# Main loop
cycle = 0

for i in range(0,total_cycle):
    hydrogen_consumption_initial_schedule.append(np.random.randint(10)*3)
total_h2_consumption = np.array(hydrogen_consumption_initial_schedule).sum()


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

    supply_RES.append(wind_generation+pv_generation)

    power_wind_t.append(np.array(wind_generation).sum())
    power_pv_t.append(np.array(pv_generation).sum())

    C_grid_t.append(predicted_day_ahead_ele_price[hour])
    cycle += 1
    pass

# optimizing
objective_dict = {'external_grid': C_grid_t,
                  'battery': [0] * total_cycle,
                  'electrolyser': [0] * total_cycle,
                  'protein': [0] * total_cycle,
                  'soc': [0] * total_cycle,
                  'Mh2': [0] * total_cycle
                  }

c = np.array(objective_dict['external_grid'] + objective_dict['battery']
             + objective_dict['electrolyser'] + objective_dict['protein']
             + objective_dict['soc'] + objective_dict['Mh2'])  # 6*total cycle

# equality constraint
A_eq_gls = np.zeros((3 * total_cycle, objective_dict.__len__() * total_cycle))
B_eq_gls = np.zeros(3 * total_cycle)

# active power conservation
# TODO: overall protein should be constant
for t in range(0, total_cycle):
    A_eq_gls[t][t] = 1
    A_eq_gls[t][t + total_cycle] = -1
    A_eq_gls[t][t + 2 * total_cycle] = A_eq_gls[t][t + 3 * total_cycle] = -1
    B_eq_gls[t] = -power_pv_t[t] - power_wind_t[t] + np.array(load_data_p_mw).sum()
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
        A_eq_gls[t][t + 3 * total_cycle] = -1
        A_eq_gls[t][t - 1 + 3 * total_cycle] = 1
    pass

# Mh2 mass of h2, initial hydrogen is 0
for t in range(total_cycle * 2, total_cycle * 3):
    A_eq_gls[t][t] = 24 / total_cycle * 25  # assuming the efficiency is constant (25kg/Mwh)so that we can use linear programming
    if t == 2 * total_cycle:
        A_eq_gls[t][t + 3 * total_cycle] = -1
        B_eq_gls[t]=0
    else:
        A_eq_gls[t][t + 3 * total_cycle] = -1
        A_eq_gls[t][t - 1 + 3 * total_cycle] = 1
    pass

# inequality constraints, only for ultimate hydrogen, meaning that at least generating 1000kg h2
A_ineq_gls = np.zeros((3 * total_cycle, objective_dict.__len__() * total_cycle))
B_ineq_gls = np.zeros(3 * total_cycle)
t = 3*total_cycle
A_ineq_gls[-1][-1]=-1
B_ineq_gls[-1]=-1780

# bound
demand_response = True
if demand_response ==True:
    pro = (0.8,1.2)
else:
    pro = (1,2)
# TODO:add variables in source file
bound_dict = {'external_grid': [(None, None)] * total_cycle,
              'battery': [(-1.36, 1.36)] * total_cycle,
              'electrolyser': [(-1e-4, Electrolyser_gls.max_power)] * total_cycle,
              'protein': [pro] * total_cycle,
              'soc': [(Battery_gls.soc_min, Battery_gls.soc_max)] * total_cycle,
              'Mh2': [(0, Hydrogen_tank_gls.mass_max)] * total_cycle
              }

bound = bound_dict['external_grid'] + bound_dict['battery'] + bound_dict['electrolyser'] \
        + bound_dict['protein'] + bound_dict['soc'] + bound_dict['Mh2']
bound_gls = tuple(bound)

# solve
res = op.linprog(c, A_ub= A_ineq_gls, b_ub=B_ineq_gls,A_eq=A_eq_gls, b_eq=B_eq_gls, bounds=bound_gls)
print(res)
print(res.success)

res_dict_opt = {'external_grid': res.x[0:total_cycle],
                'battery': res.x[total_cycle:2 * total_cycle],
                'electrolyser': res.x[2 * total_cycle:3 * total_cycle],
                'protein': res.x[3 * total_cycle:4 * total_cycle],
                'soc': res.x[4 * total_cycle:5 * total_cycle],
                'Mh2': res.x[5 * total_cycle:6 * total_cycle]
                }

cycle_power_flow = 0

while cycle_power_flow < total_cycle:
    hour = cycle_power_flow // 4

    # %% Run network builder function

    gls_network, gls_network_results_original = gls_network_function.gls_network_builder()

    # %% Change power consumption from loads
    gls_network.load.loc[:, 'name']  # order in which to supply load data

    #electrolyser as a load
    load_data_p_mw[7]=0
    load_data_p_mw[2]=res_dict_opt['protein'][cycle_power_flow]

    gls_network.load.loc[:, 'p_mw'] = load_data_p_mw
    gls_network.load.loc[:, 'q_mvar'] = load_data_q_mvar

    # %% Change storage
    gls_network.storage

    gls_network.storage.loc[:, 'p_mw'] = res_dict_opt['battery'][cycle_power_flow]\
                                         +res_dict_opt['electrolyser'][cycle_power_flow]

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

    expenditure.append((external_grid_power[cycle_power_flow]*C_grid_t[cycle_power_flow]+
                       power_wind_t[cycle_power_flow]*wind_price + power_pv_t[cycle_power_flow]*pv_price+
                        0)*24/total_cycle)
    accumulated_expenditure.append(np.array(expenditure).sum())

    print(cycle_power_flow)

    cycle_power_flow += 1

res_dict={'P_grid':np.array(external_grid_power),
          'P_wind':np.array(power_wind_t),
          'P_pv':np.array(power_pv_t),
          'P_b':res_dict_opt['battery'],
          'P_ele':res_dict_opt['electrolyser'],
          'P_pro':res_dict_opt['protein'],
          'soc':res_dict_opt['soc'],
          'Mh2':res_dict_opt['Mh2'],
          'price_grid':np.array(C_grid_t),
          'expenditure':np.array(expenditure),
          'accumulated_ex':np.array(accumulated_expenditure)
          }

pd_results = pd.DataFrame(res_dict)

try:
    pd_results.to_csv(figure_file /'Usecase1' /'results_usecase1.csv')
except PermissionError:
    print('File already exists')

# # power supply
# supply_plt = np.array(supply_RES)
# time_plt = np.linspace(0, total_cycle - 1, total_cycle) / 4
#
# fig, ax = plt.subplots()
# ax.plot(time_plt, supply_RES, 'ro-')
# ax.set_xlabel('Time/ hour')
# ax.set_ylabel('Power supplied by RES/ MW')
# plt.savefig(figure_file /'Usecase1' / 'res.png', dpi=150)
# plt.show()
#
# # battery soc
# fig_battery, ax_battery = plt.subplots()
# ax_battery.plot(time_plt, battery_soc, 'bo-')
# ax_battery.set_xlabel('Time/ hour')
# ax_battery.set_ylabel('Battery SOC')
# plt.savefig(figure_file /'Usecase1' / 'battery_soc.png', dpi=150)
# plt.show()
#
# # hydrogen tank pressure
# fig_hydrogen, ax_hydrogen = plt.subplots()
# ax_hydrogen.plot(time_plt, hydrogen_pressure, 'go-')
# ax_hydrogen.set_xlabel('Time/ hour')
# ax_hydrogen.set_ylabel('Hrdrogen pressure/ Mpa')
# plt.savefig(figure_file /'Usecase1' / 'H2Pressure.png', dpi=150)
# plt.show()
#
# # external grid power
# fig_eg, ax_eg = plt.subplots()
# ax_eg.plot(time_plt, external_grid_power, color='black', marker='x')
# ax_eg.set_xlabel('Time/ hour')
# ax_eg.set_ylabel('Power supplied by external grid/ MW')
# plt.savefig(figure_file /'Usecase1' / 'external power.png', dpi=150)
# plt.show()
#
# # electrolyser
# fig_ele, ax_ele = plt.subplots()
# ax_ele.plot(time_plt, electrolyser_input_power, color='black', marker='o')
# ax_ele.set_xlabel('Time/ hour')
# ax_ele.set_ylabel('Electrolyser input power/ MW')
# plt.savefig(figure_file /'Usecase1' / 'electrolyser.png')
# plt.show()
#
# # green hydrogen
# fig_per, ax_per = plt.subplots()
# ax_per.plot(time_plt, percentage_using_res, color='black')
# ax_per.set_xlabel('Time/ hour')
# ax_per.set_ylabel('Electrolyser input power/ MW')
# plt.savefig(figure_file /'Usecase1' / 'percentage.png')
# plt.show()
#
# # economics
#
# fig_eco, (ax_acc, ax_eco) = plt.subplots(2, sharex=True)
#
# ax_eco.plot(time_plt, expenditure, color='deepskyblue', label='expedicture per 15min')
# ax_eco.set_xlabel('Time/ hour')
# ax_eco.set_ylabel('Expenditure/ Euros')
# ax_eco.legend()
#
# ax_acc.plot(time_plt, accumulated_expenditure, color='steelblue', label='accumulated expenditure')
# ax_acc.set(ylabel='Expenditure/ Euros')
# ax_acc.legend()
#
# plt.savefig(figure_file /'Usecase1' / 'economics.png')
# plt.show()
#
# # Write all results in a dictionary
# results = {}
# results['supply_RES'] = supply_RES
# results['battery_soc'] = battery_soc
# results['hydrogen_pressure'] = hydrogen_pressure
# results['external_grid_power'] = external_grid_power
# results['electrolyser_input_power'] = electrolyser_input_power
# results['expenditure'] = expenditure
# results['accumulated_expenditure'] = accumulated_expenditure
#
#
#

