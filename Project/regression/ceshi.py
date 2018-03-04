import string
from numpy import *
import numpy as np
import math
import random
import matplotlib.pyplot as plt

# a=np.array([[1,2,3],[2,3,4]])
# b=np.array([1,2,3])
# print a
# a=np.hstack((a,[[4],[5]]))
# for i in a:
# 	print i
# c=np.array(['instant'])
# print b
# print c
# c=np.hstack((c,b))
# print c
# c=np.hstack((b,c))
# print c
# d=np.array([1,2,3,4,5,6,7])
# print d
# print d[-1]
# e=np.array([0 for i in range(0,7)])
# d=np.row_stack((e,d))
# print d

# print '-------------'
# a="2011/11/11"
# b=np.array([1,2,3])
# b=np.column_stack((b,a.split('/')))
# print b

# print '-------------'
# a=np.array([1,2,3,4])
# print a
# a=np.insert(a,1,5.9)
# print a

# a=np.array([1,2,3,4])
# b=np.array([2,3,4,5])
# def calCosDistance(vec1, vec2):
# 	dist = np.dot(vec1, vec2) / sum(vec1 ** 2) ** 0.5 / sum(vec2 ** 2) ** 0.5
# 	return dist
# print calCosDistance(a,b)
# print 20/math.sqrt(14)/math.sqrt(29)
# if 10 in a:
# 	print '1'
# else:
# 	print '0'

# print '-------------'
# for i in range(0, 100):
# 	print random.randint(0,100),

a=[1,2,3,4,5,6,7,8,9]
b=[99,98,97,6,5,4,13,21,1]
plt.plot(a,b)
plt.show()
# print corrcoef(a,b)[0][1]

# c=np.matrix([[1,2,3],[2,3,4]])
# print c
# c=np.delete(c,[0,1],axis=1)
# print c