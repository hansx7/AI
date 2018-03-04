from numpy import *
import numpy as np
from numpy import random
import string
import csv
import matplotlib.pyplot as plt

def loadData(fileA):
    trainMat=[]
    fr=open(fileA)
    Date=[]
    for line in  fr.readlines():
        curLine=line.strip().split(',')
        trainMat.append(map(float,curLine))
    return mat(trainMat)
def sigmoid(inX):
    return 1.0/(1+exp(-inX))
def normalize(data):
    max1 = np.max(data, axis = 0)
    min1 = np.min(data, axis = 0)
    m1 = max1 - min1
    if np.min(np.array(m1)[0], axis = 0) == 0:
        return data
    else:
        return (data - min1) / m1

class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes,hidden2_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.hidden2_nodes=hidden2_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        #self.weights_input_to_hidden=mat([[0.2,0.4,-0.5,-0.4],[-0.3,0.1,0.2,0.2]])
        #self.weights_input_to_hidden =random.randint(0,1000,size=(hidden_nodes,input_nodes))
        #self.weights_input_to_hidden=self.weights_input_to_hidden*1.0/1000
        self.weights_input_to_hidden=np.random.normal(size=(hidden_nodes,input_nodes))
        self.weights_hidden_to_hidden=np.random.normal(size=(hidden2_nodes,hidden_nodes+1))
        self.weights_hidden_to_output=np.random.normal(size=(output_nodes,hidden2_nodes+1))
       # self.weights_hidden_to_hidden=random.randint(0,1000,size=(hidden2_nodes,hidden_nodes+1))
        #self.weights_hidden_to_hidden=self.weights_hidden_to_hidden*1.0/1000
        #self.weights_hidden_to_output =mat([-0.3,-0.2,0.1])
        #self.weights_hidden_to_output =random.randint(0,1000,size=(output_nodes,hidden2_nodes+1))
        #self.weights_hidden_to_output=self.weights_hidden_to_output*1.0/1000
        self.lr = learning_rate
        
        self.activation_function = sigmoid
    
    def train(self, inputs_list,iterator=10000):
        # Convert inputs list to 2d array
        inputs = inputs_list[:,:-1]
        # inputs=normalize(inputs)
        inputs= np.column_stack((inputs,ones((shape(inputs)[0],1))))
        targets =inputs_list[:,-1]
        cnt=0
        pred=[]
        min=10000
        for it in range(iterator):
            print it
            hidden_inputs = self.weights_input_to_hidden*inputs.T # signals into hidden layer)
            hidden_outputs =self.activation_function(hidden_inputs) # signals from hidden layer
            hidden_outputs=np.row_stack((hidden_outputs,ones((1,shape(hidden_outputs)[1]))))
            hidden2_inputs=self.weights_hidden_to_hidden*hidden_outputs
            hidden2_outputs=self.activation_function(hidden2_inputs)
            hidden2_outputs=np.row_stack((hidden2_outputs,ones((1,shape(hidden2_outputs)[1]))))

            final_inputs =self.weights_hidden_to_output*hidden2_outputs# signals into final output layer
            final_outputs =final_inputs # signals from final output layer
            # Output error
            output_errors =(targets.T-final_outputs) # Output layer error is the difference between desired target and actual output.)
            cnt=output_errors*output_errors.T
            mse=np.sqrt(cnt*1.0/len(inputs_list))
            if mse < 90:
                self.lr = 0.008
            if mse < 80:
                self.lr = 0.007
            if mse < 70:
                self.lr = 0.006
            if mse < 60:
                self.lr = 0.004
            # if mse < 50:
            #     self.lr = 0.002
            # print "cur:", mse

            '''
            if np.sqrt(cnt*1.0/len(inputs_list))<90:
                self.lr=0.008
            elif np.sqrt(cnt*1.0/len(inputs_list))<80:
                self.lr=0.006
            if it==iterator-1:
                pred.append(final_outputs)
                #cnt=output_errors*output_errors.T
            print "cur:",cnt*1.0/len(inputs_list),";"
            '''
                
            EW0=self.weights_hidden_to_output[:,:-1].T*output_errors
            der0=multiply(hidden2_outputs,1-hidden2_outputs)[:-1,:]
            hidden2_errors=multiply(der0,EW0)
            
            EW=self.weights_hidden_to_hidden[:,:-1].T*hidden2_errors
            der=multiply(hidden_outputs,1-hidden_outputs)[:-1,:]
            hidden_errors=multiply(EW,der)
            
            hidden2_grad=output_errors*hidden2_outputs.T
            hidden_grad=hidden2_errors*hidden_outputs.T
            input_grad=hidden_errors*inputs
            
            self.weights_hidden_to_output +=self.lr*hidden2_grad/len(inputs)
            self.weights_hidden_to_hidden+=self.lr*hidden_grad/len(inputs)
            self.weights_input_to_hidden +=self.lr*input_grad/len(inputs)

            result = self.run(testMat)
            print mse

        return cnt,pred,result
    
    def run(self, inputs_list):
        inputs = inputs_list
        # inputs=normalize(inputs)
        inputs= np.column_stack((inputs,ones((shape(inputs)[0],1))))
        hidden_inputs = self.weights_input_to_hidden*inputs.T # signals into hidden layer)
        hidden_outputs =self.activation_function(hidden_inputs) # signals from hidden layer
        hidden_outputs=np.row_stack((hidden_outputs,ones((1,shape(hidden_outputs)[1]))))
        hidden2_inputs=self.weights_hidden_to_hidden*hidden_outputs
        hidden2_outputs=self.activation_function(hidden2_inputs)
        hidden2_outputs=np.row_stack((hidden2_outputs,ones((1,shape(hidden2_outputs)[1]))))

        final_inputs =self.weights_hidden_to_output*hidden2_outputs# signals into final output layer
        final_outputs =final_inputs
        return final_outputs
trainMat=loadData('processed_deleted_train.csv')
testMat=loadData('processed_deleted_test.csv')
# for i in range(0,10):
#     trainMat[:,i]=trainMat[:,i]/max(trainMat[:,i])
#     testMat[:,i]=testMat[:,i]/max(testMat[:,i])
m,n=shape(trainMat)
NN=NeuralNetwork(n,80,20,1,0.01)  #n+1 n-5
cnt,pre,br=NN.train(trainMat,1500)
# print cnt*1.0/m
# print pre
# final_outputs=NN.run(testMat)
# out=final_outputs[0].tolist()[0]
# print out
# for i in out:
#     if i < 0:
#         i = 0
np.savetxt("reg.csv", br, fmt="%d", delimiter="\n", newline="\n")