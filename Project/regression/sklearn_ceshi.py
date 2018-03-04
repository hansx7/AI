from sklearn import svm
from sklearn.svm import SVR
from sklearn.svm import SVC
import numpy as np
X = np.array([[0, 0], [1, 1], [1, 0]])  # training samples   
y = np.array([0, 1, 1])  # training target  
clf = svm.SVC()  # class   
clf.fit(X, y)  # training the svc model  
z = np.array([[2,2]])
result = clf.predict(z) # predict the target of testing samples   
print result  # target 