import numpy as np
from scipy.stats import weibull_min
# np.random.seed(seed=1)
a = np.random.uniform()
b = np.random.weibull(4)
# Simulating wind speed via weibull distribution
n = 1  # number of samples
k = 2  # shape factor should be calculated from the wind data, not available now
lam = 5  # scale,should be calculated from the wind data, not available now
v_wind = weibull_min.rvs(k, loc=0, scale=lam, size=n)