from numpy import *
import numpy as np
import csv
import math

def loadData(fileA):
	trainMat=[]
	fr=open(fileA)	
	for line in  fr.readlines():
		curLine=line.strip().split(',')
		trainMat.append(map(float,curLine))
	return mat(trainMat)

trainMat = loadData('processed_train.csv')
label = trainMat[:,-1]
trainMat = np.delete(trainMat, -1, axis=1)
dlt = []
for i in range(0, trainMat.shape[1]):
	attr = trainMat[:, i].T.tolist()[0]
	cor = corrcoef(attr, label.T.tolist()[0])[0][1]
	print cor
	if math.fabs(cor) < 0.01:
		dlt.append(i)
print dlt
trainMat = np.delete(trainMat, dlt, axis=1)
trainMat = np.column_stack((trainMat, label))
np.savetxt("processed_deleted_train.csv", trainMat, fmt="%f", delimiter=",", newline="\n")

testMat = loadData('processed_test.csv')
testMat = np.delete(testMat, dlt, axis=1)
np.savetxt("processed_deleted_test.csv", testMat, fmt="%f", delimiter=",", newline="\n")