'''
This sub-program is used to predict the day-ahead price in DK1.

Not so relevant, abandoned
'''

import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import os

# df = pd.read_csv()
directory_path = os.path.dirname(__file__)
input_data_path = r'{}/Historical_Data'.format(directory_path)

File_data = input_data_path + '/elspot-prices_2020_hourly_eur1.csv'

Price_data = pd.read_csv(File_data)

DK_da_ele_price = Price_data['DK1']

def Ele_price_prediction(temporaty_time =168):
    # ANN is planned to be used here, 20200616
    return DK_da_ele_price[temporaty_time:temporaty_time+24].to_numpy() # Eur/MWh

if __name__ == '__main__':
    a =Ele_price_prediction(temporaty_time=168)
    print(a)






