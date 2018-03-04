from sklearn import svm
from sklearn.svm import SVR
import numpy as np
import csv
import string
import random

def is_number(s):
	try:
		float(s)
		return True
	except Exception as e:
		return False

train_set = csv.reader(open('processed_train.csv'))
col = 12
ts = np.array([0 for i in range(0, col)])
vs = np.array([0 for i in range(0, col)])
label = np.array([])
answer = np.array([])
cnt = 0
for i in train_set:
	if is_number(i[0]) == False:
		continue
	temp = np.array([])
	for j in range(0, col):
		temp = np.hstack((temp, string.atof(i[j+1])))
	temp[0] -= 2011
	div = random.randint(0, 100)
	if div <= (742.0/16637*100):
		cnt += 1
		vs = np.row_stack((vs, temp))
		answer = np.hstack((answer, int(string.atof(i[col+1]))))
	else:
		ts = np.row_stack((ts, temp))
		label = np.hstack((label, int(string.atof(i[col+1]))))
ts = np.delete(ts, 0, axis=0)
vs = np.delete(vs, 0, axis=0)

test_set = csv.reader(open('processed_test.csv'))
tts = np.array([0 for i in range(0, col)])
for i in test_set:
	if is_number(i[0]) == False:
		continue
	temp = np.array([])
	for j in range(0, col):
		temp = np.hstack((temp, string.atof(i[j+1])))
	temp[0] -= 2011
	tts = np.row_stack((tts, temp))
tts = np.delete(tts, 0, axis=0)

clf = svm.SVR()
clf.fit(ts, label)

res = clf.predict(tts)
writer = csv.writer(file('22_v10.csv','wb'))
for i in res:
	if i >= 0:
		writer.writerow([int(i)])
	else:
		writer.writerow([0])