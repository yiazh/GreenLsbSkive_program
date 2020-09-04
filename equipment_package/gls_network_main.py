# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:10:14 2020

@author: Sergey Klyapovskiy, postdoctoral researcher at Technical University of Denmark (DTU)

This is the main file for running power flow analysis using GreenLab Skive network in PandaPower
"""

#%% Import modules
import numpy as np
#import os
import pandas as pd
import pandapower as pp
from gls_network_function import gls_network_builder

#%% Run network builder function
gls_network, gls_network_results_original = gls_network_builder()

#%% Change power consumption from loads
gls_network.load.loc[:, 'name']     # order in which to supply load data

fake_load_data_p_mw = [0.5]*8             # data about power production goes here
fake_load_data_q_mvar = [0.2]*8

gls_network.load.loc[:, 'p_mw'] = fake_load_data_p_mw
gls_network.load.loc[:, 'q_mvar'] = fake_load_data_q_mvar 

#%% Change storage
gls_network.storage

fake_storage_data_p_mw = 1          # data about charging/discharging power from battery goes here  

gls_network.storage.loc[:,'p_mw'] = fake_storage_data_p_mw

#%% Change power of generators
gls_network.sgen.loc[:,'name']      # order in which to supply generator data

fake_generator_data_p_mw = [3]*19   # data about power production goes here
fake_generator_data_q_mvar = [0]*19

gls_network.sgen.loc[:,'p_mw'] = fake_generator_data_p_mw
gls_network.sgen.loc[:,'q_mvar'] = fake_generator_data_q_mvar

#%% Run pandapower power flow with new set of data
pp.runpp(gls_network, trafo_loading = 'power', algorithm = 'iwamoto_nr', calculate_voltage_angles = 'auto')

#%% Write results in the dictionary
# Add names of the rows
gls_network.res_bus.insert(0, 'name', pd.Series(gls_network.bus.loc[:,'name']), allow_duplicates = False)
gls_network.res_trafo.insert(0, 'name', pd.Series(gls_network.trafo.loc[:,'name']), allow_duplicates = False)
gls_network.res_line.insert(0, 'name', pd.Series(gls_network.line.loc[:,'name']), allow_duplicates = False)
gls_network.res_load.insert(0, 'name', pd.Series(gls_network.load.loc[:,'name']), allow_duplicates = False)
gls_network.res_storage.insert(0, 'name', pd.Series(gls_network.storage.loc[:,'name']), allow_duplicates = False)
gls_network.res_sgen.insert(0, 'name', pd.Series(gls_network.sgen.loc[:,'name']), allow_duplicates = False)

# Write all results in the dictionary
gls_network_results = {}
gls_network_results['Bus'] = gls_network.res_bus
gls_network_results['External_grid'] = gls_network.res_ext_grid
gls_network_results['Transformer'] = gls_network.res_trafo
gls_network_results['Cable'] = gls_network.res_line
gls_network_results['Load'] = gls_network.res_load
gls_network_results['Storage'] = gls_network.res_storage
gls_network_results['Generator'] = gls_network.res_sgen







