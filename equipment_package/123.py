import math
import matplotlib.pyplot as plt

c =[i*(0.67+0.33*math.exp(-0.00174*i**2)) for i in range(100)]
fig, ax = plt.subplots()
ax.plot(range(100),c)
plt.show()
