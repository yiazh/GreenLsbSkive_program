'''
Using Multi-linear Regression to predict wind speed, which is not so accurate. With a longer time horizon,
the prediction result becomes worse.

This program is going to use wind speed data observed today to forecast that of tomorrow.A whole year's data
is used to train this model.Assuming that wind speed today is represented by vector: $V = v_0,\codts, v_{23}$,
we want to find a matrix B to predict wind speed tomorrow by \hat{V_1}= V*B
'''

import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
import os

# df = pd.read_csv()
directory_path = os.path.dirname(__file__)
input_data_path = r'{}/Historical_Data'.format(directory_path)

File_data = input_data_path + '/pv_wind_data_2016.csv'

Ambient_Data = pd.read_csv(File_data, index_col=0)
Ambient_Data.pop('Int')

wind_speed = Ambient_Data['WS10m']

number_of_samples = 48 # number of recorded observations used for prediction

data_for_predicting = pd.DataFrame()
for i in range(0,150):
    wind_speed_1 = wind_speed[0+i*number_of_samples:(i+1)*number_of_samples]
    wind_speed_1.reset_index(drop = True, inplace = True)
    x = wind_speed_1.to_frame()
    x = x.transpose()
    x.reset_index(drop = True, inplace = True)
    data_for_predicting = data_for_predicting.append(x)# This loop is used to change the form of data

data_for_predicting.reset_index(drop = True, inplace = True)
# regression coefficient matrix b_matrix and intercept vector a_vector_list
b_matrix_list = []
a_vector_list = []
score = []
for i in range(0,24):#using data of previous day to predict wind speed of ith hour in the next day
    # Divide the data set into training set and test set using package provided by sklearn
    X_train, X_test, Y_train, Y_test = train_test_split(data_for_predicting.iloc[:, :24],
                                                        data_for_predicting.iloc[:, 24+i], train_size=.80)

    model = LinearRegression()

    model.fit(X_train, Y_train)

    a = model.intercept_  # intercept
    a_vector_list.append(a)

    b = model.coef_  # regression coefficient
    b_matrix_list.append(b)

    score_1 = model.score(X_test, Y_test)
    score.append(score_1)

    Y_pred = model.predict(X_test)
#
# def prediction_function_wind(observed_data=np.array([1])):
#     try:
#         observed_data.__len__()
#     except:
#         print('Error')
#     data = observed_data[-number_of_samples + 1:]
#     res = []
#     for j in range(0,24):
#         res.append(a + np.dot(b, data))
#         data = np.append(data, a + np.dot(b,data))
#         data = np.delete(data, 0)
#     return np.array(res)
#
b_matrix = np.array(b_matrix_list)
a_vector = np.array(a_vector_list)

if __file__ == '__main__':
    # 20160410 real data
    day_ahead_wind_speed_data = np.array([4.23, 4.53, 4.83, 5.13, 5.31, 5.49, 5.67, 5.66, 5.64, 5.63, 5.54, 5.46,
                                          5.38, 5.6, 5.83, 6.06, 5.84, 5.63, 5.42, 5.13, 4.83, 4.54, 4.37, 4.2])
    # 20160411 real data, for reference
    real_observed_wind_speed = np.array([4.03, 4.02, 4.01, 4, 3.92, 3.84, 3.77, 3.91, 4.06, 4.21, 4.29, 4.36, 4.44,
                                         4.73, 5.02, 5.31, 5.22, 5.13, 5.03, 4.94, 4.84, 4.74, 4.58, 4.42])
    prediction = day_ahead_wind_speed_data.dot(b_matrix.transpose()) + a_vector
    fig, ax = plt.subplots()
    ax.plot(range(len(real_observed_wind_speed)), real_observed_wind_speed, 'b', label="predict")
    ax.plot(range(len(prediction)), prediction, 'r', label="test")
    plt.show()

    fig2, ax2 = plt.subplots()
    ax2.scatter(prediction,real_observed_wind_speed)


