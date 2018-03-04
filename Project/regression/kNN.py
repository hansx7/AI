import csv
import string
import numpy as np

def calEuclideanDistance(vec1, vec2):  
	dist = np.sqrt(np.sum(np.square(vec1 - vec2)))  
	return dist

def calCosDistance(vec1, vec2):
	dist = np.dot(vec1, vec2) / sum(vec1 ** 2) ** 0.5 / sum(vec2 ** 2) ** 0.5
	return dist

trainMat=[]
fr=open('processed_train.csv')
for line in fr.readlines():
	curLine=line.strip().split(',')
	trainMat.append(map(float,curLine))
testMat=[]
fr=open('processed_test.csv')
for line in fr.readlines():
	curLine=line.strip().split(',')
	testMat.append(map(float,curLine))

