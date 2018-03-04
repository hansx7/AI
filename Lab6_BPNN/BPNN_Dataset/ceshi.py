import csv
import string
import numpy as np
import random
import math

def sigmoid(m):
	return 1.0 / (1+math.pow(math.e, -m))

def tanh(m):
	return (1 - math.pow(math.e, -2*m)) / (1 + math.pow(math.e, -2*m))

def calc_mse():
	global vrow, number_of_hidden, vs, w01, w1o, vans
	mse = 0
	for i in range(0, vrow):
		h1 = [0 for h in range(0, number_of_hidden)]
		for k in range(0, number_of_hidden):
			h1[k] = sigmoid(np.dot(vs[i], w01[k]))
		ho = np.dot(h1, w1o)
		mse += (ho - vans[i]) * (ho - vans[i]) / vrow
	return mse

# train_set = csv.reader(open('train.csv'))
# ts = []
# vs = []
# trow = 0
# vrow = 0
# tans = []
# vans = []
# for i in train_set:
# 	if i[0] == 'instant':
# 		continue
# 	r = random.randint(0,99)
# 	if r < 20:
# 		vrow += 1
# 		temp = []
# 		for j in range(2, len(i)-1):
# 			if j == 2:
# 				temp.append(string.atof(i[j])/4.0)
# 			elif j == 4:
# 				temp.append(string.atof(i[j])/12.0)
# 			elif j == 5:
# 				temp.append(string.atof(i[j])/23.0)
# 			elif j == 7:
# 				temp.append(string.atof(i[j])/7.0)
# 			elif j == 9:
# 				temp.append(string.atof(i[j])/4.0)
# 			else:
# 				temp.append(string.atof(i[j]))
# 		vans.append(string.atoi(i[len(i)-1]))
# 		temp.append(1)
# 		vs.append(temp)
# 	else:
# 		trow += 1
# 		temp = []
# 		for j in range(2, len(i)-1):
# 			if j == 2:
# 				temp.append(string.atof(i[j])/4.0)
# 			elif j == 4:
# 				temp.append(string.atof(i[j])/12.0)
# 			elif j == 5:
# 				temp.append(string.atof(i[j])/23.0)
# 			elif j == 7:
# 				temp.append(string.atof(i[j])/7.0)
# 			elif j == 9:
# 				temp.append(string.atof(i[j])/4.0)
# 			else:
# 				temp.append(string.atof(i[j]))
# 		tans.append(string.atoi(i[len(i)-1]))
# 		temp.append(1)
# 		ts.append(temp)
# col = len(ts[0])

number_of_hidden = 2
w01 = [[random.uniform(0, 1) for i in range(0, col-1)] for j in range(0, number_of_hidden)]
add = [1 for i in range(0, number_of_hidden)]
w01 = np.column_stack((w01, add))

w1o = [random.uniform(0, 1) for i in range(0, number_of_hidden-1)]
w1o.append(1)

iterations = 100
eta = 0.01
for i in range(0, iterations):
	delta_w01 = [[0 for f in range(0, col)] for ff in range(0, number_of_hidden)]
	delta_w1o = [0 for f in range(0, number_of_hidden)]
	for j in range(0, trow):                                                        #need to be changed
		if random.randint(0, 99) >= 20:
			continue
		h1 = [0 for h in range(0, number_of_hidden)]
		for k in range(0, number_of_hidden):
			h1[k] = sigmoid(np.dot(ts[j], w01[k]))
		ho = np.dot(h1, w1o)
		err_o = tans[j] - ho
		err_1 = [0 for e in range(0, number_of_hidden)]
		for k in range(0, number_of_hidden):
			err_1[k] = h1[k] * (1 - h1[k]) * err_o * w1o[k]
		err_0 = [0 for e in range(0, col)]
		for k in range(0, col):
			err_0[k] = 0
			for kk in range(0, number_of_hidden):
				err_0[k] += err_1[kk] * w01[kk][k]
			err_0[k] *= ts[j][k]
		for k in range(0, number_of_hidden):
			for kk in range(0, col):
				delta_w01[k][kk] += eta * err_0[kk] * ts[j][kk]
		delta_w1o += eta * np.multiply(err_1, h1)
	w01 += delta_w01
	w1o += delta_w1o

print calc_mse()