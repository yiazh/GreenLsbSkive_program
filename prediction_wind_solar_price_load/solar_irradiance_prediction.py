'''
Created by Yi Zheng, 20200620

Using Multi-layer Perception ANN to predict solar irradiance. This program is the same as the one predicting wind speed
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

# ----------------------------------------------Build MLP ANN----------------------------------
input_size = 24
hidden_size = 10

# Fully connected neural network with one hidden layer
class SI_neural_network(nn.Module):

    def __init__(self, input_size, hidden_size):
        super(SI_neural_network, self).__init__()
        self.input_size = input_size
        self.l1_in = nn.Linear(input_size, hidden_size)  # The first layer here refers to the 1st hidden layer
        self.l1_out = nn.ReLU(self.l1_in)
        self.l2 = nn.Linear(hidden_size, 24)

    def forward(self, x):
        out = self.l1_in(x)
        out = self.l1_out(out)
        out = self.l2(out)
        return out

si_mlp_model = SI_neural_network(input_size, hidden_size)

#--------------------Try to load existing model parameters-----------------------------------------
try:
    si_mlp_model.load_state_dict(torch.load("C:/phd/Paper/Paper0-system architecture/GreenLsbSkive_program"
                                            "/prediction_wind_solar_price_load/solar_mlp.pth"))
    si_mlp_model.eval()
    print("loading solar irradiacne prediction model parameters")
except IOError:
    print("Not trained")

def prediction_fun_solar_irradiance(observed_data=np.array(range(0,24))):
    with torch.no_grad():
        observed_data_tensor = torch.from_numpy(observed_data.astype(np.float32))
        return si_mlp_model(observed_data_tensor).numpy()

if __name__ == '__main__':
    # ----------------------------------------------Data preprocessing----------------------------------
    # Read historical data
    directory_path = os.path.dirname(__file__)
    input_data_path = r'{}/Historical_Data'.format(directory_path)

    File_data = input_data_path + '/pv_wind_data_2016.csv'

    solar_ira_his_data = pd.read_csv(File_data, index_col=0)

    solar_irradiance = solar_ira_his_data['G(i)']

    length_of_samples = 24  # length of recorded observations used for prediction, hours
    start_day = 97

    data_for_predicting = pd.DataFrame()

    for i in range(0, 3):
        solar_irradiance_1 = solar_irradiance[
                             24 * start_day + i * length_of_samples:24 * start_day + (i + 1) * length_of_samples]
        solar_irradiance_1.reset_index(drop=True, inplace=True)
        x = pd.Series(np.array(range(0, 24))).append(solar_irradiance_1).to_frame()
        x = x.transpose()
        x.reset_index(drop=True, inplace=True)
        data_for_predicting = data_for_predicting.append(x)

    data_for_predicting.reset_index(drop=True, inplace=True)
    data_for_predicting = data_for_predicting.transpose()
    data_for_predicting.reset_index(drop=True, inplace=True)
    data_for_predicting = data_for_predicting.transpose()

    # Build a standard data set by inheriting a built-in data structure
    class historical_solar_irradiance(Dataset):

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

    hsi = historical_solar_irradiance(transform=transforms.ToTensor())

    batch_size = 5
    train_loader = DataLoader(dataset=hsi, batch_size=batch_size, shuffle=True)

    # ----------------------------------------------Train MLP ANN---------------------------------------
    learning_rate = 1e-2
    objective_accuracy =85.5

    # objective function
    criterion = nn.MSELoss()

    # optimizer
    optimizer = torch.optim.SGD(si_mlp_model.parameters(), lr=learning_rate)

    # train model
    n_total_steps = len(train_loader)
    num_epochs = 10000

    for epoch in range(num_epochs):
        for i, (solar_irradiance_train_in, solar_irradiance_train_out) in enumerate(train_loader):
            # solar_irradiance_train_out original size:4, should be transformed to [4,1]
            # solar_irradiance_train_out = solar_irradiance_train_out.reshape(batch_size,1)

            # forward process
            outputs = si_mlp_model(solar_irradiance_train_in)
            loss = criterion(outputs, solar_irradiance_train_out)

            # backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')

            if loss.item() < objective_accuracy ** 2:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')
                break

        if loss.item() < objective_accuracy ** 2:
            break

    #save model parameters
    file = "solar_mlp.pth"
    torch.save(si_mlp_model.state_dict(),file)

    time = np.array(range(0,24),dtype=np.float32)
    predicted_solar_irradiance = prediction_fun_solar_irradiance(time)

    fig, ax = plt.subplots()
    ax.plot(time, predicted_solar_irradiance,color = 'blue',label = "predicted data")
    plt.show()


