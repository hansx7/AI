import numpy as np
import matplotlib.pyplot as plt

a=np.array([1,2,3])
b=np.array([1,2,3])
plt.figure("fie2")
plt.plot(a,b)
plt.show()
c=np.matrix([[1,2],[3,4]])
print c.tolist()[0]