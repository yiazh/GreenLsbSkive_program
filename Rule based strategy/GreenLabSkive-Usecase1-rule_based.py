'''
Created on June 14, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147 Elevation:30m Slope:44 Azimuth:3
'''
from equipment_package import wind_turbine, battery, hydrogen
from equipment_package import pv, electrolyser, gls_network_function, economic
from prediction_wind_solar_price_load import wind_speed_prediction_MLP, solar_irradiance_prediction, \
    ele_price_prediction
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

figure_file = Path(Path().absolute().parent / 'Figure')

fig_pre_solar, ax_pre_solar = plt.subplots()
ax_pre_solar.plot(range(real_solar_irradiance.__len__()), real_solar_irradiance,
                  color='orangered', label='real value')
ax_pre_solar.plot(range(predicted_solar_irradiance.__len__()), predicted_solar_irradiance,
                  color='navy', label='predicted value')
ax_pre_solar.legend()
ax_pre_solar.set_xlabel('Time(hour)')
ax_pre_solar.set_ylabel('Solar irradiance(W/m2)')
ax_pre_solar.grid()
plt.savefig(figure_file / 'solar_pred.png', dpi=150)

fig_pre_wind, ax_pre_wind = plt.subplots()
ax_pre_wind.plot(range(real_observed_wind_speed.__len__()), real_observed_wind_speed,
                 color='orangered', label='real data')
ax_pre_wind.plot(range(predicted_wind_speed.__len__()), predicted_wind_speed,
                 color='navy', label='predicted data')
ax_pre_wind.legend()
ax_pre_wind.set_xlabel('Time(hour)')
ax_pre_wind.set_ylabel('Wind speed(m/s)')
ax_pre_wind.set_ylim([3, 6])
ax_pre_wind.grid()
plt.savefig(figure_file / 'wind_speed_pred.png', dpi=150)
print('Prediction results saved')

# Read data on 0411
directory_path = Path(Path().absolute().parent)
input_data_path = r'{}/prediction_wind_solar_price_load/Historical_Data'.format(directory_path)

File_data = input_data_path + '/pv_wind_data_0411.csv'

Ambient_Data = pd.read_csv(File_data)
# ---------------------------------------Data preprocessing-----------------------------------------
Annual_real_rate = 0.05
OandM_cost = (54 * 2e6 * 0.02 + 26.8 * 3e6 * 0.02) / (54 + 26.8) / (365 * 24)
hourly_cost = economic.crf(Annual_real_rate) * (54 * 2e6 + 26.8 * 3e6) / 365 / 24 / (54 + 26.8)
res_av_cost = OandM_cost + hourly_cost

# Build the wind turbines
WT_gls = [wind_turbine.wind_turbine(r=40, height=40)] * 13

# Build the photovoltaics
PV_gls = [pv.pv()] * 6

# Build the battery
Battery_gls = battery.battery_bank(soc_min=0.1)

# Build the electrolyser
Electrolyser_gls = electrolyser.electrolyser_group()

# Build the hydrogen tank
Hydrogen_tank_gls = hydrogen.hydrogen_tank(Volume_tank=60)  # Given the fact that trailers carry 1000kg H2

# Build the load
load_data_p_mw = [0.98,  # Quantfuel, 2020), start up tests currently. It also consumes H2,CH4 and plastic waster
                  2.5,  # Biogas
                  0.8,  # Danish Marine Protein
                  0.15,  # Ever Fuel, fillinig typical four hours. 200bar to 400bar, 900+kg Hydrogen
                  3.25,  # Recycle facility
                  0.7,  # Methanol facility
                  2,  # GreenSkive college
                  0,  # Electrolyser, which is considered in storage
                  ]
load_data_q_mvar = [0.2] * 8

supply_RES = []  # Total energy supplied by RES
battery_soc = []
hydrogen_pressure = []
external_grid_power = []
electrolyser_input_power = []
hydrogen_consumption = []
accumulated_hydrogen_consumption = []
expenditure = []
accumulated_expenditure = []
percentage_using_res = []
h2_production_cost = []
accumulated_h2_production_cost = []

