'''
A generic dynamic model parameterized to represent most popular types of rechargeable batteries

Refer to: Sizing optimization, dynamic modeling and energy management strategies of a stand-alone PV/hydrogen/
battery-based hybrid system

'''
import matplotlib.pyplot as plt

class battery_bank():
    def __init__(self,capacity = 250, E_bat = 12, serial_number = 30, parallel_number = 300,
                 internal_resistance = 0.05, soc = 0.1, soc_min = 0.1, soc_max = 0.85):
        self.capacity = capacity* parallel_number #Ah
        self.E_bat = E_bat *serial_number # no load voltage
        self.serial_number = serial_number
        self.parallel_number = parallel_number
        self.internal_resistance = internal_resistance/parallel_number*serial_number
        self.soc = soc # state of charge
        self.soc_min = soc_min
        self.soc_max = soc_max

    def charge(self, time = 3600, I = 3600):
        # Using the CC (Constant Current) control method
        charge_power = (self.E_bat + I * self.internal_resistance)*I / 1e6
        soc_estimation = self.soc + I*time/3600 / self.capacity
        if soc_estimation > self.soc_max:
            return 0
        else:
            self.soc = self.soc + I * time / 3600 / self.capacity
            return charge_power

    def discharge(self, time = 3600, I = 4000):
        # Using the CC (Constant Current) control method
        discharge_power = (self.E_bat - I * self.internal_resistance) * I /1e6
        soc_estimation = self.soc - I * time / 3600 / self.capacity
        if soc_estimation < self.soc_min:
            return 0
        else:
            self.soc = self.soc - I * time / 3600 / self.capacity
            return -discharge_power


if __name__ == "__main__":
    a = battery_bank(soc=0.6)
    print('Initial soc: {}'.format(a.soc))
    #-------------------Performance in constant current supply ---------------------------------
    soc_hour = []
    for i in range(3600):
        a.charge(time=1)
        soc_hour.append(a.soc)
    fig, ax = plt.subplots()
    ax.plot(range(3600),soc_hour)
    plt.show()

