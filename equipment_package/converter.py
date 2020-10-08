'''
Created on: 20201006

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
import matplotlib.pyplot as plt
import pwlf
import numpy as np

class converter(object):
    def __init__(self, p_nom, n10=0.93, n100=0.98):
        self.p_nom = p_nom
        self.n0 = (10/n10+1/n100-9)/(99)
        self.n10 = n10
        self.n100 = n100
        self.m = 1/n100-self.n0-1

    def eta(self, p_s):
        return (p_s/self.p_nom)/(p_s/self.p_nom+ self.n0+self.m*(p_s/self.p_nom)**2)

    def p_output(self,p_input):
        return p_input*self.eta(p_input)

if __name__ == '__main__':
    a = converter(14,0.90,0.98)
    x = np.linspace(0,3,20)
    y = np.array([a.p_output(i) for i in x])

    # piecewise linearization
    '''
    @Manual{pwlf,
    author = {Jekel, Charles F. and Venter, Gerhard},
    title = {{pwlf:} A Python Library for Fitting 1D Continuous Piecewise Linear Functions},
    year = {2019},
    url = {https://github.com/cjekel/piecewise_linear_fit_py}
    }
    '''
    my_pwlf = pwlf.PiecewiseLinFit(x, y)
    breaks = my_pwlf.fit(3)
    print(breaks)

    x_hat = np.linspace(x.min(), x.max(), 100)
    y_hat = my_pwlf.predict(x_hat)

    fig, ax = plt.subplots()
    ax.plot(x,y,'o')
    ax.plot(x_hat,y_hat,'-')
    plt.show()