# Main loop
cycle = 0
while cycle < total_cycle:
    # Corresponding time, hour
    hour = cycle // 4

    # Run network builder function
    gls_network, gls_network_results_original = gls_network_function.gls_network_builder()

    # ----------------------------Consumption------------------------------------------------
    # %% Change power consumption from loads
    gls_network.load.loc[:, 'name']  # order in which to supply load data

    gls_network.load.loc[:, 'p_mw'] = load_data_p_mw
    gls_network.load.loc[:, 'q_mvar'] = load_data_q_mvar

    Load = np.array(load_data_p_mw).sum()

    # ----------------------------Generation------------------------------------------------
    # Wind speed at 10m
    v_wind = predicted_wind_speed[hour]

    # Solar irradiance and surrounding temperature
    irradiance = predicted_solar_irradiance[hour]
    T_sur = Ambient_Data['T2m'][hour]

    # %% Change power of generators
    gls_network.sgen.loc[:, 'name']  # order in which to supply generator data

    generator_data_p = []  # data about power production goes here
    for i in WT_gls:
        generator_data_p.append(i.wt_ac_output(v_wind))

    for i in PV_gls:
        generator_data_p.append(i.pv_ac_output(irradiance, T_sur))

    generator_data_q_mvar = [0] * 19

    # Get the total supply from RE
    RE_power = np.array(generator_data_p).sum()
    supply_RES.append(RE_power)

    # excessive power
    Ex_power = RE_power - Load

    gls_network.sgen.loc[:, 'p_mw'] = generator_data_p
    gls_network.sgen.loc[:, 'q_mvar'] = generator_data_q_mvar

    # -----------------------------Strategies-----------------------------------------------
    if predicted_day_ahead_ele_price[hour] < res_av_cost:
        electrolyser.set_power_group(Electrolyser_gls, 12)
        if Hydrogen_tank_gls.p <= 200 * p0:
            Electrolyser_storage = Electrolyser_gls.power()
            Hydrogen_tank_gls.blow_up(q_h2=Electrolyser_gls.n_H2(), time=900)
        else:
            Electrolyser_storage = 0
        Battery_storage = Battery_gls.charge(time=900)
        h2_production_cost.append(Electrolyser_storage * predicted_day_ahead_ele_price[hour] * 0.25)
    else:
        if Ex_power > 0:
            if Ex_power >= 12:
                electrolyser.set_power_group(Electrolyser_gls, 12)
                if Hydrogen_tank_gls.p <= 200 * p0:
                    Electrolyser_storage = Electrolyser_gls.power()
                    Hydrogen_tank_gls.blow_up(q_h2=Electrolyser_gls.n_H2(), time=900)
                else:
                    Electrolyser_storage = 0
            elif Ex_power <= Electrolyser_gls.min_power:
                Electrolyser_storage = 0
            else:
                electrolyser.set_power_group(Electrolyser_gls, Ex_power)
                if Hydrogen_tank_gls.p <= 200 * p0:
                    Electrolyser_storage = Electrolyser_gls.power()
                    Hydrogen_tank_gls.blow_up(q_h2=Electrolyser_gls.n_H2(), time=900)
        Battery_storage = Battery_gls.discharge(time=900)
        h2_production_cost.append(Electrolyser_storage * res_av_cost * 0.25)
    electrolyser_input_power.append(Electrolyser_storage)

    # -----------------------------Hydrogen Consumption----------------------------------
    if hour > 8 and hour < 16:
        hydrogen_ran = np.random.uniform()
        if hydrogen_ran < 0.5:
            H2_consumption = Hydrogen_tank_gls.deflate(q_h2=34, time=900)
            hydrogen_consumption.append(H2_consumption)
        else:
            hydrogen_consumption.append(0)
    hydrogen_pressure.append(Hydrogen_tank_gls.p / p0)

    # -----------------------------Storage-----------------------------------------------
    battery_soc.append(Battery_gls.soc)

    # %% Change storage
    gls_network.storage

    storage_data_p_mw = Battery_storage + Electrolyser_storage  # data about charging/discharging power from battery goes here

    gls_network.storage.loc[:, 'p_mw'] = storage_data_p_mw

    #
    # %% Run pandapower power flow with new set of data
    pp.runpp(gls_network, trafo_loading='power', algorithm='iwamoto_nr', calculate_voltage_angles='auto')

    # -----------------------------Power flow calculation--------------------------------
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

    # -------------------------------------------economics------------------------------------------
    expenditure.append(
        (gls_network_results['External_grid']['p_mw'][0]) * 0.25 * predicted_day_ahead_ele_price[hour] +
        RE_power * res_av_cost)

    accumulated_expenditure.append(np.array(expenditure).sum())
    accumulated_h2_production_cost.append(np.array(h2_production_cost).sum())
    accumulated_hydrogen_consumption.append(np.array(hydrogen_consumption).sum())

    if Electrolyser_storage > 0:
        percentage_using_res.append(1)
    else:
        percentage_using_res.append(0)

    print(cycle)
    cycle += 1
    pass

