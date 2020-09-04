'''
Created by Yi Zheng, 20200620

Using Multi-layer Perception ANN to predict wind speed

Input:wind speed data of the previous day(ndarray)
Output:hourly wind speed data(ndarray)
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader


# Fully connected neural network with one hidden layer
class WS_neural_network(nn.Module):

    def __init__(self, input_size, hidden_size):
        super(WS_neural_network, self).__init__()
        self.input_size = input_size
        self.l1_in = nn.Linear(input_size, hidden_size)  # The first layer here refers to the 1st hidden layer
        self.l1_out = nn.ReLU(self.l1_in)
        self.l2 = nn.Linear(hidden_size, 24)

    def forward(self, x):
        out = self.l1_in(x)
        out = self.l1_out(out)
        out = self.l2(out)
        return out

# ----------------------------------------------Build MLP ANN----------------------------------
input_size = 24
hidden_size = 40

ws_mlp_model = WS_neural_network(input_size, hidden_size)

try:
    ws_mlp_model.load_state_dict(torch.load("C:/phd/Paper/Paper0-system architecture/GreenLsbSkive_program"
                                            "/prediction_wind_solar_price_load/wind_mlp.pth"))
    print("loading wind speed prediction model parameters")
    ws_mlp_model.eval()
except IOError:
    print('Not trained')
except RuntimeError:# this exception appears when changing ANN size
    print('Adjusting network structure')


def prediction_function_wind_mlp(observed_data=np.array([1])):
    with torch.no_grad():
        observed_data_tensor = torch.from_numpy(observed_data.astype(np.float32))
        return ws_mlp_model(observed_data_tensor).numpy()

if __name__ == '__main__':
    # ----------------------------------------------Data preprocessing----------------------------------
    # Read historical data
    directory_path = os.path.dirname(__file__)
    input_data_path = r'{}/Historical_Data'.format(directory_path)

    File_data = input_data_path + '/pv_wind_data_2005_2016.csv'

    wind_speed_historical_data = pd.read_csv(File_data, index_col=0)
    wind_speed_historical_data.pop('Int')

    wind_speed = wind_speed_historical_data['WS10m']

    length_of_samples = 48  # length of recorded observations used for prediction, hours

    data_for_predicting = pd.DataFrame()

    for i in range(0, 1500):
        wind_speed_1 = wind_speed[0 + i * length_of_samples:(i + 1) * length_of_samples]
        wind_speed_1.reset_index(drop=True, inplace=True)
        x = wind_speed_1.to_frame()
        x = x.transpose()
        x.reset_index(drop=True, inplace=True)
        data_for_predicting = data_for_predicting.append(x)

    data_for_predicting.reset_index(drop=True, inplace=True)


    # Build a standard data set by inheriting a built-in data structure
    class historical_wind_speed(Dataset):

        def __init__(self, transform=None):
            ws = data_for_predicting.to_numpy(dtype=np.float32)
            self.n_samples = ws.shape[0]
            self.x_data = ws[:, :24]
            self.y_data = ws[:, 24:48]

        # support indexing such that dataset[i] can be used to get i-th sample
        def __getitem__(self, index):
            return self.x_data[index], self.y_data[index]

        # we can call len(dataset) to return the size
        def __len__(self):
            return self.n_samples


    hws = historical_wind_speed(transform=transforms.ToTensor())
    batch_size = 4
    train_loader = DataLoader(dataset=hws, batch_size=batch_size, shuffle=True)

    dataiter = iter(train_loader)
    data = dataiter.next()
    features, labels = data
    print(features, labels)

    # ----------------------------------------------Train MLP ANN---------------------------------------
    learning_rate = 1e-4
    objective_accuracy = 0.3

    # objective function
    criterion = nn.MSELoss()

    # optimizer
    optimizer = torch.optim.SGD(ws_mlp_model.parameters(), lr=learning_rate)

    # train model
    n_total_steps = len(train_loader)
    num_epochs = 200

    for epoch in range(num_epochs):
        for i, (wind_speed_train_in, wind_speed_train_out) in enumerate(train_loader):
            # wind_speed_train_out original size:4, should be transformed to [4,1]
            # wind_speed_train_out = wind_speed_train_out.reshape(batch_size,1)

            # forward process
            outputs = ws_mlp_model(wind_speed_train_in)
            loss = criterion(outputs, wind_speed_train_out)

            # backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')

            if loss.item() < objective_accuracy:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')
                break

        if loss.item() < objective_accuracy:
            break
            pass

    # 20160410
    previous_day_wind_speed_data = np.array([4.23, 4.53, 4.83, 5.13, 5.31, 5.49, 5.67, 5.66, 5.64, 5.63, 5.54, 5.46,
                                             5.38, 5.6, 5.83, 6.06, 5.84, 5.63, 5.42, 5.13, 4.83, 4.54, 4.37, 4.2],
                                            dtype=np.float32)
    # 20160411
    real_observed_wind_speed = np.array([4.03, 4.02, 4.01, 4, 3.92, 3.84, 3.77, 3.91, 4.06, 4.21, 4.29, 4.36, 4.44,
                                         4.73, 5.02, 5.31, 5.22, 5.13, 5.03, 4.94, 4.84, 4.74, 4.58, 4.42])

    predicted_wind_speed = prediction_function_wind_mlp(previous_day_wind_speed_data)

    #save the model parameters to avoid training it every time
    file = "wind_mlp.pth"
    torch.save(ws_mlp_model.state_dict(),file)

    fig, ax = plt.subplots()
    ax.plot(range(real_observed_wind_speed.__len__()),real_observed_wind_speed,color = 'red',label = "real data")
    ax.plot(range(predicted_wind_speed.__len__()),predicted_wind_speed,color = 'blue',label = "predicted data")
    ax.set_ylim([3,6])
    plt.show()


