'''
Created on: 20200915

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
from equipment_package import wind_turbine, electrolyser, hydrogen_tank
from openpyxl import *
from pathlib import Path
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

Absolute_path = Path().absolute()

# Weibull_min distritbution
def _weibull_min(x,c,loc,scale):
    return c/scale*((x-loc)/scale)**(c-1)*np.exp(-((x - loc)/scale)**c)


class HWHS(object):
    def set_wt(self, number=13):
        self.wind_turbine = [wind_turbine.wind_turbine()] * number

    def set_ele(self):
        self.electrolyser = electrolyser.electrolyser_group()


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

        #-------------------------------------plot statistical results----------------------------
        # Interval number
        num_bins = 100

        # Dipict frequency distribution histgram
        fig, ax = plt.subplots()
        # N is the count in each bin, bins is the lower-limit of the bin
        N, bins, patches = ax.hist(WS_10_m, num_bins)

        #------------------------------------Fitting curve-----------------------------------------
        fig1, ax1 = plt.subplots()
        x = np.linspace(WS_10_m.min(),WS_10_m.max(),num_bins)
        y1 = [stats.weibull_min.pdf(i,shape,loc,scale) for i in x]
        ax1.plot(x,y1)
        # Self-defined function
        y2 = [_weibull_min(i,shape,loc, scale) for i in x]
        ax1.plot(x,y2,color = 'red')

        #------------------------------------Fitting curve and statistical data--------------------
        fig2,ax2 = plt.subplots()
        ax2.hist(WS_10_m, num_bins, density = True, color = 'tab:blue', alpha = 0.5)
        ax2.plot(x,y1, label = 'Fitted weibull dist')
        ax2.set(xlabel= 'Wind speed(m/s)', ylabel= 'Frequency',title = 'Weibull distribution fitting')
        ax2.legend()
        plt.show()

        # Save data
        wind_speed_data = pd.DataFrame()
        bins = bins.tolist()
        bins.pop(-1)
        wind_speed_data['Speed'] = bins
        wind_speed_data['Frequency'] = [i/WS_10_m.size for i in N]
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
        #-------------------------------------print statistical results----------------------------
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

        #-------------------------------------Fitting -----------------------------------------------
        loc, scale = stats.norm.fit(ele_price, loc=10)
        print(f'Parameters of normal distribution is mu = {round(loc,2)},sigma = {round(scale,2)}')
        fig1, ax1 = plt.subplots()
        x = np.linspace(ele_price.min(),ele_price.max(),num_bins)
        '''
        Specifically, norm.pdf(x, loc, scale) is identically equivalent to 
        norm.pdf(y) / scale with y = (x - loc) / scale
        '''
        y1 = [stats.norm.pdf(i,loc,scale) for i in x]
        ax1.plot(x,y1, label = 'Fitted normal dist')
        ax1.hist(ele_price, num_bins, color = 'tab:orange', alpha = 0.5 , density=True)
        ax1.set(xlabel = 'Price/€',ylabel= 'Frequency')
        ax1.legend()
        fig1.tight_layout()
        plt.show()

    def hydrogen_demand(self):
        pass


if __name__ == '__main__':
    a = Uncertainity_variable()
    b = a.electricity_price()
