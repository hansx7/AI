import numpy as np

a=np.matrix([[1,2,5],[2,1,2]])
b=np.max(a, axis=0)
c=np.min(a, axis=0)
print a
print b
print np.array(b)[0]