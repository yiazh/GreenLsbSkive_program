'''
Created on May 20, 2020

Author: Yi Zheng

GreenLab Skive: latitude: 56.645347 Longitude: 8.978147

This program calculates on-grid operation of GreenLab skive. No real data of wind and solar power
'''
from scipy.stats import weibull_min
from equipment_package import wind_turbine, battery, hydrogen
from equipment_package import pv, electrolyser,gls_network_function
import math
import numpy as np
import pandapower as pp
import pandas as pd
import matplotlib.pyplot as plt

total_time = 240 #8760h
p0 = 101325 # Atmospheric pressure
np.random.seed(1) # Make sure the random variables are the same every time

def list_add(a,n):
	"for a given list a, get the sum of its n terms "
	c = 0
	for i in range(0,n):
		c += int(a[i])
	return c

def Roughly_simulate_solar_irradiance(time):
	clock = time %24
	month = time//(24*30)+1
	irradiance_max = 1000- 100*math.fabs(month - 6)+np.random.uniform(0,100)
	if clock <=5 | clock >23:
		irradiance = 0;
	else :
		irradiance = max(0,irradiance_max - 100*math.fabs(clock - 14)*np.random.uniform(0,1))
	return irradiance

# Build the wind turbines
WT_gls = [wind_turbine.wind_turbine(r= 40, height = 40)]*13

# Build the photovoltaics
PV_gls = [pv.pv()]*6

# Build the battery
Battery_gls = battery.battery_bank(soc_min = 0)

#Build the electrolyser
Electrolyser_gls = electrolyser.electrolyser_group()

#Build the hydrogen tank
Hydrogen_tank_gls = hydrogen.hydrogen_tank()

#Build the load
pass

supply_hourly = []
battery_soc = []
hydrogen_pressure = []
external_grid_power = []

# Main loop
time = 0
while time<total_time:
	# %% Run network builder function
	gls_network, gls_network_results_original = gls_network_function.gls_network_builder()

	# Simulating wind speed via weibull distribution
	n = 1  # number of samples
	k = 2  # shape factor should be calculated from the wind data, not available now
	lam = 5  # scale,should be calculated from the wind data, not available now
	v_wind = weibull_min.rvs(k, loc=0, scale=lam, size=n)

	# Solar irradiance and surrounding temperature
	irradiance = Roughly_simulate_solar_irradiance(time)
	T_sur = 25

	# %% Change power of generators
	gls_network.sgen.loc[:, 'name']  # order in which to supply generator data

	fake_generator_data_p_mw = []  # data about power production goes here
	for i in WT_gls:
		fake_generator_data_p_mw.append(i.wt_ac_output(v_wind[0]))

	for i in PV_gls:
		fake_generator_data_p_mw.append(i.pv_ac_output(irradiance, T_sur))

	fake_generator_data_q_mvar = [0] * 19

	#Get the total supply from RE
	RE_power = np.array(fake_generator_data_p_mw).sum()
	supply_hourly.append(RE_power)

	gls_network.sgen.loc[:, 'p_mw'] = fake_generator_data_p_mw
	gls_network.sgen.loc[:, 'q_mvar'] = fake_generator_data_q_mvar

	# %% Change power consumption from loads
	gls_network.load.loc[:, 'name']  # order in which to supply load data

	fake_load_data_p_mw = [1.5] * 8  # data about power production goes here
	fake_load_data_q_mvar = [0.2] * 8

	gls_network.load.loc[:, 'p_mw'] = fake_load_data_p_mw
	gls_network.load.loc[:, 'q_mvar'] = fake_load_data_q_mvar

	Load = np.array(fake_load_data_p_mw).sum()

#-----------------------------Strategies---------------------------------------#
	if RE_power > Load:
		Battery_storage = Battery_gls.charge(time = 3600)
		if Battery_storage == 0 or RE_power - Load - Battery_storage > 0:
			if Hydrogen_tank_gls.p <= 200*p0:
				Electrolyser_storage = Electrolyser_gls.power()
				Hydrogen_tank_gls.blow_up(q_h2= Electrolyser_gls.n_H2())
			else:
				Electrolyser_storage = 0
	else:
		Battery_storage = Battery_gls.discharge(time = 3600)
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
	time += 1
	pass

# power supply
supply_plt = np.array(supply_hourly)
time_plt = np.linspace(0,total_time-1,total_time)
fig, ax = plt.subplots()
ax.plot(time_plt, supply_hourly, 'ro-')
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