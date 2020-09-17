'''
Created on June 4, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147 Elevation:30m Slope:44 Azimuth:3

Day-ahead scheduling of GLS using real data to predict wind speed, solar irradiation and surrounding temperature.
'''
from scipy.stats import weibull_min
from equipment_package import wind_turbine, battery, hydrogen_tank
from equipment_package import pv, electrolyser,gls_network_function
import os
import math
import numpy as np
import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt
from prediction_wind_solar_price_load import wind_speed_prediction_MLP

total_cycle = 96 # 96*15 minutes,24h
p0 = 101325 # Atmospheric pressure

#20160410 real data
day_ahead_wind_speed_data = np.array([4.23,4.53,4.83,5.13,5.31,5.49,5.67,5.66,5.64,5.63,5.54,5.46,
									  5.38,5.6,5.83,6.06,5.84,5.63,5.42,5.13,4.83,4.54,4.37,4.2])
# 20160411 real data, for reference
real_observed_wind_speed = np.array([4.03, 4.02,4.01,4,3.92,3.84,3.77,3.91,4.06,4.21,4.29,4.36,4.44,
							 	     4.73,5.02,5.31,5.22,5.13,5.03,4.94,4.84,4.74,4.58,4.42])
# prediction data
predicted_wind_speed = wind_speed_prediction_MLP.prediction_function_wind_mlp(day_ahead_wind_speed_data)

# Read data on 0411
directory_path = os.path.dirname(__file__)
input_data_path = r'{}/prediction_wind_solar_price_load/Historical_Data'.format(directory_path)

File_data = input_data_path + '/pv_wind_data_0411.csv'

Ambient_Data = pd.read_csv(File_data)

# Build the wind turbines
WT_gls = [wind_turbine.wind_turbine(r= 40, height = 40)]*13

# Build the photovoltaics
PV_gls = [pv.pv()]*6

# Build the battery
Battery_gls = battery.battery_bank(soc_min = 0)

#Build the electrolyser
Electrolyser_gls = electrolyser.electrolyser_group()

#Build the hydrogen tank
Hydrogen_tank_gls = hydrogen_tank.hydrogen_tank()

supply_hourly = []
battery_soc = []
hydrogen_pressure = []
external_grid_power = []

# Main loop
cycle = 0
while cycle<total_cycle:
	# Corresponding time
	hour = cycle//4

	# %% Run network builder function
	gls_network, gls_network_results_original = gls_network_function.gls_network_builder()

	# Wind speed at 10m
	v_wind = predicted_wind_speed[hour]

	# Solar irradiance and surrounding temperature
	irradiance = Ambient_Data['G(i)'][hour]
	T_sur = Ambient_Data['T2m'][hour]

	# %% Change power of generators
	gls_network.sgen.loc[:, 'name']  # order in which to supply generator data

	generator_data_p = []  # data about power production goes here
	for i in WT_gls:
		generator_data_p.append(i.wt_ac_output(v_wind))

	for i in PV_gls:
		generator_data_p.append(i.pv_ac_output(irradiance, T_sur))

	generator_data_q_mvar = [0] * 19

	#Get the total supply from RE
	RE_power = np.array(generator_data_p).sum()
	supply_hourly.append(RE_power)

	gls_network.sgen.loc[:, 'p_mw'] = generator_data_p
	gls_network.sgen.loc[:, 'q_mvar'] = generator_data_q_mvar

	# %% Change power consumption from loads
	gls_network.load.loc[:, 'name']  # order in which to supply load data

	fake_load_data_p_mw = [1.5] * 8  # data about power production goes here
	fake_load_data_q_mvar = [0.2] * 8

	gls_network.load.loc[:, 'p_mw'] = fake_load_data_p_mw
	gls_network.load.loc[:, 'q_mvar'] = fake_load_data_q_mvar

	Load = np.array(fake_load_data_p_mw).sum()

	#excessive power
	Ex_power = RE_power - Load
#-----------------------------Strategies---------------------------------------#
	if Ex_power > 0:
		Battery_storage = Battery_gls.charge(time = 900)
		if Battery_storage == 0 or RE_power - Load - Battery_storage > 0:
			if Hydrogen_tank_gls.p <= 200*p0:
				Electrolyser_storage = Electrolyser_gls.power()
				Hydrogen_tank_gls.blow_up(q_h2= Electrolyser_gls.n_H2())
			else:
				Electrolyser_storage = 0
	else:
		Battery_storage = Battery_gls.discharge(time = 900)
		Electrolyser_storage = 0
# -----------------------------Strategies---------------------------------------#

# -----------------------------Hydrogen Consumption-----------------------------#
	hydrogen_ran = np.random.uniform()
	if hydrogen_ran < 0.2:
		Hydrogen_tank_gls.deflate()
# -----------------------------Hydrogen Consumption-----------------------------#

	battery_soc.append(Battery_gls.soc)
	hydrogen_pressure.append(Hydrogen_tank_gls.p/p0)

	# %% Change storage
	gls_network.storage

	fake_storage_data_p_mw = Battery_storage + Electrolyser_storage  # data about charging/discharging power from battery goes here

	gls_network.storage.loc[:, 'p_mw'] = fake_storage_data_p_mw

	# %% Run pandapower power flow with new set of data
	pp.runpp(gls_network, trafo_loading='power', algorithm='iwamoto_nr', calculate_voltage_angles='auto')

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
	cycle += 1
	print(cycle)
	pass

# power supply
supply_plt = np.array(supply_hourly)
time_plt = np.linspace(0,total_cycle-1,total_cycle)
fig, ax = plt.subplots()
ax.plot(time_plt, supply_hourly, 'ro-')
ax.set_xlabel('Time/ x15 min')
ax.set_ylabel('Power/ MW')
plt.show()

#battery soc
fig_battery, ax_battery = plt.subplots()
ax_battery.plot(time_plt, battery_soc, 'bo-')
plt.show()

# hydrogen tank pressure
fig_hydrogen, ax_hydrogen = plt.subplots()
ax_hydrogen.plot(time_plt, hydrogen_pressure, 'go-')
plt.show()

# external grid power
fig_eg, ax_eg = plt.subplots()
ax_eg.plot(time_plt, external_grid_power, color = 'black', marker = 'x')
plt.show()
pass