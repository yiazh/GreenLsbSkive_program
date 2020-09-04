# -*- coding: utf-8 -*-
"""
Created on Sun May 24 17:26:04 2020

@author: Sergey Klyapovskiy, postdoctoral researcher at Technical University of Denmark (DTU)

This function creates a model of electrical 60/20-10 kV distribution network of GreenLab Skive in Pandapower
"""

def gls_network_builder():
    #%% Import modules
    import numpy as np
    import os
    import pandas as pd
    import pandapower as pp
    
    #%% Define folder for input data
    directory_path = os.path.dirname(__file__)
    input_folder_path = r'{}/input'.format(directory_path) # path to be created\
        
    try:
        os.makedirs(input_folder_path) 
    except OSError:
        pass
    
    #%% Load initial data
    filename = input_folder_path + '/network_data.xlsx'
    
    # Bus data
    bus_data_raw = pd.read_excel(filename,  sheet_name ='Buses')
    
    # Transformer data
    transformer_data_raw = pd.read_excel(filename,  sheet_name ='Transformers')
    
    # Cable data
    cable_data_raw = pd.read_excel(filename,  sheet_name ='Cables')
    
    # Load data
    load_data_raw = pd.read_excel(filename,  sheet_name ='Loads')
    
    # Electrical storage data
    storage_data_raw = pd.read_excel(filename,  sheet_name ='Storage')
    
    # Generator data
    generator_data_raw = pd.read_excel(filename,  sheet_name ='Generators')
    
    #%% Create empty pandapower model
    gls_network = pp.create_empty_network()
        
    #%% Add 10 kV feeder buses to model
    number_of_buses = len(bus_data_raw)
    
    variable_name = {}
    
    for i in range(number_of_buses):
        bus_name = bus_data_raw.loc[i,'name']
        bus_voltage = bus_data_raw.loc[i,'voltage_kv']
        bus_type = bus_data_raw.loc[i,'type']
        bus_zone = bus_data_raw.loc[i,'zone']
        
        variable_name['BUS' + str(i)] = pp.create_bus(gls_network, 
                                             name = bus_name, 
                                             vn_kv = bus_voltage, 
                                             type = bus_type, 
                                             zone = bus_zone,
                                             geodata = None)
        
        locals().update(variable_name)  
    
    #%% Write bus information
    bus_information = gls_network.bus
    
    #%% Make connection to external network
    pp.create_ext_grid(gls_network, 0, name = 'Upstream_60_kV_system', vm_pu = 1.04, va_degree = 0) # create an external network connection
    
    #%% Write information about external connection
    external_network_information = gls_network.ext_grid # show external network table
    
    #%% Add transformers to model 
    number_of_transformers = len(transformer_data_raw)
    variable_name = {}
    
    for i in range(number_of_transformers):
        transformer_from_bus_index = np.where(transformer_data_raw.loc[i,'from'] == bus_information.iloc[:,0])
        transformer_to_bus_index = np.where(transformer_data_raw.loc[i,'to'] == bus_information.iloc[:,0])
        transformer_name = transformer_data_raw.loc[i,'name']
        transformer_apparent_power = transformer_data_raw.loc[i,'rating_mva']
        transformer_shift_degree = transformer_data_raw.loc[i,'shift_deg']
        transformer_hv = transformer_data_raw.loc[i,'high_voltage_kv']
        transformer_lv = transformer_data_raw.loc[i,'low_voltage_kv']
        transformer_uk = transformer_data_raw.loc[i,'vk_%']
        transformer_ukr = transformer_data_raw.loc[i,'vr_%']
        transformer_pfe = transformer_data_raw.loc[i,'pfe_kw']   
        transformer_i0 = transformer_data_raw.loc[i,'i0_%'] 
        
        variable_name['TRAFO' + str(i)] = pp.create_transformer_from_parameters(gls_network, 
                                           transformer_from_bus_index[0], 
                                           transformer_to_bus_index[0], 
                                           name = transformer_name, 
                                           sn_mva = transformer_apparent_power, 
                                           vn_hv_kv = transformer_hv, 
                                           vn_lv_kv = transformer_lv, 
                                           vk_percent = transformer_uk, 
                                           vkr_percent = transformer_ukr, 
                                           pfe_kw = transformer_pfe, 
                                           i0_percent = transformer_i0, 
                                           shift_degree = transformer_shift_degree)
        
        locals().update(variable_name)                                                           
     
    #%% Write transformer information
    trafo_information = gls_network.trafo
    
    #%% Add cables to model
    number_of_cables = len(cable_data_raw)
    
    variable_name = {}
    
    for i in range(number_of_cables):
        cable_from_bus_index = np.where(cable_data_raw.loc[i,'from'] == bus_information.iloc[:,0])
        cable_to_bus_index = np.where(cable_data_raw.loc[i,'to'] == bus_information.iloc[:,0])
        cable_name = cable_data_raw.loc[i,'name']
        cable_length = cable_data_raw.loc[i,'length_km']
        cable_r_per_km = cable_data_raw.loc[i,'r_ohm_per_km']
        cable_x_per_km = cable_data_raw.loc[i,'x_ohm_per_km']
        cable_c_per_km = cable_data_raw.loc[i,'c_nf_per_km']    # get capacitance in nF
        cable_I_max = cable_data_raw.loc[i,'max_i_a']/1000    # get current in kA
        cable_type = cable_data_raw.loc[i,'type']
        cable_state = cable_data_raw.loc[i,'in_service']
        cable_parallel = cable_data_raw.loc[i,'parallel']
        
        variable_name['CABLE' + str(i)] = pp.create_line_from_parameters(gls_network, 
                                           from_bus = cable_from_bus_index[0], 
                                           to_bus = cable_to_bus_index[0], 
                                           length_km = cable_length, 
                                           r_ohm_per_km = cable_r_per_km, 
                                           x_ohm_per_km = cable_x_per_km, 
                                           c_nf_per_km = cable_c_per_km, 
                                           max_i_ka = cable_I_max,
                                           name = cable_name, 
                                           index = None, 
                                           type = cable_type, 
                                           geodata = None, 
                                           in_service = cable_state, 
                                           df = 1.0, 
                                           parallel = cable_parallel)
        
        locals().update(variable_name)  
    
    #%% Write cable information
    cable_information = gls_network.line
    
    #%% Add loads
    number_of_loads = len(load_data_raw)
    
    variable_name = {}
    load_scaling = 1    # loading scale coefficient
    
    for i in range(number_of_loads):
        load_active_power = load_data_raw.loc[i,'p_mw']         #!!! modify this to change p_mw
        load_reactive_power = load_data_raw.loc[i,'q_mvar']     #!!! modify this to change q_mvar
        load_bus_index = np.where(load_data_raw.loc[i,'bus'] == bus_information.iloc[:,0])
        load_state = load_data_raw.loc[i,'in_service']
        load_name = load_data_raw.loc[i,'name']
        
    
        variable_name['LOAD' + str(i)] = pp.create_load(gls_network, 
                                          bus = load_bus_index[0], 
                                          p_mw = load_active_power, 
                                          q_mvar = load_reactive_power, 
                                          scaling = load_scaling, 
                                          name = load_name,
                                          in_service = load_state,
                                          controllable = False)
        
        locals().update(variable_name)  
    
    #%% Write load information
    load_information = gls_network.load
    
    #%% Add electrical storage
    number_of_storage = len(storage_data_raw)
    
    for i in range(number_of_storage):
        storage_bus_index = np.where(storage_data_raw.loc[i,'bus'] == bus_information.iloc[:,0])
        storage_p_mw = storage_data_raw.loc[i,'p_mw']         #!!! modify this to change p_mw 
        storage_q_mvar = storage_data_raw.loc[i,'q_mvar']     #!!! modify this to change q_mvar
        storage_max_e_mwh = storage_data_raw.loc[i,'max_e_mwh'] 
        storage_name = storage_data_raw.loc[i,'name']
        storage_state = storage_data_raw.loc[i,'in_service']
        
        variable_name['STORAGE' + str(i)] = pp.create_storage(gls_network, 
                                          bus = storage_bus_index[0], 
                                          p_mw = storage_p_mw, 
                                          q_mvar = storage_q_mvar, 
                                          max_e_mwh = storage_max_e_mwh, 
                                          name = storage_name,
                                          in_service = storage_state)
        
        locals().update(variable_name)  
    
    #%% Write storage information
    storage_information = gls_network.storage
    
    #%% Add generators
    number_of_generators = len(generator_data_raw)
    
    for i in range(number_of_generators):
        generator_bus_index = np.where(generator_data_raw.loc[i,'bus'] == bus_information.iloc[:,0])
        generator_p_mw = generator_data_raw.loc[i,'p_mw']           #!!! modify this to change p_mw  
        generator_q_mvar = generator_data_raw.loc[i,'q_mvar']       #!!! modify this to change q_mvar
        generator_name = generator_data_raw.loc[i,'name']
        generator_state = generator_data_raw.loc[i,'in_service']
        
        variable_name['STORAGE' + str(i)] = pp.create_sgen(gls_network, 
                                          bus = generator_bus_index[0], 
                                          p_mw = generator_p_mw, 
                                          q_mvar = generator_q_mvar, 
                                          name = generator_name,
                                          in_service = generator_state)
        
        locals().update(variable_name)  
    
    #%% Write generator information
    generator_information = gls_network.sgen
    
    #%% Combine network tables in the dictionary
    gls_network_information = {}
    gls_network_information['Bus'] = bus_information
    gls_network_information['External_grid'] = external_network_information
    gls_network_information['Transformer'] = trafo_information
    gls_network_information['Cable'] = cable_information
    gls_network_information['Load'] = load_information
    gls_network_information['Storage'] = storage_information
    gls_network_information['Generator'] = generator_information
    
    #%% Perform power flow
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
    
    return gls_network, gls_network_results