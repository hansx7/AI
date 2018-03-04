import csv
import string
import numpy as np

a = csv.reader(open('reg.csv'))
b = csv.reader(open('answer.csv'))
na = np.array([])
nb = np.array([])

for i in a:
	na = np.hstack((na,string.atoi(i[0])))
for i in b:
	nb = np.hstack((nb,string.atoi(i[0])))

e = na - nb
f = np.dot(e, e)
print np.sqrt(f*1.0/742)