# power supply
supply_plt = np.array(supply_RES)
time_plt = np.linspace(0, total_cycle - 1, total_cycle) / 4

fig, ax = plt.subplots()
ax.plot(time_plt, supply_RES, 'ro-')
ax.set_xlabel('Time/ hour')
ax.set_ylabel('Power supplied by RES/ MW')
plt.savefig(figure_file / 'Usecase1_RB' / 'res.png', dpi=150)

# battery soc
fig_battery, ax_battery = plt.subplots()
ax_battery.plot(time_plt, battery_soc, 'bo-')
ax_battery.set_xlabel('Time/ hour')
ax_battery.set_ylabel('Battery SOC')
plt.savefig(figure_file / 'Usecase1_RB' / 'battery_soc.png', dpi=150)

# hydrogen tank pressure
fig_hydrogen, ax_hydrogen = plt.subplots()
ax_hydrogen.plot(time_plt, hydrogen_pressure, 'go-')
ax_hydrogen.set_xlabel('Time/ hour')
ax_hydrogen.set_ylabel('Hrdrogen pressure/ Mpa')
plt.savefig(figure_file / 'Usecase1_RB' / 'H2Pressure.png', dpi=150)

# external grid power
fig_eg, ax_eg = plt.subplots()
ax_eg.plot(time_plt, external_grid_power, color='black', marker='x')
ax_eg.set_xlabel('Time/ hour')
ax_eg.set_ylabel('Power supplied by external grid/ MW')
plt.savefig(figure_file / 'Usecase1_RB' / 'external power.png', dpi=150)

# electrolyser
fig_ele, ax_ele = plt.subplots()
ax_ele.plot(time_plt, electrolyser_input_power, color='black', marker='o')
ax_ele.set_xlabel('Time/ hour')
ax_ele.set_ylabel('Electrolyser input power/ MW')
plt.savefig(figure_file / 'Usecase1_RB' / 'electrolyser.png')

# green hydrogen
fig_per, ax_per = plt.subplots()
ax_per.plot(time_plt, percentage_using_res, color='black')
ax_per.set_xlabel('Time/ hour')
ax_per.set_ylabel('Electrolyser input power/ MW')
plt.savefig(figure_file / 'Usecase1_RB' / 'percentage.png')

# economics
fig_eco, (ax_acc, ax_eco) = plt.subplots(2, sharex=True)

ax_eco.plot(time_plt, expenditure, color='deepskyblue', label='expedicture per 15min')
ax_eco.set_xlabel('Time/ hour')
ax_eco.set_ylabel('Expenditure/ Euros')
ax_eco.legend()

ax_acc.plot(time_plt, accumulated_expenditure, color='steelblue', label='accumulated expenditure')
ax_acc.set(ylabel='Expenditure/ Euros')
ax_acc.legend()

plt.savefig(figure_file / 'Usecase1_RB' / 'economics.png')

# Write all results in a dictionary
results = {}
results['supply_RES'] = supply_RES
results['battery_soc'] = battery_soc
results['hydrogen_pressure'] = hydrogen_pressure
results['external_grid_power'] = external_grid_power
results['electrolyser_input_power'] = electrolyser_input_power
results['expenditure'] = expenditure
results['accumulated_expenditure'] = accumulated_expenditure
results['h2_production_cost_per_15min'] = h2_production_cost
results['h2_production_cost_per_accumulated'] = accumulated_h2_production_cost

pd_results = pd.DataFrame(results)

try:
    pd_results.to_csv(figure_file / 'Usecase1_RB' / 'results_usecase1.csv')
except PermissionError:
    print('File already exists')
